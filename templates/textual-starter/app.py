"""TUI Starter — Textual (Python)

A clean starter template for a sidebar + content TUI with keyboard navigation.
Run: textual run app.py --dev
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, ListView, ListItem
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive


class NavItem(ListItem):
    """A navigation sidebar item."""

    def __init__(self, label: str, icon: str = "") -> None:
        super().__init__()
        self.nav_label = label
        self.nav_icon = icon


class Sidebar(Vertical):
    """Navigation sidebar component."""

    DEFAULT_CSS = """
    Sidebar {
        width: 24;
        dock: left;
        padding: 1 2;
        border-right: solid $border;
        background: $surface;
    }

    Sidebar .nav-header {
        color: $text-muted;
        text-style: bold;
        margin-bottom: 1;
    }

    Sidebar ListItem {
        padding: 0 1;
        height: 3;
    }

    Sidebar ListItem:hover {
        background: $boost;
    }

    Sidebar ListView:focus > ListItem.--highlight {
        background: $accent 20%;
        text-style: bold;
        color: $accent;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("NAVIGATION", classes="nav-header")
        with ListView(id="nav-list"):
            yield NavItem("Dashboard", "▸")
            yield NavItem("Records", "")
            yield NavItem("Logs", "")
            yield NavItem("Settings", "")


class ContentPanel(Vertical):
    """Main content area that responds to navigation."""

    DEFAULT_CSS = """
    ContentPanel {
        padding: 2 3;
        height: 1fr;
    }

    ContentPanel .title {
        text-style: bold;
        margin-bottom: 1;
    }

    ContentPanel .subtitle {
        color: $text-muted;
        margin-bottom: 2;
    }
    """

    active_section: reactive[str] = reactive("Dashboard")

    def compose(self) -> ComposeResult:
        yield Static(self.active_section, id="content-title", classes="title")
        yield Static(
            "Select an item from the sidebar, or press ? for help.",
            id="content-subtitle",
            classes="subtitle",
        )

    def watch_active_section(self, section: str) -> None:
        title = self.query_one("#content-title", Static)
        title.update(section)


class TUIStarter(App):
    """A polished TUI starter with sidebar navigation and content area."""

    CSS_PATH = None  # Styles are inline for portability

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("question_mark", "toggle_help", "Help", key_display="?"),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Sidebar()
            yield ContentPanel()
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, NavItem):
            content = self.query_one(ContentPanel)
            content.active_section = event.item.nav_label
