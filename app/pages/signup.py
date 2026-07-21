import reflex as rx
from app.components.auth_shell import auth_shell
from app.states.auth_state import AuthState


def _field(
    label: str, name: str, placeholder: str, type_: str = "text", hint: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="text-[12px] font-semibold text-gray-700 mb-1.5",
        ),
        rx.el.input(
            name=name,
            type=type_,
            placeholder=placeholder,
            required=True,
            class_name="h-10 px-3 rounded-md border border-gray-200 bg-white text-[13.5px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
        ),
        rx.cond(
            hint != "",
            rx.el.p(hint, class_name="mt-1 text-[11.5px] text-gray-500"),
            rx.fragment(),
        ),
        class_name="flex flex-col",
    )


def _form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            _field("Full name", "name", "Alex Keller"),
            _field("Work email", "email", "alex@company.com", "email"),
            _field(
                "Company",
                "company",
                "Acme Legal",
                hint="A new workspace will be created for your team.",
            ),
            _field(
                "Password",
                "password",
                "At least 6 characters",
                "password",
            ),
            class_name="flex flex-col gap-4",
        ),
        rx.cond(
            AuthState.signup_error != "",
            rx.el.div(
                rx.icon(
                    "circle-alert",
                    class_name="h-3.5 w-3.5 text-red-600 mt-0.5 shrink-0",
                ),
                rx.el.p(
                    AuthState.signup_error,
                    class_name="text-[12.5px] text-red-700 leading-snug",
                ),
                class_name="mt-4 flex items-start gap-1.5 p-2.5 rounded-md border border-red-100 bg-red-50/70",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.p(
                "You'll start on the free ",
                rx.el.span(
                    "Starter plan", class_name="font-semibold text-gray-800"
                ),
                " — 50 contracts / month, up to 5 seats. No credit card required.",
                class_name="text-[12px] text-gray-600 leading-relaxed",
            ),
            class_name="mt-5 p-3 rounded-md border border-blue-100 bg-blue-50/40",
        ),
        rx.el.button(
            "Create workspace",
            rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
            type="submit",
            class_name="mt-5 inline-flex items-center justify-center gap-1.5 h-10 px-4 rounded-md bg-blue-600 text-[13.5px] font-semibold text-white hover:bg-blue-700 transition-colors w-full",
        ),
        rx.el.div(
            rx.el.p(
                "Already have an account?",
                class_name="text-[13px] text-gray-600",
            ),
            rx.el.a(
                "Sign in",
                href="/login",
                class_name="text-[13px] font-semibold text-blue-600 hover:text-blue-700",
            ),
            class_name="mt-5 flex items-center justify-center gap-1.5",
        ),
        on_submit=AuthState.signup,
    )


def signup_page() -> rx.Component:
    return auth_shell(
        "Create your workspace",
        "Get set up in 30 seconds — invite your team once you're in.",
        _form(),
    )
