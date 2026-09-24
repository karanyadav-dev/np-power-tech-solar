"""
NP POWER TECH SOLAR - Public Layout
Common layout for all public-facing pages.
"""

from nicegui import ui
from components.header import header
from components.footer import footer


def public_layout(current_page: str = "/"):
    """Apply public layout to the current page."""

    # Header (sticky at top)
    header(current_page=current_page)

    # Main content area with top padding for fixed header
    with ui.column().classes("w-full pt-20 min-h-screen"):
        container = ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-6")
        # Child content renders inside `container` via context
        pass

    # Footer at bottom (normal flow)
    footer()

    return container