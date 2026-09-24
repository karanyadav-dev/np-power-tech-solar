"""
NP POWER TECH SOLAR - Public Layout
Common layout for all public-facing pages.
"""

from pathlib import Path
from nicegui import ui
from components.header import header
from components.footer import footer


# Load custom CSS
CSS_FILE = Path(__file__).resolve().parent.parent / "static" / "theme.css"


def public_layout(current_page: str = "/"):
    """Apply public layout to the current page."""

    # Load custom CSS (once)
    if CSS_FILE.exists():
        ui.add_css(CSS_FILE.read_text(encoding="utf-8"))

    # SEO meta
    ui.add_head_html('''
        <meta name="description" content="NP POWER TECH SOLAR - Complete solar solutions for homes, businesses, and industries. Get free site survey, subsidy assistance, and expert installation.">
        <meta name="keywords" content="solar panels, solar installation, rooftop solar, PM Surya Ghar, solar subsidy, solar company India">
        <meta property="og:title" content="NP POWER TECH SOLAR - Power Your Future with Solar">
        <meta property="og:description" content="Save on electricity bills, reduce carbon footprint, and get government subsidies.">
        <meta property="og:type" content="website">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    ''')

    # Add global styles for sticky footer
    ui.add_head_html('''
        <style>
            body, html {
                min-height: 100vh;
                margin: 0;
                display: flex;
                flex-direction: column;
            }
            .nicegui-content {
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
        </style>
    ''')

    # Header (sticky top)
    header(current_page=current_page)

    # Main content area — grows to fill space, pushes footer down
    with ui.column().classes("w-full flex-grow"):
        with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-6 gap-6") as main_container:
            pass

    # Footer (bottom of page)
    footer()

    return main_container