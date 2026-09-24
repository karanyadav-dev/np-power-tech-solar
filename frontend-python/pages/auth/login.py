"""
NP POWER TECH SOLAR - Login Page
"""

from nicegui import ui, app
from services.auth_service import auth_service
from config.settings import settings


@ui.page("/login")
def login_page():
    with ui.column().classes("w-full min-h-screen items-center justify-center bg-gray-100"):
        with ui.card().classes("w-96 p-8 gap-4"):
            with ui.row().classes("items-center gap-2 justify-center"):
                ui.icon("solar_power", size="2rem").classes("text-yellow-500")
                ui.label(settings.APP_TITLE).classes("text-lg font-bold")

            ui.label("Admin Login").classes("text-2xl font-bold text-center mt-2")

            email = ui.input("Email").classes("w-full")
            password = ui.input("Password", password=True, password_toggle_button=True).classes("w-full")

            result = ui.label("").classes("text-sm")

            def do_login():
                if not email.value or not password.value:
                    result.set_text("Please enter email and password.")
                    result.classes("text-red-600")
                    return

                resp = auth_service.login(email.value, password.value)

                if resp.get("success"):
                    # Store token in app storage (session)
                    token = resp["data"]["accessToken"]
                    app.storage.user["access_token"] = token
                    app.storage.user["user"] = resp["data"]["user"]
                    ui.navigate.to("/admin/dashboard")
                else:
                    err = resp.get("error", {}).get("message", "Login failed.")
                    result.set_text(f"❌ {err}")
                    result.classes("text-red-600")

            ui.button("Login", on_click=do_login).classes(
                "bg-yellow-500 text-white w-full mt-2"
            )

            ui.link("← Back to Home", "/").classes("text-center text-sm text-gray-500 mt-2")