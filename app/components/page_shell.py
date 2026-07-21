import reflex as rx
from app.components.navbar import navbar
from app.components.sidebar import sidebar


def page_shell(active: str, content: rx.Component) -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            sidebar(active=active),
            rx.el.div(
                rx.el.div(
                    content,
                    class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
                ),
                class_name="flex-1 min-w-0 bg-gray-50",
            ),
            class_name="flex items-start",
        ),
        class_name="font-['Inter'] bg-gray-50 text-gray-900 antialiased min-h-screen",
    )


def page_header(
    title: str,
    subtitle: str,
    actions: rx.Component | None = None,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                title,
                class_name="text-2xl sm:text-3xl font-semibold tracking-tight text-gray-900",
            ),
            rx.el.p(
                subtitle,
                class_name="mt-1 text-[14px] text-gray-600",
            ),
            class_name="flex flex-col min-w-0",
        ),
        rx.cond(
            actions != None,
            rx.el.div(actions, class_name="flex items-center gap-2 flex-wrap"),
            rx.fragment(),
        ),
        class_name="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-6",
    )


def stat_card(
    label: str, value: rx.Component | str, sub: rx.Component | str, icon: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
            rx.el.span(
                label,
                class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            value,
            class_name="mt-3 text-3xl font-semibold tracking-tight text-gray-900 leading-none",
        ),
        rx.el.p(sub, class_name="mt-2 text-[12.5px] text-gray-600"),
        class_name="p-4 rounded-xl border border-gray-200 bg-white",
    )
