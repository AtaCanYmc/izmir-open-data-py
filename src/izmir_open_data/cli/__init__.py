import asyncio

import typer
from rich.console import Console

from izmir_open_data.core.client import IzmirClient

app = typer.Typer(help="Izmir Open Data CLI")
console = Console()


def run_async(coro):
    return asyncio.run(coro)


@app.callback()
def main():
    """Izmir Open Data CLI"""
    pass


@app.command()
def get(dataset_id: str = typer.Argument(..., help="The ID of the dataset to fetch")):
    """Fetch and display a dataset from Izmir Open Data API."""

    async def _get():
        async with IzmirClient() as client:
            try:
                data = await client.get(f"ibb/{dataset_id}")
                console.print_json(data=data)
            except Exception as e:
                console.print(f"[bold red]Error fetching dataset:[/bold red] {e}")

    run_async(_get())


if __name__ == "__main__":
    app()
