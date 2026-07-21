import reflex as rx
from app.components.page_shell import page_shell, page_header, stat_card
from app.states.approvals_state import ApprovalsState, Approval


def _priority_pill(p: str) -> rx.Component:
    return rx.match(
        p,
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
                "Medium",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
            ),
        ),
        rx.el.span(
            "Low",
            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
        ),
    )


def _status_pill(s: str) -> rx.Component:
    return rx.match(
        s,
        (
            "Pending",
            rx.el.span(
                rx.el.span(class_name="h-1.5 w-1.5 rounded-full bg-blue-500"),
                "Pending",
                class_name="inline-flex items-center gap-1.5 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
            ),
        ),
        (
            "Approved",
            rx.el.span(
                rx.icon("check", class_name="h-3 w-3"),
                "Approved",
                class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
            ),
        ),
        rx.el.span(
            rx.icon("x", class_name="h-3 w-3"),
            "Rejected",
            class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
        ),
    )


def _select(
    value, options: rx.Var, on_change, placeholder_label: str
) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.foreach(options, lambda o: rx.el.option(o, value=o)),
            default_value=value,
            key=value,
            on_change=on_change,
            class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100",
        ),
        rx.icon(
            "chevron-down",
            class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
        ),
        rx.el.span(
            placeholder_label,
            class_name="absolute -top-1.5 left-2 px-1 bg-white text-[10px] font-semibold uppercase tracking-wider text-gray-400",
        ),
        class_name="relative",
    )


def _row(a: Approval) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    a["contract"],
                    class_name="text-[13px] font-semibold text-gray-900 leading-tight",
                ),
                rx.el.p(
                    a["id"] + " · " + a["counterparty"],
                    class_name="text-[11.5px] text-gray-500 leading-tight mt-0.5",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="px-4 py-3 align-top",
        ),
        rx.el.td(
            rx.el.span(
                a["type"],
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
            ),
            class_name="px-4 py-3 align-top",
        ),
        rx.el.td(
            rx.el.p(
                a["value"],
                class_name="text-[13px] font-medium text-gray-900",
            ),
            class_name="px-4 py-3 align-top",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        a["requester_initials"],
                        class_name="text-[10px] font-semibold text-blue-700",
                    ),
                    class_name="h-6 w-6 rounded-full bg-blue-100 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        a["requester"],
                        class_name="text-[12.5px] font-medium text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        "→ " + a["approver"],
                        class_name="text-[11px] text-gray-500 leading-tight",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-2 min-w-0",
            ),
            class_name="px-4 py-3 align-top",
        ),
        rx.el.td(
            rx.el.p(
                a["reason"],
                class_name="text-[12px] text-gray-600 leading-snug max-w-xs",
            ),
            class_name="px-4 py-3 align-top",
        ),
        rx.el.td(
            _priority_pill(a["priority"]), class_name="px-4 py-3 align-top"
        ),
        rx.el.td(
            rx.el.div(
                _status_pill(a["status"]),
                rx.el.p(
                    a["requested"],
                    class_name="text-[11px] text-gray-500 mt-1",
                ),
                class_name="flex flex-col items-start",
            ),
            class_name="px-4 py-3 align-top",
        ),
        rx.el.td(
            rx.cond(
                a["status"] == "Pending",
                rx.el.div(
                    rx.el.button(
                        rx.icon("check", class_name="h-3.5 w-3.5"),
                        "Approve",
                        on_click=lambda: ApprovalsState.approve(a["id"]),
                        class_name="inline-flex items-center gap-1 h-7 px-2.5 rounded-md bg-blue-600 text-[12px] font-semibold text-white hover:bg-blue-700 transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-3.5 w-3.5"),
                        "Reject",
                        on_click=lambda: ApprovalsState.reject(a["id"]),
                        class_name="inline-flex items-center gap-1 h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.a(
                    "View",
                    href="/review",
                    class_name="inline-flex items-center h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
                ),
            ),
            class_name="px-4 py-3 align-top",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50/60 transition-colors",
    )


def _header_actions() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("download", class_name="h-3.5 w-3.5"),
            "Export CSV",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
        ),
        rx.el.button(
            rx.icon("bell", class_name="h-3.5 w-3.5"),
            "Notify approvers",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
        ),
        class_name="flex items-center gap-2",
    )


def _stats() -> rx.Component:
    return rx.el.div(
        stat_card(
            "Pending",
            ApprovalsState.pending_count.to_string(),
            "Awaiting sign-off across all workflows",
            "clock",
        ),
        stat_card(
            "Urgent",
            ApprovalsState.urgent_count.to_string(),
            "High-priority items over standard SLA",
            "triangle-alert",
        ),
        stat_card(
            "Approved",
            ApprovalsState.approved_this_week.to_string(),
            "Approved recently across your team",
            "circle-check",
        ),
        stat_card(
            "Rejected",
            ApprovalsState.rejected_count.to_string(),
            "Sent back to counterparty this cycle",
            "x-circle",
        ),
        class_name="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6",
    )


def _filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="h-3.5 w-3.5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
            ),
            rx.el.input(
                placeholder="Search by contract, counterparty, or requester…",
                default_value=ApprovalsState.search_query,
                on_change=ApprovalsState.set_search.debounce(300),
                class_name="w-full h-9 pl-9 pr-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100",
            ),
            class_name="relative flex-1 min-w-[220px]",
        ),
        _select(
            ApprovalsState.status_filter,
            ApprovalsState.status_options,
            ApprovalsState.set_status,
            "Status",
        ),
        _select(
            ApprovalsState.priority_filter,
            ApprovalsState.priority_options,
            ApprovalsState.set_priority,
            "Priority",
        ),
        _select(
            ApprovalsState.type_filter,
            ApprovalsState.type_options,
            ApprovalsState.set_type,
            "Type",
        ),
        rx.el.button(
            rx.icon("rotate-ccw", class_name="h-3.5 w-3.5"),
            "Reset",
            on_click=ApprovalsState.reset_filters,
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-medium text-gray-700 hover:bg-gray-50 transition-colors",
        ),
        class_name="flex flex-wrap items-center gap-2.5 mb-4",
    )


def _table() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Contract", class_name=header_cls),
                        rx.el.th("Type", class_name=header_cls),
                        rx.el.th("Value", class_name=header_cls),
                        rx.el.th("Requester", class_name=header_cls),
                        rx.el.th("Reason", class_name=header_cls),
                        rx.el.th("Priority", class_name=header_cls),
                        rx.el.th("Status", class_name=header_cls),
                        rx.el.th("Actions", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(rx.foreach(ApprovalsState.filtered, _row)),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.cond(
            ApprovalsState.filtered.length() == 0,
            rx.el.div(
                rx.icon("inbox", class_name="h-6 w-6 text-gray-300"),
                rx.el.p(
                    "No approvals match your filters",
                    class_name="mt-2 text-[13px] font-medium text-gray-700",
                ),
                rx.el.p(
                    "Try clearing filters or adjust the search query.",
                    class_name="text-[12px] text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center py-12 text-center",
            ),
            rx.fragment(),
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def approvals_page() -> rx.Component:
    return page_shell(
        "approvals",
        rx.el.div(
            page_header(
                "Approvals",
                "Route deviations to the right approver and clear your queue in minutes, not days.",
                _header_actions(),
            ),
            _stats(),
            _filters(),
            _table(),
        ),
    )
