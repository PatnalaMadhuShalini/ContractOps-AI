import reflex as rx


def _pill() -> rx.Component:
    return rx.el.a(
        rx.el.span(
            "New",
            class_name="inline-flex items-center h-5 px-1.5 rounded bg-blue-600 text-[10px] font-semibold uppercase tracking-wider text-white",
        ),
        rx.el.span(
            "Playbook v2 — bulk redlines with a single click",
            class_name="text-[12.5px] font-medium text-gray-700",
        ),
        rx.icon("arrow-right", class_name="h-3.5 w-3.5 text-gray-500"),
        href="#",
        class_name="inline-flex items-center gap-2 h-7 pl-1 pr-2.5 rounded-full border border-gray-200 bg-white hover:border-gray-300 transition-colors",
    )


def _mock_doc_row(
    title: str, tag: str, tag_cls: str, risk: str, risk_cls: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("file-text", class_name="h-4 w-4 text-gray-500 shrink-0"),
            rx.el.div(
                rx.el.p(
                    title,
                    class_name="text-[13px] font-medium text-gray-900 leading-tight truncate",
                ),
                rx.el.p(
                    "Updated 2m ago · Alex Keller",
                    class_name="text-[11px] text-gray-500 leading-tight truncate",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-center gap-2.5 min-w-0 flex-1",
        ),
        rx.el.span(
            tag,
            class_name=f"hidden sm:inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold uppercase tracking-wider {tag_cls}",
        ),
        rx.el.span(
            risk,
            class_name=f"inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold uppercase tracking-wider {risk_cls}",
        ),
        class_name="flex items-center gap-2 px-3 h-11 border-b border-gray-100 last:border-b-0",
    )


def _hero_mock() -> rx.Component:
    return rx.el.div(
        # Window chrome
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="h-2.5 w-2.5 rounded-full bg-gray-200"),
                rx.el.div(class_name="h-2.5 w-2.5 rounded-full bg-gray-200"),
                rx.el.div(class_name="h-2.5 w-2.5 rounded-full bg-gray-200"),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.div(
                rx.icon("search", class_name="h-3 w-3 text-gray-400"),
                rx.el.span(
                    "app.contractops.ai / contracts",
                    class_name="text-[11.5px] font-medium text-gray-500",
                ),
                class_name="hidden sm:flex items-center gap-1.5 h-6 px-2.5 rounded-md bg-gray-100 border border-gray-200",
            ),
            rx.el.div(class_name="w-14"),
            class_name="flex items-center justify-between px-3 h-10 border-b border-gray-200 bg-gray-50",
        ),
        # Body
        rx.el.div(
            # Left column: doc queue
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Contract queue",
                        class_name="text-[12px] font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        "24",
                        class_name="ml-auto text-[11px] font-medium text-gray-500",
                    ),
                    class_name="flex items-center px-3 h-9 border-b border-gray-200",
                ),
                _mock_doc_row(
                    "Acme MSA — Vendor v3.docx",
                    "MSA",
                    "bg-blue-50 text-blue-700",
                    "Medium",
                    "bg-amber-50 text-amber-700",
                ),
                _mock_doc_row(
                    "Northwind NDA — mutual.pdf",
                    "NDA",
                    "bg-violet-50 text-violet-700",
                    "Low",
                    "bg-emerald-50 text-emerald-700",
                ),
                _mock_doc_row(
                    "Globex DPA — 2024 addendum",
                    "DPA",
                    "bg-slate-100 text-slate-700",
                    "High",
                    "bg-red-50 text-red-700",
                ),
                _mock_doc_row(
                    "Initech SOW — Q4 renewal",
                    "SOW",
                    "bg-blue-50 text-blue-700",
                    "Low",
                    "bg-emerald-50 text-emerald-700",
                ),
                _mock_doc_row(
                    "Umbrella SaaS agreement",
                    "SaaS",
                    "bg-blue-50 text-blue-700",
                    "Medium",
                    "bg-amber-50 text-amber-700",
                ),
                class_name="border-r border-gray-200 min-w-0",
            ),
            # Right column: review panel
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Acme MSA — Vendor v3",
                            class_name="text-[13px] font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "Reviewing 42 clauses · Playbook: Enterprise SaaS",
                            class_name="text-[11px] text-gray-500",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.span(
                        rx.icon("sparkles", class_name="h-3 w-3"),
                        "AI reviewed",
                        class_name="inline-flex items-center gap-1 h-6 px-2 rounded-md bg-blue-50 text-blue-700 text-[11px] font-semibold ml-auto",
                    ),
                    class_name="flex items-center gap-2 px-3 h-12 border-b border-gray-200",
                ),
                rx.el.div(
                    # Risk summary card
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Risk score",
                                class_name="text-[11px] font-medium text-gray-500",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "62",
                                    class_name="text-2xl font-semibold text-gray-900 leading-none",
                                ),
                                rx.el.span(
                                    "/ 100",
                                    class_name="text-[11px] text-gray-500",
                                ),
                                class_name="flex items-baseline gap-1 mt-1",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="h-1.5 flex-1 rounded-full bg-emerald-400"
                            ),
                            rx.el.div(
                                class_name="h-1.5 flex-1 rounded-full bg-amber-400"
                            ),
                            rx.el.div(
                                class_name="h-1.5 flex-1 rounded-full bg-amber-400"
                            ),
                            rx.el.div(
                                class_name="h-1.5 flex-1 rounded-full bg-gray-200"
                            ),
                            rx.el.div(
                                class_name="h-1.5 flex-1 rounded-full bg-gray-200"
                            ),
                            class_name="flex items-center gap-1 mt-3",
                        ),
                        class_name="p-3 rounded-lg border border-gray-200 bg-white",
                    ),
                    # Clauses
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-3.5 w-3.5 text-amber-600 mt-0.5 shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Limitation of liability capped at 6 months fees",
                                    class_name="text-[12.5px] font-medium text-gray-900 leading-snug",
                                ),
                                rx.el.p(
                                    "Playbook requires 12 months. Suggest counter with fallback clause.",
                                    class_name="text-[11.5px] text-gray-500 leading-snug mt-0.5",
                                ),
                                class_name="flex flex-col min-w-0",
                            ),
                            class_name="flex items-start gap-2 p-2.5 rounded-md border border-amber-100 bg-amber-50/50",
                        ),
                        rx.el.div(
                            rx.icon(
                                "circle-check",
                                class_name="h-3.5 w-3.5 text-emerald-600 mt-0.5 shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Governing law: Delaware",
                                    class_name="text-[12.5px] font-medium text-gray-900 leading-snug",
                                ),
                                rx.el.p(
                                    "Matches standard playbook. Auto-approved.",
                                    class_name="text-[11.5px] text-gray-500 leading-snug mt-0.5",
                                ),
                                class_name="flex flex-col min-w-0",
                            ),
                            class_name="flex items-start gap-2 p-2.5 rounded-md border border-gray-200 bg-white",
                        ),
                        rx.el.div(
                            rx.icon(
                                "circle-alert",
                                class_name="h-3.5 w-3.5 text-red-600 mt-0.5 shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Auto-renewal without notice window",
                                    class_name="text-[12.5px] font-medium text-gray-900 leading-snug",
                                ),
                                rx.el.p(
                                    "Redline: add 60-day notice before renewal.",
                                    class_name="text-[11.5px] text-gray-500 leading-snug mt-0.5",
                                ),
                                class_name="flex flex-col min-w-0",
                            ),
                            class_name="flex items-start gap-2 p-2.5 rounded-md border border-red-100 bg-red-50/50",
                        ),
                        class_name="flex flex-col gap-2 mt-3",
                    ),
                    class_name="p-3",
                ),
                class_name="min-w-0",
            ),
            class_name="grid grid-cols-1 md:grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)]",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden shadow-[0_1px_2px_rgba(0,0,0,0.04),0_12px_40px_-12px_rgba(15,23,42,0.15)]",
    )


def hero() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                _pill(),
                rx.el.h1(
                    "Close contracts ",
                    rx.el.span("10x faster", class_name="text-blue-600"),
                    ", without giving up control.",
                    class_name="mt-5 text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-gray-900 leading-[1.05]",
                ),
                rx.el.p(
                    "ContractOps AI reads every contract like your best lawyer would — flagging risky clauses against your playbook, drafting redlines, and routing approvals so revenue moves without the bottleneck.",
                    class_name="mt-5 text-lg text-gray-600 max-w-2xl leading-relaxed",
                ),
                rx.el.div(
                    rx.el.a(
                        "Start free trial",
                        rx.icon("arrow-right", class_name="h-4 w-4"),
                        href="/signup",
                        class_name="inline-flex items-center gap-1.5 h-10 px-4 rounded-md bg-blue-600 text-sm font-semibold text-white hover:bg-blue-700 transition-colors",
                    ),
                    rx.el.a(
                        rx.icon("calendar-clock", class_name="h-3.5 w-3.5"),
                        "Book a demo",
                        href="#contact-sales",
                        class_name="inline-flex items-center gap-1.5 h-10 px-4 rounded-md border border-gray-200 bg-white text-sm font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
                    ),
                    rx.el.a(
                        rx.icon(
                            "message-square-text", class_name="h-3.5 w-3.5"
                        ),
                        "Contact sales",
                        href="#contact-sales",
                        class_name="inline-flex items-center gap-1.5 h-10 px-4 rounded-md border border-gray-200 bg-white text-sm font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
                    ),
                    class_name="mt-7 flex flex-wrap items-center gap-2.5",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "check", class_name="h-3.5 w-3.5 text-emerald-600"
                        ),
                        rx.el.span(
                            "SOC 2 Type II",
                            class_name="text-[12.5px] font-medium text-gray-600",
                        ),
                        class_name="inline-flex items-center gap-1.5",
                    ),
                    rx.el.div(
                        rx.icon(
                            "check", class_name="h-3.5 w-3.5 text-emerald-600"
                        ),
                        rx.el.span(
                            "No credit card",
                            class_name="text-[12.5px] font-medium text-gray-600",
                        ),
                        class_name="inline-flex items-center gap-1.5",
                    ),
                    rx.el.div(
                        rx.icon(
                            "check", class_name="h-3.5 w-3.5 text-emerald-600"
                        ),
                        rx.el.span(
                            "14-day trial",
                            class_name="text-[12.5px] font-medium text-gray-600",
                        ),
                        class_name="inline-flex items-center gap-1.5",
                    ),
                    class_name="mt-5 flex flex-wrap items-center gap-x-5 gap-y-2",
                ),
                class_name="max-w-3xl",
            ),
            rx.el.div(
                _hero_mock(),
                class_name="mt-14",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 sm:pt-20 pb-16",
        ),
        class_name="relative bg-white border-b border-gray-200",
    )
