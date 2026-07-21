import reflex as rx


def _feature(icon: str, title: str, body: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
            class_name="inline-flex items-center justify-center h-8 w-8 rounded-md bg-blue-50 border border-blue-100",
        ),
        rx.el.h3(
            title, class_name="mt-4 text-[15px] font-semibold text-gray-900"
        ),
        rx.el.p(
            body,
            class_name="mt-1.5 text-[13.5px] text-gray-600 leading-relaxed",
        ),
        class_name="p-5 rounded-xl border border-gray-200 bg-white",
    )


def _quote_card() -> rx.Component:
    return rx.el.div(
        rx.icon("quote", class_name="h-5 w-5 text-blue-600"),
        rx.el.p(
            "We cut MSA turnaround from 11 days to under 24 hours. Our GC calls it the highest-leverage tool she's adopted in a decade.",
            class_name="mt-4 text-lg font-medium text-gray-900 leading-snug",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "SR", class_name="text-[11px] font-semibold text-blue-700"
                ),
                class_name="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.p(
                    "Sarah Reeves",
                    class_name="text-[13px] font-semibold text-gray-900 leading-tight",
                ),
                rx.el.p(
                    "VP Legal Ops · Northwind",
                    class_name="text-[11.5px] text-gray-500 leading-tight",
                ),
                class_name="flex flex-col",
            ),
            class_name="mt-6 flex items-center gap-2.5",
        ),
        class_name="p-6 rounded-xl border border-gray-200 bg-white",
    )


def features() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Built for legal teams",
                    class_name="text-[12px] font-semibold uppercase tracking-[0.14em] text-blue-600",
                ),
                rx.el.h2(
                    "Every capability your review team wishes they had.",
                    class_name="mt-2 text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900 max-w-3xl",
                ),
                class_name="max-w-3xl",
            ),
            rx.el.div(
                _feature(
                    "book-open",
                    "Playbook-native review",
                    "Codify your standards once. Every contract is scored against them with citations and confidence.",
                ),
                _feature(
                    "scan-search",
                    "Clause extraction",
                    "Auto-extract 120+ clause types across MSAs, NDAs, DPAs, SOWs and vendor paper.",
                ),
                _feature(
                    "git-pull-request",
                    "One-click redlines",
                    "Insert fallback language from your library — tracked changes ready for counterparty.",
                ),
                _feature(
                    "shield-check",
                    "Deviation-based approvals",
                    "Only escalate what breaks your playbook. Everything else auto-approves.",
                ),
                _feature(
                    "chart-line",
                    "Obligation & renewal tracking",
                    "Extract dates, notice periods, and commitments. Get pinged before you're stuck.",
                ),
                _feature(
                    "lock",
                    "SOC 2 + private tenancy",
                    "Enterprise-grade security. Your data never trains our models. EU + US regions.",
                ),
                class_name="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4",
            ),
            rx.el.div(
                _quote_card(),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Time to first value",
                            class_name="text-[12px] font-semibold uppercase tracking-wider text-gray-500",
                        ),
                        rx.el.p(
                            "48 hours",
                            class_name="mt-3 text-3xl font-semibold tracking-tight text-gray-900",
                        ),
                        rx.el.p(
                            "From kickoff to first AI-reviewed contract, with your playbook.",
                            class_name="mt-1.5 text-[13px] text-gray-600",
                        ),
                        class_name="p-5 rounded-xl border border-gray-200 bg-white",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Integrations",
                            class_name="text-[12px] font-semibold uppercase tracking-wider text-gray-500",
                        ),
                        rx.el.div(
                            *[
                                rx.el.div(
                                    rx.icon(
                                        i, class_name="h-4 w-4 text-gray-600"
                                    ),
                                    class_name="h-9 w-9 rounded-md border border-gray-200 bg-white flex items-center justify-center",
                                )
                                for i in [
                                    "mail",
                                    "slack",
                                    "chrome",
                                    "database",
                                    "cloud",
                                    "webhook",
                                ]
                            ],
                            class_name="mt-3 flex flex-wrap gap-2",
                        ),
                        rx.el.p(
                            "Salesforce, Google Drive, DocuSign, Ironclad, Slack, and 40+ more.",
                            class_name="mt-3 text-[13px] text-gray-600",
                        ),
                        class_name="p-5 rounded-xl border border-gray-200 bg-white",
                    ),
                    class_name="flex flex-col gap-4",
                ),
                class_name="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-4",
                id="customers",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
        ),
        class_name="border-b border-gray-200",
    )
