"""
NP POWER TECH SOLAR - Blog Listing
"""

from nicegui import ui
from layouts.public_layout import public_layout


# Placeholder blog posts (to be fetched from API/DB in later phase)
PLACEHOLDER_POSTS = [
    {
        "title": "PM Surya Ghar Yojana: Complete Guide 2025",
        "excerpt": "Everything you need to know about the government's flagship solar subsidy scheme — eligibility, application process, and subsidy amounts.",
        "category": "Subsidy",
        "date": "2025-09-15",
        "read_time": "5 min read",
    },
    {
        "title": "5 Reasons to Install Solar in 2025",
        "excerpt": "Rising electricity costs, falling solar prices, and government incentives make 2025 the best year to go solar. Here's why.",
        "category": "Solar Basics",
        "date": "2025-09-10",
        "read_time": "4 min read",
    },
    {
        "title": "On-Grid vs Off-Grid vs Hybrid: Which is Right for You?",
        "excerpt": "Confused between solar system types? We break down the pros, cons, and ideal use cases for each.",
        "category": "Guides",
        "date": "2025-09-05",
        "read_time": "6 min read",
    },
    {
        "title": "How to Calculate Your Solar System Size",
        "excerpt": "A simple 3-step method to figure out exactly how much solar capacity your home or business needs.",
        "category": "Guides",
        "date": "2025-08-28",
        "read_time": "5 min read",
    },
    {
        "title": "Solar Panel Maintenance: 7 Tips for Long Life",
        "excerpt": "Solar panels need minimal care, but these simple habits will keep them performing at peak efficiency for 25+ years.",
        "category": "Maintenance",
        "date": "2025-08-20",
        "read_time": "4 min read",
    },
    {
        "title": "Understanding Net Metering in India",
        "excerpt": "What is net metering, how does it work, and how much can you save? A complete guide for residential solar owners.",
        "category": "Guides",
        "date": "2025-08-12",
        "read_time": "5 min read",
    },
]


@ui.page("/blog")
def blog_page():
    public_layout(current_page="/blog")

    with ui.column().classes("w-full max-w-6xl mx-auto px-4 py-8 gap-6"):
        ui.label("Solar Blog").classes("text-4xl font-bold text-gray-900")
        ui.label("Learn about solar energy, subsidies, and industry insights.").classes("text-gray-600")

        # Category filters
        with ui.row().classes("gap-2 flex-wrap"):
            categories = ["All", "Subsidy", "Solar Basics", "Guides", "Maintenance"]
            for c in categories:
                ui.chip(c, color="yellow-100").classes("cursor-pointer text-yellow-800")

        # Posts grid
        with ui.row().classes("w-full gap-4 flex-wrap"):
            for post in PLACEHOLDER_POSTS:
                with ui.card().classes("w-full md:w-96 p-5 hover:shadow-lg transition-shadow cursor-pointer"):
                    ui.chip(post["category"], color="yellow-100").classes("text-yellow-800 text-xs")
                    ui.label(post["title"]).classes("text-lg font-bold text-gray-900 mt-3")
                    ui.label(post["excerpt"]).classes("text-gray-600 text-sm mt-2")
                    ui.separator()
                    with ui.row().classes("w-full justify-between text-xs text-gray-500 mt-2"):
                        ui.label(post["date"])
                        ui.label(post["read_time"])

        # CTA
        ui.separator()
        with ui.card().classes("w-full bg-yellow-50 p-6 items-center"):
            ui.label("Have Questions About Solar?").classes("text-xl font-bold")
            ui.label("Our experts are happy to help.").classes("text-gray-600 mt-2")
            ui.button("Talk to Expert", on_click=lambda: ui.navigate.to("/contact")).classes(
                "bg-yellow-500 text-white mt-3"
            )