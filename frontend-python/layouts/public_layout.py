"""
NP POWER TECH SOLAR - Public Layout
Common layout for all public-facing pages.
"""

from nicegui import ui
from components.header import header
from components.footer import footer


def public_layout(current_page: str = "/"):
    """Apply public layout to the current page."""

    # Header (sticky top)
    header(current_page=current_page)

    # Main content area with top padding to clear the fixed header
    # (NiceGUI's ui.header is fixed; content needs spacing)
    with ui.column().classes("w-full pt-20"):
        with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-6") as main_container:
            # Child content renders here via context
            pass

    # Footer (normal flow at bottom)
    footer()

    return main_container