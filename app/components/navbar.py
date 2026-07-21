import reflex as rx
from app.states.landing_state import LandingState
from app.components.user_menu import user_menu_navbar


def _nav_link(label: str, href: str) -> rx.Component:
    return rx.el.a(
        label,
        href=href,
        class_name="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors",
    )


def _logo() -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon("file-check-2", class_name="h-4 w-4 text-white"),
            class_name="h-7 w-7 rounded-md bg-blue-600 flex items-center justify-center",
        ),
        rx.el.span(
            "ContractOps",
            rx.el.span(" AI", class_name="text-blue-600"),
            class_name="text-[15px] font-semibold text-gray-900 tracking-tight",
        ),
        href="/",
        class_name="flex items-center gap-2",
    )


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                _logo(),
                rx.el.nav(
                    _nav_link("Product", "#product"),
                    _nav_link("Workflow", "#workflow"),
                    _nav_link("Pricing", "#pricing"),
                    _nav_link("Customers", "#customers"),
                    _nav_link("Contact", "#contact-sales"),
                    _nav_link("Docs", "#"),
                    class_name="hidden md:flex items-center gap-7 ml-10",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                user_menu_navbar(),
                rx.el.button(
                    rx.icon(
                        rx.cond(LandingState.mobile_nav_open, "x", "menu"),
                        class_name="h-5 w-5 text-gray-700",
                    ),
                    on_click=LandingState.toggle_mobile_nav,
                    class_name="md:hidden inline-flex items-center justify-center h-9 w-9 rounded-md border border-gray-200 bg-white",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between",
        ),
        rx.cond(
            LandingState.mobile_nav_open,
            rx.el.div(
                rx.el.div(
                    _nav_link("Product", "#product"),
                    _nav_link("Workflow", "#workflow"),
                    _nav_link("Pricing", "#pricing"),
                    _nav_link("Customers", "#customers"),
                    _nav_link("Contact", "#contact-sales"),
                    _nav_link("Docs", "#"),
                    class_name="flex flex-col gap-3 px-4 py-4",
                ),
                class_name="md:hidden border-t border-gray-200 bg-white",
            ),
            rx.fragment(),
        ),
        class_name="sticky top-0 z-40 border-b border-gray-200 bg-white/80 backdrop-blur-sm",
    )
