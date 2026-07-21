import reflex as rx


def _logo_pill(name: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-4 w-4 text-gray-500"),
        rx.el.span(
            name,
            class_name="text-[13.5px] font-semibold text-gray-500 tracking-tight",
        ),
        class_name="inline-flex items-center gap-2",
    )


def logos() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.p(
                "Trusted by legal and revenue teams at fast-moving companies",
                class_name="text-center text-[12px] font-semibold uppercase tracking-[0.14em] text-gray-500",
            ),
            rx.el.div(
                _logo_pill("Northwind", "wind"),
                _logo_pill("Acme Corp", "hexagon"),
                _logo_pill("Globex", "globe"),
                _logo_pill("Initech", "cpu"),
                _logo_pill("Umbrella", "umbrella"),
                _logo_pill("Vandelay", "building-2"),
                _logo_pill("Soylent", "leaf"),
                class_name="mt-7 flex flex-wrap items-center justify-center gap-x-10 gap-y-4",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
        ),
        class_name="border-b border-gray-200 bg-white",
    )
