import subprocess
from pathlib import Path

from rich import print
from rich.markup import escape

if __name__ == "__main__":

    svgPath = Path("temp-icon.svg")

    svgFiles = list(Path(__file__).parent.glob("*.svg"))

    if len(svgFiles) == 1:

        svgPath = svgFiles[0]

    elif len(svgFiles) > 1:

        raise ValueError(
            f"[red]Multiple SVG files found:[/red] {', '.join(str(f) for f in svgFiles)}"
        )

    else:

        pass

    outputPath = svgPath.with_suffix(".png")

    size = 16
    density = 300
    background = "none"

    if not svgPath.is_file():

        raise FileNotFoundError(
            f"[red]File not found:[/red] [bold yellow]{svgPath.absolute()}[/bold yellow]"
        )

    if svgPath.suffix != ".svg":

        raise FileNotFoundError(
            f"[red]Invalid file type (not .svg):[/red] [bold yellow]{svgPath.absolute()}[/bold yellow]"
        )

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

    print(
        f"[green]✅ Rasterized[/green] [bold cyan]{svgPath.name}[/bold cyan] "
        f"→ [bold magenta]{outputPath.name}[/bold magenta] [dim]({size}px)[/dim]"
    )
