import reflex as rx
from app.states.auth_state import AuthState


def user_menu_navbar() -> rx.Component:
    """Right-side navbar controls: auth-aware."""
    return rx.cond(
        AuthState.is_authenticated,
        rx.el.div(
            rx.cond(
                AuthState.is_platform_admin,
                rx.el.a(
                    rx.icon("shield-check", class_name="h-3.5 w-3.5"),
                    "Admin",
                    href="/admin",
                    class_name="hidden sm:inline-flex items-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-sm font-medium text-gray-800 hover:bg-gray-50 transition-colors",
                ),
                rx.el.a(
                    rx.icon("layout-grid", class_name="h-3.5 w-3.5"),
                    "Workspace",
                    href="/workspace",
                    class_name="hidden sm:inline-flex items-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-sm font-medium text-gray-800 hover:bg-gray-50 transition-colors",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        AuthState.current_user["initials"],
                        class_name="text-[10.5px] font-semibold text-blue-700",
                    ),
                    class_name="h-7 w-7 rounded-full bg-blue-100 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.current_user["name"],
                        class_name="text-[12.5px] font-semibold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        AuthState.current_user["email"],
                        class_name="text-[10.5px] text-gray-500 leading-tight",
                    ),
                    class_name="hidden md:flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-2 px-2 h-8 rounded-md border border-gray-200 bg-white",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="h-3.5 w-3.5"),
                on_click=AuthState.logout,
                class_name="inline-flex items-center justify-center h-8 w-8 rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 transition-colors",
                title="Sign out",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.div(
            rx.el.a(
                "Sign in",
                href="/login",
                class_name="hidden sm:inline-flex text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors",
            ),
            rx.el.a(
                "Book a demo",
                href="#cta",
                class_name="hidden sm:inline-flex items-center h-8 px-3 rounded-md border border-gray-200 bg-white text-sm font-medium text-gray-800 hover:bg-gray-50 transition-colors",
            ),
            rx.el.a(
                "Start free trial",
                rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                href="/signup",
                class_name="inline-flex items-center gap-1.5 h-8 px-3 rounded-md bg-blue-600 text-sm font-medium text-white hover:bg-blue-700 transition-colors",
            ),
            class_name="flex items-center gap-3",
        ),
    )
