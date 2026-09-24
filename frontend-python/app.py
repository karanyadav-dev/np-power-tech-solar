"""
NP POWER TECH SOLAR - Python + NiceGUI Frontend
Main application entry point.
"""

from nicegui import ui, app

# ---------- Import all pages (register routes) ----------
from pages.public import home            # noqa: F401  → /
from pages.public import about           # noqa: F401  → /about
from pages.public import services        # noqa: F401  → /services
from pages.public import products        # noqa: F401  → /products
from pages.public import projects        # noqa: F401  → /projects
from pages.public import contact         # noqa: F401  → /contact
from pages.public import get_quote       # noqa: F401  → /get-quote
from pages.public import solar_calculator  # noqa: F401  → /calculator
from pages.public import faq             # noqa: F401  → /faq
from pages.public import residential     # noqa: F401  → /residential
from pages.public import commercial      # noqa: F401  → /commercial
from pages.public import industrial      # noqa: F401  → /industrial
from pages.public import on_grid         # noqa: F401  → /on-grid
from pages.public import off_grid        # noqa: F401  → /off-grid
from pages.public import hybrid          # noqa: F401  → /hybrid
from pages.public import subsidy         # noqa: F401  → /subsidy
from pages.public import pincode_check   # noqa: F401  → /pincode-check
from pages.public import reviews         # noqa: F401  → /reviews
from pages.public import blog            # noqa: F401  → /blog
from pages.public import privacy_policy  # noqa: F401  → /privacy-policy
from pages.public import terms as terms_page  # noqa: F401  → /terms
from pages.auth import login             # noqa: F401  → /login
from pages.admin import dashboard        # noqa: F401  → /admin/dashboard


# ---------- Placeholder pages (polish pending) ----------
@ui.page("/site-survey")
def site_survey():
    from layouts.public_layout import public_layout
    public_layout(current_page="/site-survey")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Book Site Survey").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/warranty")
def warranty():
    from layouts.public_layout import public_layout
    public_layout(current_page="/warranty")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Warranty").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/amc")
def amc():
    from layouts.public_layout import public_layout
    public_layout(current_page="/amc")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("AMC Plans").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


@ui.page("/refund-policy")
def refund_policy():
    from layouts.public_layout import public_layout
    public_layout(current_page="/refund-policy")
    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-4"):
        ui.label("Refund Policy").classes("text-3xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")


# ---------- Config ----------
from config.settings import settings

# Enable storage for sessions
app.storage.secret = "dev-only-secret-change-in-production-abc123"


# ---------- Run ----------
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        title=settings.APP_TITLE,
        favicon="☀️",
        reload=False,
        show=False,
        storage_secret="dev-only-secret-change-in-production-abc123",
        language="en",
        viewport="width=device-width, initial-scale=1.0",
    )