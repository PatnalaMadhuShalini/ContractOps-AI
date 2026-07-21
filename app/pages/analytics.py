import reflex as rx
from app.components.page_shell import page_shell, page_header, stat_card
from app.states.analytics_state import AnalyticsState


def _period_button(opt: dict) -> rx.Component:
    active = AnalyticsState.period == opt["key"]
    return rx.el.button(
        opt["label"],
        on_click=lambda: AnalyticsState.set_period(opt["key"]),
        class_name=rx.cond(
            active,
            "h-8 px-3 rounded-md bg-white text-[12.5px] font-semibold text-gray-900 shadow-sm border border-gray-200",
            "h-8 px-3 rounded-md text-[12.5px] font-semibold text-gray-500 hover:text-gray-800",
        ),
    )


def _report_tab(opt: dict) -> rx.Component:
    active = AnalyticsState.report_type == opt["key"]
    return rx.el.button(
        opt["label"],
        on_click=lambda: AnalyticsState.set_report(opt["key"]),
        class_name=rx.cond(
            active,
            "h-9 px-3 border-b-2 border-blue-600 text-[13px] font-semibold text-blue-700",
            "h-9 px-3 border-b-2 border-transparent text-[13px] font-medium text-gray-500 hover:text-gray-800",
        ),
    )


def _header_actions() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(AnalyticsState.period_options, _period_button),
            class_name="inline-flex items-center gap-1 p-1 rounded-lg bg-gray-100 border border-gray-200",
        ),
        rx.el.button(
            rx.icon("mail", class_name="h-3.5 w-3.5"),
            "Schedule report",
            on_click=AnalyticsState.schedule_report,
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
        ),
        rx.el.button(
            rx.icon("download", class_name="h-3.5 w-3.5"),
            "Export CSV",
            on_click=AnalyticsState.export_report,
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
        ),
        class_name="flex items-center gap-2 flex-wrap",
    )


def _kpis() -> rx.Component:
    return rx.el.div(
        stat_card(
            "Contracts closed",
            AnalyticsState.kpis["volume"],
            "Signed and countersigned in period",
            "file-check-2",
        ),
        stat_card(
            "Avg. cycle time",
            AnalyticsState.kpis["cycle"],
            "Down 62% vs. the previous period",
            "timer",
        ),
        stat_card(
            "Total value",
            AnalyticsState.kpis["value"],
            "ARR + one-time contract value",
            "circle-dollar-sign",
        ),
        stat_card(
            "Auto-approved",
            AnalyticsState.kpis["auto"],
            "Deviation-free matches to playbook",
            "sparkles",
        ),
        class_name="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6",
    )


def _volume_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Contract volume",
                    class_name="text-[13.5px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Signed vs. in-review over selected period",
                    class_name="text-[12px] text-gray-500 mt-0.5",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="h-2 w-2 rounded-full bg-blue-600"),
                    rx.el.span(
                        "Signed",
                        class_name="text-[11.5px] font-medium text-gray-600",
                    ),
                    class_name="inline-flex items-center gap-1.5",
                ),
                rx.el.div(
                    rx.el.div(class_name="h-2 w-2 rounded-full bg-blue-200"),
                    rx.el.span(
                        "In review",
                        class_name="text-[11.5px] font-medium text-gray-600",
                    ),
                    class_name="inline-flex items-center gap-1.5",
                ),
                class_name="ml-auto flex items-center gap-4",
            ),
            class_name="flex items-center px-4 h-12 border-b border-gray-100",
        ),
        rx.el.div(
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    horizontal=True,
                    vertical=False,
                    class_name="opacity-40",
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.x_axis(
                    data_key="label",
                    axis_line=False,
                    tick_line=False,
                    custom_attrs={"fontSize": "11px"},
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    custom_attrs={"fontSize": "11px"},
                ),
                rx.recharts.area(
                    data_key="in_review",
                    stack_id="1",
                    stroke="#bfdbfe",
                    fill="#dbeafe",
                    type_="monotone",
                ),
                rx.recharts.area(
                    data_key="signed",
                    stack_id="1",
                    stroke="#2563eb",
                    fill="#3b82f6",
                    type_="monotone",
                ),
                data=AnalyticsState.volume_data,
                width="100%",
                height=280,
                margin={"top": 16, "right": 16, "left": 0, "bottom": 8},
            ),
            class_name="p-2",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _type_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Volume by contract type",
                    class_name="text-[13.5px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Distribution across your paper types",
                    class_name="text-[12px] text-gray-500 mt-0.5",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center px-4 h-12 border-b border-gray-100",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    horizontal=True,
                    vertical=False,
                    class_name="opacity-40",
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.x_axis(
                    data_key="type",
                    axis_line=False,
                    tick_line=False,
                    custom_attrs={"fontSize": "11px"},
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    custom_attrs={"fontSize": "11px"},
                ),
                rx.recharts.bar(
                    data_key="count",
                    fill="#3b82f6",
                    radius=[4, 4, 0, 0],
                ),
                data=AnalyticsState.type_breakdown,
                width="100%",
                height=280,
                margin={"top": 16, "right": 16, "left": 0, "bottom": 8},
            ),
            class_name="p-2",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _cycle_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Average cycle time by type (hours)",
                    class_name="text-[13.5px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    "From intake to signature — lower is better",
                    class_name="text-[12px] text-gray-500 mt-0.5",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center px-4 h-12 border-b border-gray-100",
        ),
        rx.el.div(
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3",
                    vertical=True,
                    horizontal=False,
                    class_name="opacity-40",
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.x_axis(
                    type_="number",
                    axis_line=False,
                    tick_line=False,
                    custom_attrs={"fontSize": "11px"},
                ),
                rx.recharts.y_axis(
                    data_key="type",
                    type_="category",
                    axis_line=False,
                    tick_line=False,
                    custom_attrs={"fontSize": "11px"},
                ),
                rx.recharts.bar(
                    data_key="hours",
                    fill="#2563eb",
                    radius=[0, 4, 4, 0],
                ),
                data=AnalyticsState.cycle_by_type,
                layout="vertical",
                width="100%",
                height=280,
                margin={"top": 16, "right": 24, "left": 20, "bottom": 8},
            ),
            class_name="p-2",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _team_table() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Team performance",
                    class_name="text-[13.5px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Reviewer throughput and approval rates",
                    class_name="text-[12px] text-gray-500 mt-0.5",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center px-4 h-12 border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Reviewer", class_name=header_cls),
                        rx.el.th("Role", class_name=header_cls),
                        rx.el.th("Reviewed", class_name=header_cls),
                        rx.el.th("Avg hours", class_name=header_cls),
                        rx.el.th("Approval rate", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(
                        AnalyticsState.team,
                        lambda m: rx.el.tr(
                            rx.el.td(
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.p(
                                            m["initials"],
                                            class_name="text-[10px] font-semibold text-blue-700",
                                        ),
                                        class_name="h-7 w-7 rounded-full bg-blue-100 flex items-center justify-center shrink-0",
                                    ),
                                    rx.el.p(
                                        m["name"],
                                        class_name="text-[13px] font-medium text-gray-900",
                                    ),
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-4 py-3",
                            ),
                            rx.el.td(
                                m["role"],
                                class_name="px-4 py-3 text-[12.5px] text-gray-600",
                            ),
                            rx.el.td(
                                m["reviewed"].to_string(),
                                class_name="px-4 py-3 text-[13px] font-medium text-gray-900",
                            ),
                            rx.el.td(
                                m["avg_hours"].to_string() + " h",
                                class_name="px-4 py-3 text-[13px] font-medium text-gray-900",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.div(
                                            class_name="h-full bg-blue-600 rounded-full",
                                            style={
                                                "width": m[
                                                    "approval_rate"
                                                ].to_string()
                                                + "%"
                                            },
                                        ),
                                        class_name="h-1.5 w-24 rounded-full bg-gray-100 overflow-hidden",
                                    ),
                                    rx.el.p(
                                        m["approval_rate"].to_string() + "%",
                                        class_name="text-[12.5px] font-semibold text-gray-900",
                                    ),
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-4 py-3",
                            ),
                            class_name="border-t border-gray-100",
                        ),
                    )
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _counterparties() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Top counterparties",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "By contract count in period",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-12 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.el.div(
            rx.foreach(
                AnalyticsState.counterparties,
                lambda c: rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            c["name"],
                            class_name="text-[13px] font-medium text-gray-900 leading-tight",
                        ),
                        rx.el.p(
                            c["contracts"].to_string() + " contracts",
                            class_name="text-[11.5px] text-gray-500 leading-tight",
                        ),
                        class_name="flex flex-col min-w-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            c["value"],
                            class_name="text-[13px] font-semibold text-gray-900",
                        ),
                        rx.match(
                            c["risk"],
                            (
                                "High",
                                rx.el.span(
                                    "High",
                                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
                                ),
                            ),
                            (
                                "Medium",
                                rx.el.span(
                                    "Med",
                                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
                                ),
                            ),
                            rx.el.span(
                                "Low",
                                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
                            ),
                        ),
                        class_name="flex items-center gap-2 shrink-0",
                    ),
                    class_name="flex items-center justify-between gap-2 px-4 py-3 border-t border-gray-100 first:border-t-0",
                ),
            ),
            class_name="flex flex-col",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _overview_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(_volume_chart(), class_name="lg:col-span-7"),
            rx.el.div(_type_chart(), class_name="lg:col-span-5"),
            class_name="grid grid-cols-1 lg:grid-cols-12 gap-4",
        ),
        rx.el.div(
            rx.el.div(_team_table(), class_name="lg:col-span-8"),
            rx.el.div(_counterparties(), class_name="lg:col-span-4"),
            class_name="mt-4 grid grid-cols-1 lg:grid-cols-12 gap-4",
        ),
    )


def _cycle_content() -> rx.Component:
    return rx.el.div(
        _cycle_chart(),
        rx.el.div(_volume_chart(), class_name="mt-4"),
    )


def _volume_content() -> rx.Component:
    return rx.el.div(
        _type_chart(),
        rx.el.div(_counterparties(), class_name="mt-4"),
    )


def _team_content() -> rx.Component:
    return rx.el.div(
        _team_table(),
        rx.el.div(_cycle_chart(), class_name="mt-4"),
    )


def analytics_page() -> rx.Component:
    return page_shell(
        "analytics",
        rx.el.div(
            page_header(
                "Analytics",
                "Understand throughput, bottlenecks, and where AI is compounding your legal capacity.",
                _header_actions(),
            ),
            _kpis(),
            rx.el.div(
                rx.el.div(
                    rx.foreach(AnalyticsState.report_options, _report_tab),
                    class_name="flex items-center gap-1 border-b border-gray-200 overflow-x-auto",
                ),
                rx.el.div(
                    rx.match(
                        AnalyticsState.report_type,
                        ("overview", _overview_content()),
                        ("cycle", _cycle_content()),
                        ("volume", _volume_content()),
                        ("team", _team_content()),
                        _overview_content(),
                    ),
                    class_name="pt-5",
                ),
            ),
        ),
    )
