"""
NP POWER TECH SOLAR - Python + NiceGUI Frontend
Main application entry point.
"""

from nicegui import ui, app

# ============================================================
# Import all pages (register routes via @ui.page decorator)
# ============================================================

# ---------- Public pages ----------
from pages.public import home               # → /
from pages.public import about              # → /about
from pages.public import services           # → /services
from pages.public import products           # → /products
from pages.public import projects           # → /projects
from pages.public import contact            # → /contact
from pages.public import get_quote          # → /get-quote
from pages.public import solar_calculator   # → /calculator
from pages.public import faq                # → /faq
from pages.public import residential        # → /residential
from pages.public import commercial         # → /commercial
from pages.public import industrial         # → /industrial
from pages.public import on_grid            # → /on-grid
from pages.public import off_grid           # → /off-grid
from pages.public import hybrid             # → /hybrid
from pages.public import subsidy            # → /subsidy
from pages.public import pincode_check      # → /pincode-check
from pages.public import reviews            # → /reviews
from pages.public import blog               # → /blog
from pages.public import privacy_policy     # → /privacy-policy
from pages.public import terms as terms_page  # → /terms

# ---------- Auth pages ----------
from pages.auth import login                # → /login

# ---------- Admin pages ----------
from pages.admin import dashboard           # → /admin/dashboard


# ============================================================
# Placeholder pages (to be built in future phases)
# ============================================================

@ui.page("/site-survey")
def site_survey():
    from layouts.public_layout import public_layout
    public_layout(current_page="/site-survey")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Book Site Survey").classes("text-4xl font-bold")
        ui.label("Coming soon — full booking form will be added.").classes("text-gray-600")
        ui.button("Get Quote Instead", on_click=lambda: ui.navigate.to("/get-quote")).classes(
            "bg-yellow-500 text-white mt-4"
        )


@ui.page("/service")
def service():
    from layouts.public_layout import public_layout
    public_layout(current_page="/service")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Service Request").classes("text-4xl font-bold")
        ui.label("Coming soon — service ticket system.").classes("text-gray-600")


@ui.page("/amc")
def amc():
    from layouts.public_layout import public_layout
    public_layout(current_page="/amc")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("AMC Plans").classes("text-4xl font-bold")
        ui.label("Coming soon — AMC plans and renewals.").classes("text-gray-600")


@ui.page("/warranty")
def warranty():
    from layouts.public_layout import public_layout
    public_layout(current_page="/warranty")
    with ui.column().classes("w-full max-w-7xl mx-auto px-4 py-8 gap-4"):
        ui.label("Warranty Information").classes("text-4xl font-bold")
        ui.label("Coming soon — warranty lookup and registration.").classes("text-gray-600")


@ui.page("/refund-policy")
def refund_policy():
    from layouts.public_layout import public_layout
    public_layout(current_page="/refund-policy")
    with ui.column().classes("w-full max-w-4xl mx-auto px-4 py-8 gap-4"):
        ui.label("Refund Policy").classes("text-3xl font-bold")
        ui.label("This page will be updated soon. For any refund-related queries, please contact us.").classes("text-gray-600")
        ui.link("Contact Us →", "/contact").classes("text-yellow-600 font-semibold mt-2")


@ui.page("/solar-panels")
def solar_panels():
    from layouts.public_layout import public_layout
    public_layout(current_page="/solar-panels")
    ui.navigate.to("/products")


@ui.page("/solar-systems")
def solar_systems():
    from layouts.public_layout import public_layout
    public_layout(current_page="/solar-systems")
    ui.navigate.to("/products")


# ============================================================
# Config + Run
# ============================================================

from config.settings import settings

STORAGE_SECRET = "np-power-tech-solar-dev-secret-2025-change-in-prod"


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        title=settings.APP_TITLE,
        favicon="☀️",
        reload=False,
        show=False,
        storage_secret=STORAGE_SECRET,
    )