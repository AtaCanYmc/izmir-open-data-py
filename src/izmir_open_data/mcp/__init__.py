from fastmcp import FastMCP

from izmir_open_data.core.client import IzmirClient

# Initialize FastMCP server
mcp = FastMCP("izmir-open-data", description="Izmir Open Data MCP Server")


@mcp.tool()
async def get_dataset(dataset_id: str) -> dict:
    """
    Fetch a dataset from the Izmir Open Data API.
    
    Args:
        dataset_id: The ID of the dataset to fetch (e.g., 'hal-fiyatlari')
    """
    async with IzmirClient() as client:
        data = await client.get(f"ibb/{dataset_id}")
        return data


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
