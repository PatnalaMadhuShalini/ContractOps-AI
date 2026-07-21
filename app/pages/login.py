import reflex as rx
from app.components.auth_shell import auth_shell
from app.states.auth_state import AuthState


def _demo_row(label: str, email: str, password: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-[11px] font-semibold text-gray-500"),
        rx.el.p(
            email,
            class_name="text-[12px] font-mono text-gray-800 leading-tight",
        ),
        rx.el.p(
            password,
            class_name="text-[11.5px] font-mono text-gray-500 leading-tight",
        ),
        class_name="flex flex-col gap-0.5 p-2.5 rounded-md border border-gray-200 bg-gray-50/60",
    )


def _form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Work email",
                class_name="text-[12px] font-semibold text-gray-700 mb-1.5",
            ),
            rx.el.input(
                name="email",
                type="email",
                placeholder="you@company.com",
                required=True,
                default_value="alex@acmelegal.com",
                class_name="h-10 px-3 rounded-md border border-gray-200 bg-white text-[13.5px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
            ),
            class_name="flex flex-col mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="text-[12px] font-semibold text-gray-700",
                ),
                rx.el.a(
                    "Forgot?",
                    href="#",
                    class_name="ml-auto text-[12px] font-medium text-blue-600 hover:text-blue-700",
                ),
                class_name="flex items-center mb-1.5",
            ),
            rx.el.input(
                name="password",
                type="password",
                placeholder="••••••••",
                required=True,
                default_value="demo123",
                class_name="h-10 px-3 rounded-md border border-gray-200 bg-white text-[13.5px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
            ),
            class_name="flex flex-col mb-4",
        ),
        rx.cond(
            AuthState.login_error != "",
            rx.el.div(
                rx.icon(
                    "circle-alert",
                    class_name="h-3.5 w-3.5 text-red-600 mt-0.5 shrink-0",
                ),
                rx.el.p(
                    AuthState.login_error,
                    class_name="text-[12.5px] text-red-700 leading-snug",
                ),
                class_name="mb-4 flex items-start gap-1.5 p-2.5 rounded-md border border-red-100 bg-red-50/70",
            ),
            rx.fragment(),
        ),
        rx.el.button(
            "Sign in",
            rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
            type="submit",
            class_name="inline-flex items-center justify-center gap-1.5 h-10 px-4 rounded-md bg-blue-600 text-[13.5px] font-semibold text-white hover:bg-blue-700 transition-colors w-full",
        ),
        rx.el.div(
            rx.el.p(
                "Don't have an account?",
                class_name="text-[13px] text-gray-600",
            ),
            rx.el.a(
                "Create one",
                href="/signup",
                class_name="text-[13px] font-semibold text-blue-600 hover:text-blue-700",
            ),
            class_name="mt-5 flex items-center justify-center gap-1.5",
        ),
        rx.el.div(
            rx.el.p(
                "Demo accounts",
                class_name="text-[11px] font-semibold uppercase tracking-wider text-gray-500 mb-2",
            ),
            rx.el.div(
                _demo_row("Company owner", "alex@acmelegal.com", "demo123"),
                _demo_row("Platform admin", "admin@contractops.ai", "admin123"),
                class_name="grid grid-cols-1 sm:grid-cols-2 gap-2",
            ),
            class_name="mt-6 pt-5 border-t border-gray-100",
        ),
        on_submit=AuthState.login,
    )


def login_page() -> rx.Component:
    return auth_shell(
        "Welcome back",
        "Sign in to continue to your ContractOps workspace.",
        _form(),
    )
