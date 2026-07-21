import reflex as rx


def _col(title: str, items: list[str]) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            title,
            class_name="text-[12px] font-semibold uppercase tracking-wider text-gray-500",
        ),
        rx.el.ul(
            *[
                rx.el.li(
                    rx.el.a(
                        i,
                        href="#",
                        class_name="text-[13.5px] font-medium text-gray-700 hover:text-blue-600 transition-colors",
                    ),
                )
                for i in items
            ],
            class_name="mt-4 flex flex-col gap-2.5",
        ),
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "file-check-2", class_name="h-4 w-4 text-white"
                            ),
                            class_name="h-7 w-7 rounded-md bg-blue-600 flex items-center justify-center",
                        ),
                        rx.el.span(
                            "ContractOps",
                            rx.el.span(" AI", class_name="text-blue-600"),
                            class_name="text-[15px] font-semibold text-gray-900 tracking-tight",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.p(
                        "The AI contract operations platform for modern legal teams.",
                        class_name="mt-4 text-[13.5px] text-gray-600 max-w-xs leading-relaxed",
                    ),
                    rx.el.div(
                        *[
                            rx.el.a(
                                rx.icon(i, class_name="h-4 w-4 text-gray-600"),
                                href="#",
                                class_name="h-8 w-8 rounded-md border border-gray-200 bg-white flex items-center justify-center hover:border-gray-300 transition-colors",
                            )
                            for i in ["linkedin", "twitter", "github"]
                        ],
                        class_name="mt-5 flex items-center gap-2",
                    ),
                    class_name="lg:col-span-2",
                ),
                _col(
                    "Product",
                    ["Overview", "Workflow", "Pricing", "Changelog", "Roadmap"],
                ),
                _col(
                    "Company",
                    ["About", "Customers", "Careers", "Press", "Contact"],
                ),
                _col(
                    "Resources",
                    ["Docs", "API", "Security", "Trust center", "Status"],
                ),
                class_name="grid grid-cols-2 lg:grid-cols-5 gap-8",
            ),
            rx.el.div(
                rx.el.p(
                    "© 2025 ContractOps AI, Inc.",
                    class_name="text-[12.5px] text-gray-500",
                ),
                rx.el.div(
                    rx.el.a(
                        "Terms",
                        href="#",
                        class_name="text-[12.5px] text-gray-500 hover:text-gray-800",
                    ),
                    rx.el.a(
                        "Privacy",
                        href="#",
                        class_name="text-[12.5px] text-gray-500 hover:text-gray-800",
                    ),
                    rx.el.a(
                        "DPA",
                        href="#",
                        class_name="text-[12.5px] text-gray-500 hover:text-gray-800",
                    ),
                    class_name="flex items-center gap-5",
                ),
                class_name="mt-12 pt-6 border-t border-gray-200 flex flex-col sm:flex-row items-center justify-between gap-3",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14",
        ),
        class_name="bg-white border-t border-gray-200",
    )
