import reflex as rx


def _metric_card(value: str, label: str, sub: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
            rx.el.span(
                label,
                class_name="text-[12px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            value,
            class_name="mt-4 text-4xl font-semibold tracking-tight text-gray-900 leading-none",
        ),
        rx.el.p(sub, class_name="mt-2 text-[13px] text-gray-600 leading-snug"),
        class_name="p-5 rounded-xl border border-gray-200 bg-white",
    )


def metrics() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "The ROI",
                    class_name="text-[12px] font-semibold uppercase tracking-[0.14em] text-blue-600",
                ),
                rx.el.h2(
                    "Numbers your CFO will actually like.",
                    class_name="mt-2 text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "Teams using ContractOps AI compress review cycles from weeks to hours and recover thousands of hours of legal capacity per year.",
                    class_name="mt-3 text-[15px] text-gray-600 max-w-2xl",
                ),
                class_name="max-w-3xl",
            ),
            rx.el.div(
                _metric_card(
                    "83%",
                    "Faster review",
                    "Median contract turnaround, from 9 days to 1.4.",
                    "gauge",
                ),
                _metric_card(
                    "4.2h",
                    "Saved per contract",
                    "Reviewer hours reclaimed on every negotiation.",
                    "timer",
                ),
                _metric_card(
                    "$1.8M",
                    "Avg. annual savings",
                    "For a 40-person legal team across all agreements.",
                    "trending-up",
                ),
                _metric_card(
                    "97%",
                    "Playbook accuracy",
                    "AI redlines match senior counsel on our benchmark suite.",
                    "shield-check",
                ),
                class_name="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
        ),
        class_name="border-b border-gray-200",
        id="product",
    )
