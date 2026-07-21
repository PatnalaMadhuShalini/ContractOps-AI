import reflex as rx


def cta() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Ready to move contracts at the speed of revenue?",
                        class_name="text-3xl sm:text-4xl font-semibold tracking-tight text-white max-w-2xl leading-tight",
                    ),
                    rx.el.p(
                        "Get set up in 48 hours. Bring one contract or a thousand — we'll review it before your next stand-up.",
                        class_name="mt-3 text-[15px] text-blue-100 max-w-xl",
                    ),
                    class_name="max-w-2xl",
                ),
                rx.el.div(
                    rx.el.a(
                        "Start free trial",
                        rx.icon("arrow-right", class_name="h-4 w-4"),
                        href="/signup",
                        class_name="inline-flex items-center gap-1.5 h-11 px-5 rounded-md bg-white text-sm font-semibold text-blue-700 hover:bg-blue-50 transition-colors",
                    ),
                    rx.el.a(
                        "Book a demo",
                        href="#contact-sales",
                        class_name="inline-flex items-center h-11 px-5 rounded-md border border-white/25 bg-transparent text-sm font-semibold text-white hover:bg-white/10 transition-colors",
                    ),
                    class_name="flex flex-wrap items-center gap-2.5 lg:justify-end",
                ),
                class_name="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-8",
            ),
            class_name="max-w-7xl mx-auto px-6 sm:px-10 py-14 rounded-2xl bg-blue-600 border border-blue-700",
        ),
        class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16",
        id="cta",
    )
