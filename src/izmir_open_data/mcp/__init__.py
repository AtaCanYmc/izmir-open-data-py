import inspect
import re
import urllib.parse
from typing import Any

from fastmcp import FastMCP

from izmir_open_data.core.client import IzmirClient

# Initialize FastMCP server
mcp = FastMCP("izmir-open-data")

DISALLOWED_NAMESPACES = {
    "close",
    "get",
    "get_ckan",
    "get_ckan_dump",
    "get_csv",
    "cache",
    "clear_cache",
    "retry_config",
    "api_key",
    "base_url",
    "ckan_base_url",
    "ckan_dump_base_url",
}


@mcp.tool()
async def list_endpoints() -> list[str]:
    """
    List all available namespaces and their endpoints in the Izmir Open Data API.
    Returns a list of strings in the format "namespace.method_name: Description".
    LLMs can use this to discover what data they can fetch.
    """
    endpoints = []
    async with IzmirClient() as client:
        for attr_name in sorted(dir(client)):
            if attr_name.startswith("_") or attr_name in DISALLOWED_NAMESPACES:
                continue

            attr_val = getattr(client, attr_name)
            if (
                hasattr(attr_val, "__class__")
                and "Endpoint" in attr_val.__class__.__name__
            ):
                for method_name in sorted(dir(attr_val)):
                    if method_name.startswith("_"):
                        continue
                    method = getattr(attr_val, method_name)
                    if callable(method):
                        doc = inspect.getdoc(method) or "No description available."
                        short_doc = doc.strip().split("\n")[0]
                        endpoints.append(f"{attr_name}.{method_name}: {short_doc}")

    return endpoints


@mcp.tool()
async def get_dataset(dataset_id: str) -> dict | list:
    """
    Fetch a dataset from the Izmir Open Data API using raw ibb/ dataset id.
    DEPRECATED for direct LLM use: Prefer to use call_endpoint instead.

    Args:
        dataset_id: The ID of the dataset to fetch (e.g., 'cbs/hastaneler')
    """
    unquoted = urllib.parse.unquote(dataset_id)
    if ".." in unquoted or not re.match(r"^[a-zA-Z0-9_\-/]+$", dataset_id):
        raise ValueError("Geçersiz veya güvensiz dataset_id formatı.")

    async with IzmirClient() as client:
        return await client.get(f"ibb/{dataset_id}")


@mcp.tool()
async def call_endpoint(
    namespace: str,
    endpoint_name: str,
    kwargs_dict: dict[str, Any] | None = None,
    args: list[Any] | None = None,
) -> dict | list | str:
    """
    Call a specific endpoint from the Izmir Open Data Python Client.
    Use list_endpoints() first to see available namespaces and endpoint_names.

    Args:
        namespace: The namespace (e.g. 'eshot', 'bisim', 'kamu', 'otopark', 'ckan', 'itfaiye', 'tuvalet')
        endpoint_name: The method name (e.g. 'get_istasyon_list', 'search_packages', 'get_akilli_tuvaletler')
        kwargs_dict: Optional dictionary of keyword arguments to pass to the method.
        args: Optional list of positional arguments to pass to the method.
    """
    if namespace in DISALLOWED_NAMESPACES or namespace.startswith("_"):
        return f"Error: Unauthorized or invalid namespace: '{namespace}'."

    async with IzmirClient() as client:
        if not hasattr(client, namespace):
            return f"Error: Namespace '{namespace}' not found."

        ns_obj = getattr(client, namespace)
        if not (
            hasattr(ns_obj, "__class__") and "Endpoint" in ns_obj.__class__.__name__
        ):
            return f"Error: '{namespace}' is not a valid API endpoint namespace."

        if not hasattr(ns_obj, endpoint_name) or endpoint_name.startswith("_"):
            return f"Error: Endpoint '{endpoint_name}' not found in namespace '{namespace}'."

        method = getattr(ns_obj, endpoint_name)
        if not callable(method):
            return f"Error: '{endpoint_name}' is not callable."

        try:
            pos_args = args or []
            kw_args = kwargs_dict or {}

            if inspect.iscoroutinefunction(method):
                result = await method(*pos_args, **kw_args)
            else:
                result = method(*pos_args, **kw_args)

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
