import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .models import UserProfile
from .questionnaire import run_interactive_questionnaire
from .recommender import recommend
from .persistence import save_run

app = typer.Typer(add_completion=False, help="🧭 Orientador de carreras (CLI)")
console = Console()


@app.command("interactive")
def interactive(
    top_k: int = typer.Option(5, "--top", min=1, max=10, help="Cantidad de recomendaciones"),
    save: bool = typer.Option(True, "--save/--no-save", help="Guardar resultado en /runs"),
):
    """Ejecuta el cuestionario interactivo y recomienda carreras."""
    user = run_interactive_questionnaire()
    recs = recommend(user, top_k=top_k)

    _print_recs(recs)

    if save:
        path = save_run(user, recs)
        console.print(f"\n💾 Guardado en: [bold]{path}[/bold]")


@app.command("recommend-career")
def recommend_career(
    interes: list[str] = typer.Option([], "--interes", help="Intereses (repetible)"),
    habilidad: list[str] = typer.Option([], "--habilidad", help="Habilidades (repetible)"),
    matematica: int = typer.Option(2, "--matematica", min=1, max=3, help="1=baja 2=media 3=alta"),
    comunicacion: int = typer.Option(2, "--comunicacion", min=1, max=3, help="1..3"),
    creatividad: int = typer.Option(2, "--creatividad", min=1, max=3, help="1..3"),
    personas: bool = typer.Option(False, "--personas", help="Te gusta trabajar con personas"),
    equipo: int = typer.Option(2, "--equipo", min=1, max=3, help="Preferencia por trabajo en equipo (1..3)"),
    top_k: int = typer.Option(5, "--top", min=1, max=10, help="Cantidad de recomendaciones"),
    save: bool = typer.Option(False, "--save/--no-save", help="Guardar resultado en /runs"),
):
    """Recomienda carreras pasando parámetros por flags."""
    user = UserProfile(
        interests=interes,
        skills=habilidad,
        math=matematica,
        communication=comunicacion,
        creativity=creatividad,
        people_work=1 if personas else 0,
        teamwork=equipo,
    )

    recs = recommend(user, top_k=top_k)
    _print_recs(recs)

    if save:
        path = save_run(user, recs)
        console.print(f"\n💾 Guardado en: [bold]{path}[/bold]")


def _print_recs(recs):
    for r in recs:
        body_lines = []

        header = Text(f"{r.career}", style="bold")
        header.append(f"  (score: {r.score:.2f})", style="dim")

        if r.reasons:
            body_lines.append("✅ Por qué encaja")
            body_lines.extend([f"- {x}" for x in r.reasons])

        if r.cautions:
            if body_lines:
                body_lines.append("")
            body_lines.append("⚠️ A considerar")
            body_lines.extend([f"- {x}" for x in r.cautions])

        console.print(Panel("\n".join(body_lines) if body_lines else "Sin detalles.", title=header))


def main():
    app()


if __name__ == "__main__":
    main()
