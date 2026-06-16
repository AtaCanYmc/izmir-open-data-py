import inspect

from fastmcp import FastMCP

from izmir_open_data.core.client import IzmirClient

# Initialize FastMCP server
mcp = FastMCP("izmir-open-data")


@mcp.tool()
async def list_endpoints() -> list[str]:
    """
    List all available namespaces and their endpoints in the Izmir Open Data API.
    Returns a list of strings in the format "namespace.method_name: Description".
    LLMs can use this to discover what data they can fetch.
    """
    endpoints = []

    # We create a temporary client just to inspect its properties
    client = IzmirClient()

    for attr_name in dir(client):
        # Ignore private attributes and basic properties
        if attr_name.startswith("_") or attr_name in ["close", "get"]:
            continue

        attr_val = getattr(client, attr_name)
        # If it's an Endpoint class instance
        if hasattr(attr_val, "__class__") and "Endpoint" in attr_val.__class__.__name__:
            # Inspect its methods
            for method_name in dir(attr_val):
                if method_name.startswith("get_"):
                    method = getattr(attr_val, method_name)
                    doc = inspect.getdoc(method) or "No description available."
                    # Get the first line of the docstring for brevity
                    short_doc = doc.strip().split("\n")[0]
                    endpoints.append(f"{attr_name}.{method_name}: {short_doc}")

    return endpoints


@mcp.tool()
async def get_dataset(dataset_id: str) -> dict:
    """
    Fetch a dataset from the Izmir Open Data API using raw ibb/ dataset id.
    DEPRECATED for direct LLM use: Prefer to use call_endpoint instead.

    Args:
        dataset_id: The ID of the dataset to fetch (e.g., 'cbs/hastaneler')
    """
    async with IzmirClient() as client:
        data = await client.get(f"ibb/{dataset_id}")
        return data


@mcp.tool()
async def call_endpoint(
    namespace: str, endpoint_name: str, kwargs_dict: dict | None = None
) -> dict | list | str:
    """
    Call a specific endpoint from the Izmir Open Data Python Client.
    Use list_endpoints() first to see available namespaces and endpoint_names.

    Args:
        namespace: The namespace (e.g. 'eshot', 'bisim', 'kamu', 'otopark')
        endpoint_name: The method name (e.g. 'get_istasyon_list', 'get_hastaneler_list')
        kwargs_dict: Optional dictionary of arguments to pass to the method (e.g. {"enlem": 38.4, "boylam": 27.1})
    """
    async with IzmirClient() as client:
        if not hasattr(client, namespace):
            return f"Error: Namespace '{namespace}' not found."

        ns_obj = getattr(client, namespace)
        if not hasattr(ns_obj, endpoint_name):
            return f"Error: Endpoint '{endpoint_name}' not found in namespace '{namespace}'."

        method = getattr(ns_obj, endpoint_name)

        try:
            if kwargs_dict:
                result = await method(**kwargs_dict)
            else:
                result = await method()

            # If the result is a Pydantic model (or a list of them), convert to dict so MCP can serialize it
            if hasattr(result, "model_dump"):
                return result.model_dump()
            elif (
                isinstance(result, list)
                and len(result) > 0
                and hasattr(result[0], "model_dump")
            ):
                return [item.model_dump() for item in result]

            return result
        except Exception as e:
            return f"Error calling {namespace}.{endpoint_name}: {str(e)}"


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
