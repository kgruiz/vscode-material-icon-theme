import subprocess
from pathlib import Path

from rich.console import Console
from rich.markup import escape

console = Console()

if __name__ == "__main__":

    svgPath = Path("pytorch.svg")

    svgFiles = list(Path(__file__).parent.glob("*.svg"))

    if not svgPath.exists():

        if len(svgFiles) == 1:

            svgPath = svgFiles[0]

        elif len(svgFiles) > 1:

            console.print(
                f"[red]Multiple SVG files found:[/red] {', '.join(str(f) for f in svgFiles)}"
            )

            raise ValueError(
                f"Multiple SVG files found: {', '.join(str(f) for f in svgFiles)}"
            )

        else:

            console.print(
                f"[red]No SVG files found in directory:[/red] {Path(__file__).parent}"
            )

            raise FileNotFoundError(
                f"No SVG files found in directory: {Path(__file__).parent}"
            )

    outputPath = svgPath.with_suffix(".png")

    size = 16
    density = 300
    background = "none"

    if not svgPath.is_file():

        console.print(
            f"[red]File not found:[/red] [bold yellow]{svgPath.absolute()}[/bold yellow]"
        )

        raise FileNotFoundError(f"File not found: {svgPath.absolute()}")

    if svgPath.suffix != ".svg":

        console.print(
            f"[red]Invalid file type (not .svg):[/red] [bold yellow]{svgPath.absolute()}[/bold yellow]"
        )

        raise FileNotFoundError(f"Invalid file type (not .svg): {svgPath.absolute()}")

    result = subprocess.run(
        [
            "magick",
            "-background",
            background,
            "-density",
            str(density),
            str(svgPath),
            "-resize",
            f"{size}x{size}",
            str(outputPath),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:

        raise RuntimeError(
            f"[red]ImageMagick failed:[/red]\n[dim]{escape(result.stderr)}[/dim]"
        )

    console.print(
        f"[green]✅ Rasterized[/green] [bold cyan]{svgPath.name}[/bold cyan] "
        f"→ [bold magenta]{outputPath.name}[/bold magenta] [dim]({size}px)[/dim]"
    )
