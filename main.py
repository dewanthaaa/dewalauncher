from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
import questionary
import subprocess
from pathlib import Path
import time
import os

console = Console()

# === CONFIG ===
PROJECTS_DIR = Path.home() / "Projects"

EDITORS = {
    "VS Code": "code",
    "Vim": "vim",
    "Nano": "nano",
    "Kiro": "kiro"
}

# === BANNER ===


def show_banner():
    ascii_art = """
██████╗ ███████╗██╗    ██╗ █████╗     ██╗      █████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝██║    ██║██╔══██╗    ██║     ██╔══██╗██║   ██║████╗  ██║██╔════╝██║  ██║██╔════╝██╔══██╗
██║  ██║█████╗  ██║ █╗ ██║███████║    ██║     ███████║██║   ██║██╔██╗ ██║██║     ███████║█████╗  ██████╔╝
██║  ██║██╔══╝  ██║███╗██║██╔══██║    ██║     ██╔══██║██║   ██║██║╚██╗██║██║     ██╔══██║██╔══╝  ██╔══██╗
██████╔╝███████╗╚███╔███╔╝██║  ██║    ███████╗██║  ██║╚██████╔╝██║ ╚████║╚██████╗██║  ██║███████╗██║  ██║
╚═════╝ ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """
    content = Text(ascii_art, style="bold cyan", justify="center")
    content.append("\n DewaLauncher v1.0", style="bold white")
    content.append("\n Your personal dev environment starter\n", style="dim")

    console.print(Align.center(
        Panel(content, border_style="cyan", padding=(1, 4))))


# === CLEAR ===


def clear():
    os.system('clear')


# === LOADING ===


def loading():
    with Progress(
        TextColumn("[bold green]Booting DewaLauncher..."),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("", total=100)
        while not progress.finished:
            progress.advance(task, 1)
            time.sleep(0.03)  # atur kecepatan di sini

# === GET PROJECTS ===


def get_projects():
    # Ambil semua folder di direktori Projects
    return [f.name for f in PROJECTS_DIR.iterdir() if f.is_dir()]

# === SELECT PROJECTS ===


def select_project(projects):
    return questionary.select(
        "Pilih project yang mau lo buka:",
        choices=projects
    ).ask()

# === SELECT EDITOR ===


def select_editor():
    return questionary.select(
        "Pilih editor:",
        choices=list(EDITORS.keys())
    ).ask()

# === OPEN PROJECT ===


def open_project(project, editor):
    project_path = PROJECTS_DIR / project
    editor_cmd = EDITORS[editor]

    try:
        subprocess.run([editor_cmd, str(project_path)])
        console.print(f"[green]Opened {project} with {editor} 🚀[/green]")
    except FileNotFoundError:
        console.print(f"[red]Editor {editor} gak ditemukan cuy 😅[/red]")

# === MAIN ===


def main():
    loading()
    clear()
    show_banner()
    time.sleep(0.5)
    projects = get_projects()

    if not projects:
        console.print("[red]Folder project kosong 😢[/red]")
        return

    project = select_project(projects)
    editor = select_editor()

    open_project(project, editor)


if __name__ == "__main__":
    main()
