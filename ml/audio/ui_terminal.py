from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def render_terminal_ui(result, interval):
    status = Text()
    status.append("🧠 Prediction : ", style="bold")
    status.append(result["label"] + "\n", style="green" if result["label"]=="normal" else "red")

    status.append("📊 Confidence  : ")
    status.append(f"{result['confidence']:.3f}\n", style="cyan")

    status.append("⚠ Severity    : ")
    status.append(result["severity"] + "\n", style="yellow")

    status.append(f"⏱ Interval    : {interval} sec\n")

    console.clear()
    console.print(
        Panel(
            status,
            title="🛠 AutoFix Reality – Fan Monitor",
            border_style="blue"
        )
    )
