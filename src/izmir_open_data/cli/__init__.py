import asyncio

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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
                # Show a waiting message using console status (optional, but Panel is good for intro)
                console.print(
                    Panel(
                        f"Fetching dataset: [bold cyan]{dataset_id}[/bold cyan] from İzmir Open Data...",
                        border_style="blue",
                    )
                )

                data = await client.get(f"ibb/{dataset_id}")

                # Dinamik olarak listeyi bul (direkt liste veya 'onemliyer' / 'kayitlar' key'i icindeki liste)
                items = []
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    if "onemliyer" in data and isinstance(data["onemliyer"], list):
                        items = data["onemliyer"]
                    elif "kayitlar" in data and isinstance(data["kayitlar"], list):
                        items = data["kayitlar"]
                    else:
                        # Fallback to json if structure is completely unknown
                        console.print_json(data=data)
                        return

                if not items:
                    console.print(
                        Panel(
                            "[yellow]Veri bulunamadı veya liste boş.[/yellow]",
                            title="Uyarı",
                            border_style="yellow",
                        )
                    )
                    return

                table = Table(
                    show_header=True,
                    header_style="bold magenta",
                    border_style="cyan",
                    title=f"Dataset: [bold cyan]{dataset_id}[/bold cyan]",
                    show_lines=True,
                    row_styles=["none", "dim"],
                )

                # Get columns from the first item
                # Many APIs return keys like 'Id', 'Adi', 'Aciklama', 'Enlem', 'Boylam'. We'll show first 6 keys to avoid terminal clutter.
                first_item = items[0]
                keys_to_show = list(first_item.keys())[:6]

                colors = ["cyan", "yellow", "green", "magenta", "blue", "red"]
                for idx, key in enumerate(keys_to_show):
                    table.add_column(str(key), style=colors[idx % len(colors)])

                for item in items:
                    row = [str(item.get(k, "")) for k in keys_to_show]
                    table.add_row(*row)

                console.print(table)

                # Footer note
                if len(first_item.keys()) > 6:
                    console.print(
                        Panel(
                            f"[dim]Not: Terminale sığması için toplam {len(first_item.keys())} sütundan sadece ilk 6'sı gösteriliyor.\n"
                            f"Görünmeyen sütunlar: {', '.join(list(first_item.keys())[6:])}[/dim]",
                            title="Bilgi",
                            border_style="dim",
                        )
                    )

            except Exception as e:
                console.print(
                    Panel(
                        f"[bold red]Hata oluştu:[/bold red] {e}",
                        title="Hata",
                        border_style="red",
                    )
                )

    run_async(_get())


if __name__ == "__main__":
    app()
