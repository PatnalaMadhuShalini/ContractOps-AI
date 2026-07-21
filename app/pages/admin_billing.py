import reflex as rx
from app.components.page_shell import page_shell, page_header, stat_card
from app.states.billing_state import BillingState


def _inr(amount) -> rx.Var:
    return f"₹{amount}"


def _status_pill(status) -> rx.Component:
    return rx.match(
        status,
        (
            "paid",
            rx.el.span(
                rx.icon("check", class_name="h-3 w-3"),
                "Paid",
                class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
            ),
        ),
        (
            "awaiting_confirmation",
            rx.el.span(
                "Awaiting",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
            ),
        ),
        (
            "pending",
            rx.el.span(
                "Pending",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
            ),
        ),
        (
            "overdue",
            rx.el.span(
                "Overdue",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
            ),
        ),
        rx.el.span(
            "Cancelled",
            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-gray-100 text-gray-700",
        ),
    )


def _status_select(row) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.el.option("pending", value="pending"),
            rx.el.option(
                "awaiting_confirmation", value="awaiting_confirmation"
            ),
            rx.el.option("paid", value="paid"),
            rx.el.option("overdue", value="overdue"),
            rx.el.option("cancelled", value="cancelled"),
            default_value=row["status"].to(str),
            key=row["status"].to(str),
            on_change=lambda v: BillingState.admin_update_status(row["id"], v),
            class_name="h-8 pl-2 pr-7 rounded-md border border-gray-200 bg-white text-[11.5px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500",
        ),
        rx.icon(
            "chevron-down",
            class_name="h-3 w-3 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
        ),
        class_name="relative",
    )


def _country_pill(country, code) -> rx.Component:
    return rx.el.div(
        rx.icon("globe", class_name="h-3 w-3 text-gray-400"),
        rx.el.span(
            country,
            class_name="text-[11.5px] font-medium text-gray-700",
        ),
        rx.el.span(
            code,
            class_name="ml-1 inline-flex items-center h-4 px-1 rounded bg-gray-100 text-[10px] font-semibold text-gray-600",
        ),
        class_name="inline-flex items-center gap-1",
    )


def _invoice_row(row) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.p(
                row["id"],
                class_name="text-[12.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                row["period"],
                class_name="text-[11px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                row["company_name"],
                class_name="text-[13px] font-semibold text-gray-900",
            ),
            rx.el.p(
                row["billing_email"],
                class_name="text-[11px] text-gray-500 truncate max-w-[14rem]",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            _country_pill(row["billing_country"], row["currency_code"]),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                f"{row['plan']} · {row['seats']} seats",
                class_name="text-[12.5px] font-medium text-gray-800",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                row["display_total"],
                class_name="text-[13px] font-semibold text-gray-900",
            ),
            rx.el.p(
                _inr(row["total_inr"]) + " ledger",
                class_name="text-[10.5px] text-gray-400 mt-0.5",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                row["method"],
                class_name="text-[12px] text-gray-700",
            ),
            rx.el.p(
                row["transaction_ref"],
                class_name="text-[10.5px] text-gray-400 font-mono truncate max-w-[10rem]",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                row["gst_number"],
                class_name="text-[11.5px] font-mono text-gray-700",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            _status_pill(row["status"]), class_name="px-4 py-3 align-middle"
        ),
        rx.el.td(
            rx.el.div(
                _status_select(row),
                rx.el.button(
                    rx.icon("check", class_name="h-3.5 w-3.5"),
                    on_click=lambda: BillingState.admin_mark_paid(row["id"]),
                    class_name="inline-flex items-center justify-center h-8 w-8 rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-emerald-50 hover:border-emerald-200 hover:text-emerald-700 transition-colors",
                    title="Mark paid",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-3.5 w-3.5"),
                    on_click=lambda: BillingState.admin_cancel_invoice(
                        row["id"]
                    ),
                    class_name="inline-flex items-center justify-center h-8 w-8 rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                    title="Cancel invoice",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50/60 transition-colors",
    )


def _filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    BillingState.status_options,
                    lambda o: rx.el.option(o, value=o),
                ),
                default_value=BillingState.admin_status_filter,
                key=BillingState.admin_status_filter,
                on_change=BillingState.admin_set_status_filter,
                class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500",
            ),
            rx.icon(
                "chevron-down",
                class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    BillingState.company_options,
                    lambda o: rx.el.option(o, value=o),
                ),
                default_value=BillingState.admin_company_filter,
                key=BillingState.admin_company_filter,
                on_change=BillingState.admin_set_company_filter,
                class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500",
            ),
            rx.icon(
                "chevron-down",
                class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
            ),
            class_name="relative",
        ),
        class_name="flex items-center gap-2 mb-4 flex-wrap",
    )


def _invoices_table() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "All invoices",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Every invoice across every workspace",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-14 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Invoice", class_name=header_cls),
                        rx.el.th("Workspace", class_name=header_cls),
                        rx.el.th("Country", class_name=header_cls),
                        rx.el.th("Plan", class_name=header_cls),
                        rx.el.th("Total", class_name=header_cls),
                        rx.el.th("Method / ref", class_name=header_cls),
                        rx.el.th("GSTIN", class_name=header_cls),
                        rx.el.th("Status", class_name=header_cls),
                        rx.el.th("Actions", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(BillingState.admin_invoices, _invoice_row)
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _upgrade_row(u) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    u["id"],
                    class_name="text-[11px] font-medium text-gray-500",
                ),
                rx.el.p(
                    u["company_name"],
                    class_name="text-[13.5px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"{u['current_plan']} → {u['requested_plan']}",
                    class_name="mt-0.5 text-[12.5px] font-medium text-blue-700",
                ),
                rx.el.p(
                    f"{u['seats']} seats · {u['requested_by']} · {u['created']}",
                    class_name="mt-0.5 text-[11.5px] text-gray-500",
                ),
                rx.cond(
                    u["reason"] != "",
                    rx.el.p(
                        u["reason"],
                        class_name="mt-2 text-[12px] text-gray-600 leading-snug",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    u["admin_note"] != "",
                    rx.el.p(
                        f"Admin note: {u['admin_note']}",
                        class_name="mt-1 text-[11.5px] text-gray-500 leading-snug",
                    ),
                    rx.fragment(),
                ),
                class_name="flex flex-col min-w-0",
            ),
            rx.match(
                u["status"],
                (
                    "approved",
                    rx.el.span(
                        rx.icon("check", class_name="h-3 w-3"),
                        "Approved",
                        class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
                    ),
                ),
                (
                    "rejected",
                    rx.el.span(
                        "Rejected",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
                    ),
                ),
                rx.el.span(
                    "Pending",
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
                ),
            ),
            class_name="flex items-start justify-between gap-3 flex-wrap",
        ),
        rx.cond(
            u["status"] == "pending",
            rx.el.div(
                rx.el.button(
                    rx.icon("check", class_name="h-3.5 w-3.5"),
                    "Approve & change plan",
                    on_click=lambda: BillingState.admin_approve_upgrade(
                        u["id"]
                    ),
                    class_name="inline-flex items-center gap-1.5 h-8 px-3 rounded-md bg-blue-600 text-[12px] font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-3.5 w-3.5"),
                    "Reject",
                    on_click=lambda: BillingState.admin_reject_upgrade(u["id"]),
                    class_name="inline-flex items-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                ),
                class_name="mt-3 pt-3 border-t border-gray-100 flex items-center gap-1.5 flex-wrap",
            ),
            rx.fragment(),
        ),
        class_name="p-4 rounded-xl border border-gray-200 bg-white",
    )


def _upgrades_grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Plan change requests",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Approve to update the workspace plan and trigger a pro-rated invoice",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="mb-3",
        ),
        rx.el.div(
            rx.foreach(BillingState.admin_upgrade_requests, _upgrade_row),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-3",
        ),
        rx.cond(
            BillingState.admin_upgrade_requests.length() == 0,
            rx.el.div(
                rx.icon("inbox", class_name="h-6 w-6 text-gray-300"),
                rx.el.p(
                    "No plan change requests yet",
                    class_name="mt-2 text-[13px] font-medium text-gray-700",
                ),
                class_name="flex flex-col items-center justify-center py-10 text-center border border-gray-200 rounded-xl bg-white",
            ),
            rx.fragment(),
        ),
    )


def _stats() -> rx.Component:
    s = BillingState.admin_stats
    return rx.el.div(
        stat_card(
            "Revenue collected",
            _inr(s["total_paid"]),
            "All-time paid invoices",
            "circle-dollar-sign",
        ),
        stat_card(
            "Outstanding",
            _inr(s["outstanding"]),
            "Pending + awaiting + overdue",
            "wallet",
        ),
        stat_card(
            "Awaiting confirmation",
            s["awaiting_confirmation"].to_string(),
            "Customer-submitted payments to verify",
            "hourglass",
        ),
        stat_card(
            "Overdue",
            s["overdue"].to_string(),
            s["pending_upgrades"].to_string() + " plan change requests pending",
            "triangle-alert",
        ),
        class_name="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6",
    )


def _header_actions() -> rx.Component:
    return rx.el.a(
        "Platform admin",
        rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
        href="/admin",
        class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
    )


def _workspace_card(w) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("building-2", class_name="h-4 w-4 text-blue-600"),
                class_name="h-9 w-9 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    w["company_name"],
                    class_name="text-[13.5px] font-semibold text-gray-900 leading-tight",
                ),
                rx.el.p(
                    f"{w['domain']} · {w['plan']}",
                    class_name="text-[11.5px] text-gray-500 leading-tight mt-0.5",
                ),
                class_name="flex flex-col min-w-0",
            ),
            rx.el.div(
                _country_pill(w["country"], w["currency_code"]),
                class_name="ml-auto shrink-0",
            ),
            class_name="flex items-start gap-3 flex-wrap",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Paid",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    w["total_paid_display"],
                    class_name="mt-0.5 text-[14px] font-semibold text-gray-900",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.p(
                    "Outstanding",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    w["outstanding_display"],
                    class_name=rx.cond(
                        w["outstanding_inr"].to(int) > 0,
                        "mt-0.5 text-[14px] font-semibold text-amber-700",
                        "mt-0.5 text-[14px] font-semibold text-gray-900",
                    ),
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.p(
                    "Invoices",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    w["invoices"].to_string(),
                    class_name="mt-0.5 text-[14px] font-semibold text-gray-900",
                ),
                class_name="flex flex-col",
            ),
            class_name="mt-4 grid grid-cols-3 gap-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("mail", class_name="h-3 w-3 text-gray-400"),
                rx.el.p(
                    w["billing_email"],
                    class_name="text-[11.5px] text-gray-700 truncate",
                ),
                class_name="inline-flex items-center gap-1.5 min-w-0",
            ),
            rx.el.div(
                rx.icon("receipt", class_name="h-3 w-3 text-gray-400"),
                rx.el.p(
                    w["gst_number"],
                    class_name="text-[11.5px] font-mono text-gray-700 truncate",
                ),
                class_name="inline-flex items-center gap-1.5 min-w-0",
            ),
            class_name="mt-4 pt-3 border-t border-gray-100 flex flex-col gap-1.5",
        ),
        rx.cond(
            (w["awaiting"].to(int) > 0) | (w["overdue"].to(int) > 0),
            rx.el.div(
                rx.cond(
                    w["awaiting"].to(int) > 0,
                    rx.el.span(
                        w["awaiting"].to(int).to_string() + " awaiting",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    w["overdue"].to(int) > 0,
                    rx.el.span(
                        w["overdue"].to(int).to_string() + " overdue",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    "Filter",
                    rx.icon("arrow-right", class_name="h-3 w-3"),
                    on_click=lambda: BillingState.admin_set_company_filter(
                        w["company_id"]
                    ),
                    class_name="ml-auto inline-flex items-center gap-1 h-6 px-2 rounded-md border border-gray-200 bg-white text-[11px] font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
                ),
                class_name="mt-3 flex items-center gap-1.5 flex-wrap",
            ),
            rx.fragment(),
        ),
        class_name="p-4 rounded-xl border border-gray-200 bg-white",
    )


def _workspaces_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Workspaces",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Per-workspace billing country, contact, and running totals",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="mb-3",
        ),
        rx.el.div(
            rx.foreach(BillingState.admin_workspace_summaries, _workspace_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3",
        ),
    )


def _money_receiving_guide() -> rx.Component:
    def _step(
        num: str, title: str, body: rx.Component, icon: str
    ) -> rx.Component:
        return rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
                    class_name="h-8 w-8 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
                ),
                rx.el.span(
                    num,
                    class_name="ml-auto text-[10.5px] font-semibold uppercase tracking-wider text-gray-400",
                ),
                class_name="flex items-center",
            ),
            rx.el.p(
                title,
                class_name="mt-3 text-[13.5px] font-semibold text-gray-900",
            ),
            body,
            class_name="p-4 rounded-xl border border-gray-200 bg-white",
        )

    def _bullet(icon: str, text: rx.Component) -> rx.Component:
        return rx.el.li(
            rx.icon(
                icon,
                class_name="h-3.5 w-3.5 text-blue-600 mt-0.5 shrink-0",
            ),
            rx.el.span(
                text,
                class_name="text-[12.5px] text-gray-700 leading-relaxed",
            ),
            class_name="flex items-start gap-1.5",
        )

    india_body = rx.el.ul(
        _bullet(
            "smartphone",
            rx.el.span(
                "UPI to ",
                rx.el.span(
                    "contractops@hdfcbank",
                    class_name="font-mono font-semibold text-gray-900",
                ),
            ),
        ),
        _bullet(
            "landmark",
            rx.el.span(
                "NEFT / RTGS / IMPS to HDFC A/c ",
                rx.el.span(
                    "5010 0234 5678 90",
                    class_name="font-mono font-semibold text-gray-900",
                ),
                " · IFSC ",
                rx.el.span(
                    "HDFC0001234",
                    class_name="font-mono font-semibold text-gray-900",
                ),
            ),
        ),
        _bullet(
            "receipt",
            rx.el.span(
                "Cheque / DD to ",
                rx.el.span(
                    "ContractOps AI Private Limited",
                    class_name="font-semibold text-gray-900",
                ),
                " (Bengaluru address)",
            ),
        ),
        class_name="mt-2 flex flex-col gap-1.5",
    )

    intl_body = rx.el.ul(
        _bullet(
            "globe",
            rx.el.span(
                "SWIFT wire to HDFC · BIC ",
                rx.el.span(
                    "HDFCINBB",
                    class_name="font-mono font-semibold text-gray-900",
                ),
                " (INR-denominated ledger)",
            ),
        ),
        _bullet(
            "landmark",
            rx.el.span(
                "ACH / Fedwire to JPMorgan Chase · Routing ",
                rx.el.span(
                    "021000021",
                    class_name="font-mono font-semibold text-gray-900",
                ),
                " · A/c ",
                rx.el.span(
                    "8842095173",
                    class_name="font-mono font-semibold text-gray-900",
                ),
            ),
        ),
        _bullet(
            "receipt",
            rx.el.span(
                "Cheque to ",
                rx.el.span(
                    "ContractOps AI Inc",
                    class_name="font-semibold text-gray-900",
                ),
                " (San Francisco address)",
            ),
        ),
        class_name="mt-2 flex flex-col gap-1.5",
    )

    reconcile_body = rx.el.div(
        rx.el.p(
            "Customer submits their payment reference from the billing page. The invoice flips to ",
            rx.el.span(
                "awaiting confirmation",
                class_name="font-semibold text-blue-700",
            ),
            ". You then cross-check the reference against your bank statement or UPI app.",
            class_name="mt-2 text-[12.5px] text-gray-700 leading-relaxed",
        ),
        rx.el.div(
            rx.el.span(
                rx.icon("check", class_name="h-3 w-3"),
                "Paid",
                class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
            ),
            rx.el.span(
                "Awaiting",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
            ),
            rx.el.span(
                "Overdue",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
            ),
            rx.el.span(
                "Cancelled",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-gray-100 text-gray-700",
            ),
            class_name="mt-3 flex flex-wrap items-center gap-1.5",
        ),
    )

    visibility_body = rx.el.ul(
        _bullet(
            "building-2",
            rx.el.span("Workspace name, domain, plan, and seat count"),
        ),
        _bullet(
            "globe",
            rx.el.span(
                "Billing country + display currency (INR ledger internally)"
            ),
        ),
        _bullet(
            "mail",
            rx.el.span("Billing contact email and GSTIN (India only)"),
        ),
        _bullet(
            "hash",
            rx.el.span(
                "Transaction reference (UPI ref, UTR, MT103, ACH trace, cheque no.)"
            ),
        ),
        _bullet(
            "file-text",
            rx.el.span("Customer-provided notes and full invoice history"),
        ),
        class_name="mt-2 flex flex-col gap-1.5",
    )

    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "info",
                    class_name="h-4 w-4 text-blue-600",
                ),
                class_name="h-8 w-8 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    "How money is received",
                    class_name="text-[14px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    "This workspace runs a manual, provider-free billing loop — no Stripe, PayPal, or Razorpay integration. Payments hit our bank accounts directly and are reconciled from this dashboard.",
                    class_name="mt-0.5 text-[12.5px] text-gray-600 leading-relaxed max-w-3xl",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-start gap-3 mb-4",
        ),
        rx.el.div(
            _step(
                "01",
                "India · INR to HDFC Bank",
                rx.el.div(
                    rx.el.p(
                        "Customers on India-based workspaces see these instructions on their ",
                        rx.el.span(
                            "/billing",
                            class_name="font-mono text-gray-800",
                        ),
                        " page and pay in INR + 18% GST:",
                        class_name="mt-1 text-[12.5px] text-gray-600 leading-relaxed",
                    ),
                    india_body,
                ),
                "indian-rupee",
            ),
            _step(
                "02",
                "International · display currency",
                rx.el.div(
                    rx.el.p(
                        "Non-India workspaces see totals in their local currency (USD, GBP, EUR, AED…) and pay via international rails. GST does not apply:",
                        class_name="mt-1 text-[12.5px] text-gray-600 leading-relaxed",
                    ),
                    intl_body,
                ),
                "globe",
            ),
            _step(
                "03",
                "Verify & reconcile in this dashboard",
                reconcile_body,
                "shield-check",
            ),
            _step(
                "04",
                "What customer details you see",
                visibility_body,
                "eye",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "settings",
                    class_name="h-3.5 w-3.5 text-gray-500 mt-0.5 shrink-0",
                ),
                rx.el.p(
                    rx.el.span(
                        "Where instructions live: ",
                        class_name="font-semibold text-gray-900",
                    ),
                    "the bank / UPI / wire details shown to customers come from ",
                    rx.el.span(
                        "INDIA_PAYMENT_INSTRUCTIONS",
                        class_name="font-mono text-gray-800",
                    ),
                    " and ",
                    rx.el.span(
                        "INTERNATIONAL_PAYMENT_INSTRUCTIONS",
                        class_name="font-mono text-gray-800",
                    ),
                    " in ",
                    rx.el.span(
                        "app/states/billing_state.py",
                        class_name="font-mono text-gray-800",
                    ),
                    ". Update the account numbers, IFSC, SWIFT/BIC, and mailing addresses there — the billing page picks them up automatically for the customer's selected country.",
                    class_name="text-[12px] text-gray-600 leading-relaxed",
                ),
                class_name="flex items-start gap-2",
            ),
            rx.el.div(
                rx.icon(
                    "triangle-alert",
                    class_name="h-3.5 w-3.5 text-amber-600 mt-0.5 shrink-0",
                ),
                rx.el.p(
                    rx.el.span(
                        "What stays offline / manual: ",
                        class_name="font-semibold text-gray-900",
                    ),
                    "the actual money movement, bank statement reconciliation, GST invoice generation, and any refunds are handled by your finance team outside the app. This dashboard is the system of record for invoice status only — no funds are held, moved, or refunded here.",
                    class_name="text-[12px] text-gray-600 leading-relaxed",
                ),
                class_name="flex items-start gap-2",
            ),
            class_name="mt-4 grid grid-cols-1 lg:grid-cols-2 gap-3 p-4 rounded-lg border border-gray-200 bg-gray-50/60",
        ),
        class_name="mb-6 p-5 rounded-xl border border-gray-200 bg-white",
    )


def admin_billing_page() -> rx.Component:
    return page_shell(
        "admin_billing",
        rx.el.div(
            page_header(
                "Billing operations",
                "Reconcile customer payments, approve plan changes, and track outstanding invoices across every workspace — with billing country, currency, and payment references in one place.",
                _header_actions(),
            ),
            _stats(),
            _money_receiving_guide(),
            _workspaces_section(),
            rx.el.div(_filters(), class_name="mt-6"),
            _invoices_table(),
            rx.el.div(_upgrades_grid(), class_name="mt-6"),
        ),
    )
