import reflex as rx


def auth_shell(title: str, subtitle: str, body: rx.Component) -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.a(
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
                class_name="flex items-center gap-2 justify-center mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        title,
                        class_name="text-[22px] font-semibold tracking-tight text-gray-900",
                    ),
                    rx.el.p(
                        subtitle,
                        class_name="mt-1 text-[13.5px] text-gray-600",
                    ),
                    class_name="mb-6",
                ),
                body,
                class_name="p-7 rounded-xl border border-gray-200 bg-white",
            ),
            class_name="w-full max-w-md",
        ),
        class_name="font-['Inter'] min-h-screen bg-gray-50 text-gray-900 antialiased flex items-center justify-center px-4 py-12",
    )
