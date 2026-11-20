import asyncio
import re
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from izmir_open_data.core.client import IzmirClient

app = typer.Typer(help="Izmir Open Data CLI")
console = Console()


def run_async(coro):
    return asyncio.run(coro)


def format_value(val: Any) -> str:
    if isinstance(val, (dict, list)):
        import json

        val = json.dumps(val, ensure_ascii=False)
    s = str(val if val is not None else "")
    s = re.sub(r"[\r\n\t]+", " ", s)
    if len(s) > 40:
        return s[:37] + "..."
    return s


@app.callback()
def main():
    """Izmir Open Data CLI"""
    pass


@app.command()
def get(
    dataset_id: str = typer.Argument(
        ..., help="The ID of the dataset to fetch (e.g. 'cbs/adayarimada')"
    ),
):
    """Fetch and display a dataset from Izmir Open Data API."""

    if ".." in dataset_id or not re.match(r"^[a-zA-Z0-9_\-/]+$", dataset_id):
        console.print(
            Panel(
                "[bold red]Hata:[/bold red] Geçersiz veya güvensiz dataset_id formatı.",
                title="Hata",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    async def _get():
        async with IzmirClient() as client:
            try:
                console.print(
                    Panel(
                        f"Fetching dataset: [bold cyan]{dataset_id}[/bold cyan] from İzmir Open Data...",
                        border_style="blue",
                    )
                )

                data = await client.get(f"ibb/{dataset_id}")

                items: list[Any] = []
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    if isinstance(data.get("onemliyer"), list):
                        items = data["onemliyer"]
                    elif isinstance(data.get("kayitlar"), list):
                        items = data["kayitlar"]
                    else:
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

                first_item = items[0]
                all_keys = (
                    list(first_item.keys()) if isinstance(first_item, dict) else []
                )
                keys_to_show = all_keys[:6]

                table = Table(
                    show_header=True,
                    header_style="bold magenta",
                    border_style="cyan",
                    title=f"Dataset: [bold cyan]{dataset_id}[/bold cyan]",
                    show_lines=True,
                    row_styles=["none", "dim"],
                )

                colors = ["cyan", "yellow", "green", "magenta", "blue", "red"]
                for idx, key in enumerate(keys_to_show):
                    table.add_column(str(key), style=colors[idx % len(colors)])

                for item in items:
                    if isinstance(item, dict):
                        row = [format_value(item.get(k)) for k in keys_to_show]
                        table.add_row(*row)

                console.print(table)

                if len(all_keys) > 6:
                    console.print(
                        Panel(
                            f"[dim]Not: Terminale sığması için toplam {len(all_keys)} sütundan sadece ilk 6'sı gösteriliyor.\n"
                            f"Görünmeyen sütunlar: {', '.join(all_keys[6:])}[/dim]",
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
                raise typer.Exit(1)

    run_async(_get())


@app.command()
def search(
    query: str = typer.Argument(
        ..., help="Search keyword (e.g. 'otopark', 'tuvalet', 'itfaiye')"
    ),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum results to display"),
):
    """Search across all 260+ datasets on acikveri.bizizmir.com."""

    async def _search():
        async with IzmirClient() as client:
            try:
                console.print(
                    Panel(
                        f"Searching datasets for: [bold cyan]{query}[/bold cyan] in İzmir Açık Veri...",
                        border_style="blue",
                    )
                )

                res = await client.ckan.search_packages(query, rows=limit)
                results = res.get("results", []) if isinstance(res, dict) else []

                if not results:
                    console.print(
                        Panel(
                            f"[yellow]'{query}' ile eşleşen veri seti bulunamadı.[/yellow]",
                            title="Uyarı",
                            border_style="yellow",
                        )
                    )
                    return

                total_count = res.get("count", len(results))
                console.print(
                    f"[green]Toplam bulunan veri seti: {total_count} (Gösterilen: {len(results)})[/green]\n"
                )

                table = Table(
                    show_header=True,
                    header_style="bold magenta",
                    border_style="cyan",
                    title="Arama Sonuçları",
                    show_lines=True,
                )
                table.add_column("ID / Slug", style="cyan")
                table.add_column("Başlık", style="green")
                table.add_column("Kaynak Sayısı", style="yellow")

                for pkg in results:
                    table.add_row(
                        format_value(pkg.get("name")),
                        format_value(pkg.get("title")),
                        format_value(pkg.get("num_resources")),
                    )

                console.print(table)

            except Exception as e:
                console.print(
                    Panel(
                        f"[bold red]Arama hatası:[/bold red] {e}",
                        title="Hata",
                        border_style="red",
                    )
                )
                raise typer.Exit(1)

    run_async(_search())


@app.command()
def datastore(
    resource_id: str = typer.Argument(
        ...,
        help="The UUID of the CKAN resource (e.g. 'd87de3c1-9bc0-4a8c-842a-90cd2a30d03a')",
    ),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of records to fetch"),
    query: str | None = typer.Option(
        None, "--query", "-q", help="Full text search query"
    ),
):
    """Query records from any CKAN datastore resource ID."""

    if not re.match(r"^[a-zA-Z0-9_\-]+$", resource_id):
        console.print(
            Panel(
                "[bold red]Hata:[/bold red] Geçersiz veya güvensiz resource_id formatı.",
                title="Hata",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    async def _datastore():
        async with IzmirClient() as client:
            try:
                console.print(
                    Panel(
                        f"Fetching records from resource: [bold cyan]{resource_id}[/bold cyan]...",
                        border_style="blue",
                    )
                )

                res = await client.ckan.search_datastore(
                    resource_id, limit=limit, q=query
                )
                records = res.get("records", []) if isinstance(res, dict) else []

                if not records:
                    console.print(
                        Panel(
                            "[yellow]Kayıt bulunamadı.[/yellow]",
                            title="Uyarı",
                            border_style="yellow",
                        )
                    )
                    return

                total = res.get("total", len(records))
                console.print(
                    f"[green]Toplam kayıt: {total} (Gösterilen: {len(records)})[/green]\n"
                )

                first_item = records[0]
                all_keys = (
                    list(first_item.keys()) if isinstance(first_item, dict) else []
                )
                keys_to_show = all_keys[:6]

                table = Table(
                    show_header=True,
                    header_style="bold magenta",
                    border_style="cyan",
                    title=f"Datastore: [bold cyan]{resource_id}[/bold cyan]",
                    show_lines=True,
                )

                colors = ["cyan", "yellow", "green", "magenta", "blue", "red"]
                for idx, key in enumerate(keys_to_show):
                    table.add_column(str(key), style=colors[idx % len(colors)])

                for record in records:
                    if isinstance(record, dict):
                        row = [format_value(record.get(k)) for k in keys_to_show]
                        table.add_row(*row)

                console.print(table)

            except Exception as e:
                console.print(
                    Panel(
                        f"[bold red]Datastore hatası:[/bold red] {e}",
                        title="Hata",
                        border_style="red",
                    )
                )
                raise typer.Exit(1)

    run_async(_datastore())


if __name__ == "__main__":
    app()
