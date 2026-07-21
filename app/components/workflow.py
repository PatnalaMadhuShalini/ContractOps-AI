import reflex as rx


def _step(
    num: str, title: str, body: str, icon: str, accent: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                num,
                class_name="inline-flex items-center justify-center h-6 w-6 rounded-md bg-blue-50 text-blue-700 text-[11.5px] font-semibold",
            ),
            rx.icon(icon, class_name="h-4 w-4 text-gray-400 ml-auto"),
            class_name="flex items-center",
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


def _stage_preview() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Live pipeline",
                    class_name="text-[12px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.span(
                    rx.el.span(
                        class_name="h-1.5 w-1.5 rounded-full bg-emerald-500"
                    ),
                    "Syncing",
                    class_name="inline-flex items-center gap-1.5 ml-auto text-[11.5px] font-medium text-gray-600",
                ),
                class_name="flex items-center px-4 h-10 border-b border-gray-200",
            ),
            rx.el.div(
                _stage_col(
                    "Intake",
                    "6",
                    [
                        (
                            "Northwind DPA",
                            "New · 2m ago",
                            "bg-blue-50 text-blue-700",
                        ),
                        ("Initech SOW", "Uploaded", "bg-blue-50 text-blue-700"),
                    ],
                ),
                _stage_col(
                    "AI Review",
                    "3",
                    [
                        (
                            "Acme MSA v3",
                            "8 flags · 62/100",
                            "bg-amber-50 text-amber-700",
                        ),
                        (
                            "Umbrella SaaS",
                            "3 flags · 78/100",
                            "bg-emerald-50 text-emerald-700",
                        ),
                    ],
                ),
                _stage_col(
                    "Approval",
                    "2",
                    [
                        (
                            "Globex DPA",
                            "GC review",
                            "bg-violet-50 text-violet-700",
                        ),
                    ],
                ),
                _stage_col(
                    "Signed",
                    "12",
                    [
                        (
                            "Vandelay MSA",
                            "Countersigned",
                            "bg-emerald-50 text-emerald-700",
                        ),
                        (
                            "Soylent NDA",
                            "Sent to CS",
                            "bg-emerald-50 text-emerald-700",
                        ),
                    ],
                ),
                class_name="grid grid-cols-2 lg:grid-cols-4 divide-x divide-gray-200",
            ),
            class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
        ),
        class_name="mt-10",
    )


def _stage_col(
    name: str, count: str, items: list[tuple[str, str, str]]
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                name, class_name="text-[12.5px] font-semibold text-gray-900"
            ),
            rx.el.span(
                count,
                class_name="ml-auto text-[11px] font-medium text-gray-500",
            ),
            class_name="flex items-center px-3 h-9 border-b border-gray-100 bg-gray-50/60",
        ),
        rx.el.div(
            *[
                rx.el.div(
                    rx.el.p(
                        t,
                        class_name="text-[12.5px] font-medium text-gray-900 leading-tight truncate",
                    ),
                    rx.el.div(
                        rx.el.span(
                            sub,
                            class_name=f"inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold {cls}",
                        ),
                        class_name="mt-1.5",
                    ),
                    class_name="p-2.5 rounded-md border border-gray-200 bg-white",
                )
                for (t, sub, cls) in items
            ],
            class_name="flex flex-col gap-2 p-3 min-h-[180px]",
        ),
    )


def workflow() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "How it works",
                    class_name="text-[12px] font-semibold uppercase tracking-[0.14em] text-blue-600",
                ),
                rx.el.h2(
                    "One pipeline, from intake to signed.",
                    class_name="mt-2 text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "ContractOps AI plugs into the tools your team already uses — email, Slack, Salesforce, Google Drive — and quietly moves every agreement forward.",
                    class_name="mt-3 text-[15px] text-gray-600 max-w-2xl",
                ),
                class_name="max-w-3xl",
            ),
            rx.el.div(
                _step(
                    "01",
                    "Ingest anywhere",
                    "Forward from email, drop into Slack, or auto-pull from your CRM. We parse Word, PDF, and scans.",
                    "inbox",
                ),
                _step(
                    "02",
                    "AI review against your playbook",
                    "Every clause is scored against your standards with cited fallback language and rationale.",
                    "sparkles",
                ),
                _step(
                    "03",
                    "Route the right approvals",
                    "Deviation-based routing to GC, Finance, or Security — no more manual triage or email loops.",
                    "git-branch",
                ),
                _step(
                    "04",
                    "Sign, store, and track",
                    "Native e-signature, obligation tracking, and renewal alerts so nothing slips through the cracks.",
                    "file_key",
                ),
                class_name="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
            ),
            _stage_preview(),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
        ),
        class_name="bg-white border-b border-gray-200",
        id="workflow",
    )
