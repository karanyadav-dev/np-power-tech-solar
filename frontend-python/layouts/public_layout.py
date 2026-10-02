"""
NP POWER TECH SOLAR - Public Layout
Header + main content container + footer helper.
"""

from pathlib import Path
from nicegui import ui
from components.header import header
from components.footer import footer


CSS_FILE = Path(__file__).resolve().parent.parent / "static" / "theme.css"


def public_layout(current_page: str = "/"):
    """Apply public layout — header + main content container."""
    # CSS
    if CSS_FILE.exists():
        ui.add_css(CSS_FILE.read_text(encoding="utf-8"))

    # SEO meta
    ui.add_head_html('''
        <meta name="description" content="NP POWER TECH SOLAR - Complete solar solutions for homes, businesses, and industries.">
        <meta name="keywords" content="solar panels, solar installation, rooftop solar, PM Surya Ghar, solar subsidy">
        <meta property="og:title" content="NP POWER TECH SOLAR - Power Your Future with Solar">
        <meta property="og:type" content="website">
    ''')

    # Header
    header(current_page=current_page)

    # Main content container
    main_container = ui.column().classes(
        "w-full max-w-7xl mx-auto px-4 pt-24 pb-8 gap-6"
    )

    return main_container


def public_layout_footer():
    """Render footer — call at end of each page."""
    footer()