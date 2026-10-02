"""
NP POWER TECH SOLAR - Python + NiceGUI Frontend
Main application entry point.
"""

from pathlib import Path
from nicegui import ui, app

# ---------- Import all pages (register routes) ----------
from pages.public import home          # noqa: F401  Ã¢â€ â€™ /
from pages.public import about          # noqa: F401  Ã¢â€ â€™ /about
from pages.public import services       # noqa: F401  Ã¢â€ â€™ /services
from pages.public import products       # noqa: F401  Ã¢â€ â€™ /products
from pages.public import projects       # noqa: F401  Ã¢â€ â€™ /projects
from pages.public import contact        # noqa: F401  Ã¢â€ â€™ /contact
from pages.public import get_quote      # noqa: F401  Ã¢â€ â€™ /get-quote
from pages.public import solar_calculator  # noqa: F401  Ã¢â€ â€™ /calculator
from pages.public import faq            # noqa: F401  Ã¢â€ â€™ /faq
from pages.public import residential     # noqa: F401  Ã¢â€ â€™ /residential
from pages.public import commercial      # noqa: F401  Ã¢â€ â€™ /commercial
from pages.public import industrial      # noqa: F401  Ã¢â€ â€™ /industrial
from pages.public import on_grid         # noqa: F401  Ã¢â€ â€™ /on-grid
from pages.public import off_grid        # noqa: F401  Ã¢â€ â€™ /off-grid
from pages.public import hybrid          # noqa: F401  Ã¢â€ â€™ /hybrid
from pages.public import subsidy         # noqa: F401  Ã¢â€ â€™ /subsidy
from pages.public import pincode_check   # noqa: F401  Ã¢â€ â€™ /pincode-check
from pages.public import reviews         # noqa: F401  Ã¢â€ â€™ /reviews
from pages.public import blog            # noqa: F401  Ã¢â€ â€™ /blog
from pages.public import privacy_policy    # noqa: F401  Ã¢â€ â€™ /privacy-policy
from pages.public import terms as terms_page  # noqa: F401  Ã¢â€ â€™ /terms
from pages.public import write_review    # noqa: F401  Ã¢â€ â€™ /write-review
from pages.public import quotation_wizard     # noqa: F401  Ã¢â€ â€™ /quotation-request
from pages.public import quotation_status     # noqa: F401  Ã¢â€ â€™ /quotation-status/{id}

from pages.auth import login            # noqa: F401  Ã¢â€ â€™ /login

from pages.admin import dashboard       # noqa: F401  Ã¢â€ â€™ /admin/dashboard
from pages.admin import products as admin_products  # noqa: F401
from pages.admin import product_form as admin_product_form  # noqa: F401
from pages.admin import leads as admin_leads  # noqa: F401
from pages.admin import customers as admin_customers  # noqa: F401
from pages.admin import reviews as admin_reviews  # noqa: F401
from pages.admin import uploads as admin_uploads  # noqa: F401
from pages.admin import settings as admin_settings_page  # noqa: F401
from pages.admin import quotation_review
from pages.admin import quotation_pricing  # noqa: F401


# ---------- Placeholder pages ----------
@ui.page("/site-survey")
def site_survey():
    from layouts.public_layout import public_layout, public_layout_footer
    container = public_layout(current_page="/site-survey")
    with container:
        ui.label("Book Site Survey").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")
    public_layout_footer()


@ui.page("/refund-policy")
def refund_policy():
    from layouts.public_layout import public_layout, public_layout_footer
    container = public_layout(current_page="/refund-policy")
    with container:
        ui.label("Refund Policy").classes("text-3xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")
    public_layout_footer()


@ui.page("/warranty")
def warranty():
    from layouts.public_layout import public_layout, public_layout_footer
    container = public_layout(current_page="/warranty")
    with container:
        ui.label("Warranty").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")
    public_layout_footer()


@ui.page("/amc")
def amc():
    from layouts.public_layout import public_layout, public_layout_footer
    container = public_layout(current_page="/amc")
    with container:
        ui.label("AMC Plans").classes("text-4xl font-bold")
        ui.label("Coming soon...").classes("text-gray-600")
    public_layout_footer()


# ---------- Config ----------
from config.settings import settings

# Enable storage for sessions
app.storage.secret = "dev-only-secret-change-in-production-abc123"


# ---------- Favicon ----------
LOGO_PATH = Path(__file__).resolve().parent / "assets" / "logo.png"


# ---------- Run ----------
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        title=settings.APP_TITLE,
        favicon=str(LOGO_PATH) if LOGO_PATH.exists() else "Ã¢Ëœâ‚¬Ã¯Â¸Â",
        reload=False,
        show=False,
        storage_secret="dev-only-secret-change-in-production-abc123",
        language="en",
        viewport="width=device-width, initial-scale=1.0",
    )