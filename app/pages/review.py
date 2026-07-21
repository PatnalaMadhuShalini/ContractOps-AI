import reflex as rx
from app.components.navbar import navbar
from app.components.sidebar import sidebar
from app.components.review.queue import queue_panel
from app.components.review.detail import detail_panel


def review_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            sidebar(active="contracts"),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        queue_panel(),
                        class_name="lg:col-span-4 xl:col-span-3",
                    ),
                    rx.el.div(
                        detail_panel(),
                        class_name="lg:col-span-8 xl:col-span-9",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-12 gap-6",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
            ),
            class_name="flex items-start flex-1 min-w-0 bg-gray-50",
        ),
        class_name="font-['Inter'] bg-gray-50 text-gray-900 antialiased min-h-screen",
    )
