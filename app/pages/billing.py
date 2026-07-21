import reflex as rx
from app.components.page_shell import page_shell, page_header, stat_card
from app.states.billing_state import (
    BillingState,
    PLAN_PRICING_INR,
    BILLING_COUNTRIES,
)
from app.states.auth_state import AuthState


def _money(amount) -> rx.Var:
    """Localized amount display.

    Invoices are stored in INR. For India customers we show ₹ with the raw
    integer amount. For non-India customers we convert at the current display
    rate and prefix the localized currency symbol. Admin-facing views keep
    using the raw INR ledger via their own `_inr` helper.
    """
    return rx.cond(
        BillingState.is_india,
        "₹" + str(amount),
        BillingState.currency_symbol
        + (amount / BillingState.currency_rate).to(int).to_string(),
    )


# Backwards-compatible alias so callsites keep reading well.
_inr = _money


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
                rx.el.span(class_name="h-1.5 w-1.5 rounded-full bg-blue-500"),
                "Awaiting confirmation",
                class_name="inline-flex items-center gap-1.5 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
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
                rx.icon("triangle-alert", class_name="h-3 w-3"),
                "Overdue",
                class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
            ),
        ),
        rx.el.span(
            "Cancelled",
            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-gray-100 text-gray-700",
        ),
    )


_METHOD_ICONS: dict[str, str] = {
    "UPI": "smartphone",
    "Bank transfer": "landmark",
    "Cheque": "receipt",
    "Wire transfer": "globe",
    "ACH transfer": "landmark",
}


def _method_button_dynamic(method) -> rx.Component:
    """Method button rendered inside rx.foreach — icon is looked up from a map."""
    active = BillingState.selected_method == method
    icon = rx.match(
        method,
        ("UPI", "smartphone"),
        ("Bank transfer", "landmark"),
        ("Wire transfer", "globe"),
        ("ACH transfer", "landmark"),
        ("Cheque", "receipt"),
        "landmark",
    )
    return rx.el.button(
        rx.icon(icon, class_name="h-4 w-4"),
        method,
        on_click=lambda: BillingState.select_method(method),
        type="button",
        class_name=rx.cond(
            active,
            "inline-flex items-center gap-2 h-9 px-3 rounded-md border-2 border-blue-600 bg-blue-50/60 text-[13px] font-semibold text-blue-700",
            "inline-flex items-center gap-2 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-medium text-gray-700 hover:bg-gray-50 transition-colors",
        ),
    )


def _payment_instructions() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    BillingState.selected_instructions["icon"],
                    class_name="h-4 w-4 text-blue-600",
                ),
                class_name="h-8 w-8 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    BillingState.selected_instructions["label"],
                    class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    BillingState.selected_instructions["primary"],
                    class_name="mt-0.5 text-[13px] font-semibold text-gray-900 font-mono break-all",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-start gap-3",
        ),
        rx.el.p(
            BillingState.selected_instructions["hint"],
            class_name="mt-3 text-[12px] text-gray-600 leading-relaxed",
        ),
        class_name="p-3 rounded-md border border-gray-200 bg-gray-50/60",
    )


def _open_invoice_card() -> rx.Component:
    inv = BillingState.my_open_invoice
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Current invoice",
                    class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    inv["id"],
                    class_name="mt-1 text-[15px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    inv["plan"]
                    + " · "
                    + inv["seats"].to_string()
                    + " seats · "
                    + inv["period"],
                    class_name="text-[12px] text-gray-600",
                ),
                class_name="flex flex-col",
            ),
            _status_pill(inv["status"]),
            class_name="flex items-start justify-between gap-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Subtotal",
                    class_name="text-[11px] text-gray-500",
                ),
                rx.el.p(
                    _inr(inv["subtotal_inr"]),
                    class_name="text-[13px] font-medium text-gray-900",
                ),
                class_name="flex items-center justify-between py-1.5",
            ),
            rx.el.div(
                rx.el.p(
                    "GST @ 18%",
                    class_name="text-[11px] text-gray-500",
                ),
                rx.el.p(
                    _inr(inv["gst_inr"]),
                    class_name="text-[13px] font-medium text-gray-900",
                ),
                class_name="flex items-center justify-between py-1.5",
            ),
            rx.el.div(
                rx.el.p(
                    "Total due",
                    class_name="text-[12px] font-semibold text-gray-700",
                ),
                rx.el.p(
                    _inr(inv["total_inr"]),
                    class_name="text-[16px] font-semibold text-gray-900",
                ),
                class_name="flex items-center justify-between pt-2 mt-1 border-t border-gray-100",
            ),
            class_name="mt-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(
                    "Issued " + inv["issued"],
                    class_name="text-[11.5px] text-gray-600",
                ),
                class_name="inline-flex items-center gap-1.5",
            ),
            rx.el.div(
                rx.icon("clock", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(
                    "Due " + inv["due"],
                    class_name="text-[11.5px] text-gray-600",
                ),
                class_name="inline-flex items-center gap-1.5",
            ),
            class_name="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1",
        ),
        class_name="p-5 rounded-xl border border-gray-200 bg-white",
    )


def _payment_form() -> rx.Component:
    inv = BillingState.my_open_invoice
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Confirm your payment",
                class_name="text-[15px] font-semibold text-gray-900",
            ),
            rx.el.p(
                rx.cond(
                    BillingState.is_india,
                    "Pay via UPI, NEFT/RTGS, or cheque and then confirm below. Our finance team reconciles within one business day.",
                    "Pay via international SWIFT wire, ACH, or cheque and then confirm below. Our finance team reconciles within one business day.",
                ),
                class_name="mt-1 text-[12.5px] text-gray-600",
            ),
            class_name="mb-4 pb-4 border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.p(
                "1. Choose payment method",
                class_name="text-[12px] font-semibold text-gray-700 mb-2",
            ),
            rx.el.div(
                rx.foreach(BillingState.method_options, _method_button_dynamic),
                class_name="flex flex-wrap items-center gap-2",
            ),
            rx.el.div(_payment_instructions(), class_name="mt-3"),
            class_name="mb-5",
        ),
        rx.el.div(
            rx.el.p(
                "2. Submit confirmation",
                class_name="text-[12px] font-semibold text-gray-700 mb-2",
            ),
            rx.cond(
                BillingState.submitted_invoice_id != "",
                rx.el.div(
                    rx.icon(
                        "circle-check",
                        class_name="h-5 w-5 text-emerald-600",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Payment submitted",
                            class_name="text-[14px] font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "Invoice "
                            + BillingState.submitted_invoice_id
                            + " is now marked awaiting confirmation. Our finance team will verify and issue a GST invoice within 1 business day.",
                            class_name="mt-1 text-[12.5px] text-gray-600 leading-relaxed",
                        ),
                        rx.el.button(
                            "Submit another payment",
                            on_click=BillingState.reset_submission,
                            class_name="mt-3 inline-flex items-center h-8 px-3 rounded-md border border-gray-200 bg-white text-[12.5px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
                        ),
                        class_name="flex flex-col min-w-0",
                    ),
                    class_name="flex items-start gap-3 p-4 rounded-md border border-emerald-100 bg-emerald-50/50",
                ),
                rx.el.form(
                    rx.el.input(
                        type="hidden",
                        name="invoice_id",
                        default_value=inv["id"],
                        key=inv["id"],
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Invoice",
                                class_name="text-[12px] font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    inv["id"] + " · " + _inr(inv["total_inr"]),
                                    class_name="text-[13px] font-semibold text-gray-900",
                                ),
                                class_name="h-9 px-3 rounded-md border border-gray-200 bg-gray-50 flex items-center",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Payment reference (UTR / UPI ref / cheque no.)",
                                class_name="text-[12px] font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="transaction_ref",
                                required=True,
                                placeholder="e.g. UPI 512874109223 or HDFC/NEFT/N...",
                                class_name="h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Billing email",
                                class_name="text-[12px] font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="billing_email",
                                type="email",
                                placeholder="finance@company.com",
                                default_value=inv["billing_email"],
                                key=inv["billing_email"],
                                class_name="h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.cond(
                            BillingState.is_india,
                            rx.el.div(
                                rx.el.label(
                                    rx.el.input(
                                        type="checkbox",
                                        name="gst_requested",
                                        class_name="h-4 w-4 rounded text-blue-600 border-gray-300 focus:ring-blue-500",
                                        default_value="true",
                                        key="true",
                                    ),
                                    rx.el.span(
                                        "Request GST invoice with GSTIN",
                                        class_name="text-[12.5px] font-medium text-gray-700",
                                    ),
                                    class_name="inline-flex items-center gap-2 cursor-pointer",
                                ),
                                rx.cond(
                                    BillingState.gst_requested,
                                    rx.el.input(
                                        name="gst_number",
                                        placeholder="15-digit GSTIN e.g. 29AAECA1234F1Z2",
                                        default_value=inv["gst_number"],
                                        key=inv["gst_number"],
                                        class_name="mt-2 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full font-mono",
                                    ),
                                    rx.fragment(),
                                ),
                                class_name="flex flex-col",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Tax invoice",
                                    class_name="text-[12px] font-semibold text-gray-700 mb-1",
                                ),
                                rx.el.p(
                                    "A "
                                    + BillingState.currency_code
                                    + " tax invoice will be issued to your billing email once payment is reconciled. VAT/withholding certificates available on request.",
                                    class_name="text-[11.5px] text-gray-500 leading-relaxed",
                                ),
                                class_name="flex flex-col p-2.5 rounded-md border border-gray-200 bg-gray-50/60",
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Notes (optional)",
                            class_name="text-[12px] font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.textarea(
                            name="notes",
                            rows=2,
                            placeholder="Anything our finance team should know (PO number, remitter name, etc.)",
                            class_name="p-2.5 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full resize-none",
                        ),
                        class_name="mt-3 flex flex-col",
                    ),
                    rx.cond(
                        BillingState.payment_error != "",
                        rx.el.div(
                            rx.icon(
                                "circle-alert",
                                class_name="h-3.5 w-3.5 text-red-600 mt-0.5 shrink-0",
                            ),
                            rx.el.p(
                                BillingState.payment_error,
                                class_name="text-[12.5px] text-red-700 leading-snug",
                            ),
                            class_name="mt-3 flex items-start gap-1.5 p-2.5 rounded-md border border-red-100 bg-red-50/70",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "By submitting, you confirm you've completed payment offline. No card details are stored — this workflow is Razorpay-ready for future one-click flows.",
                            class_name="text-[11.5px] text-gray-500 max-w-lg",
                        ),
                        rx.el.button(
                            rx.icon("send", class_name="h-3.5 w-3.5"),
                            "Confirm payment",
                            type="submit",
                            class_name="ml-auto inline-flex items-center gap-1.5 h-9 px-4 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
                        ),
                        class_name="mt-4 flex items-start gap-3 flex-wrap",
                    ),
                    on_submit=BillingState.submit_payment,
                    reset_on_submit=True,
                ),
            ),
        ),
        class_name="p-5 rounded-xl border border-gray-200 bg-white",
    )


def _plan_price_row(plan: str) -> rx.Component:
    price = PLAN_PRICING_INR[plan]["per_seat"]
    if price > 0:
        localized = rx.cond(
            BillingState.is_india,
            "₹" + str(price) + " / seat / month + 18% GST",
            BillingState.currency_symbol
            + (price / BillingState.currency_rate).to(int).to_string()
            + " / seat / month + local taxes if applicable",
        )
    else:
        localized = rx.Var.create("Custom — talk to sales")
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                plan,
                class_name="text-[13px] font-semibold text-gray-900",
            ),
            rx.cond(
                AuthState.current_company["plan"] == plan,
                rx.el.span(
                    "Current",
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
                ),
                rx.fragment(),
            ),
            class_name="flex items-center gap-1.5",
        ),
        rx.el.p(
            localized,
            class_name="text-[11.5px] text-gray-500 mt-0.5",
        ),
        class_name="flex flex-col py-2 border-b border-gray-100 last:border-b-0",
    )


def _upgrade_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Change your plan",
                class_name="text-[15px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Request an upgrade or downgrade. Our team will confirm and issue a pro-rated invoice.",
                class_name="mt-1 text-[12.5px] text-gray-600",
            ),
            class_name="mb-4 pb-4 border-b border-gray-100",
        ),
        rx.el.div(
            _plan_price_row("Starter"),
            _plan_price_row("Growth"),
            _plan_price_row("Enterprise"),
            class_name="mb-4",
        ),
        rx.cond(
            BillingState.has_pending_upgrade,
            rx.el.div(
                rx.icon(
                    "clock",
                    class_name="h-3.5 w-3.5 text-amber-600 mt-0.5 shrink-0",
                ),
                rx.el.p(
                    "You have a pending plan change request. Our team will confirm shortly.",
                    class_name="text-[12.5px] text-amber-800 leading-snug",
                ),
                class_name="flex items-start gap-1.5 p-2.5 rounded-md border border-amber-100 bg-amber-50/70",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Move to plan",
                            class_name="text-[12px] font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.div(
                            rx.el.select(
                                rx.el.option("Starter", value="Starter"),
                                rx.el.option("Growth", value="Growth"),
                                rx.el.option("Enterprise", value="Enterprise"),
                                name="requested_plan",
                                default_value="Growth",
                                class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
                            ),
                            rx.icon(
                                "chevron-down",
                                class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
                            ),
                            class_name="relative",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Seats",
                            class_name="text-[12px] font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="seats",
                            type="number",
                            min=1,
                            default_value="10",
                            class_name="h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="grid grid-cols-2 gap-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "Reason (optional)",
                        class_name="text-[12px] font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.textarea(
                        name="reason",
                        rows=2,
                        placeholder="Anything the team should know before confirming.",
                        class_name="p-2.5 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full resize-none",
                    ),
                    class_name="mt-3 flex flex-col",
                ),
                rx.el.button(
                    rx.icon("arrow-up-right", class_name="h-3.5 w-3.5"),
                    "Request plan change",
                    type="submit",
                    class_name="mt-4 inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                on_submit=BillingState.request_upgrade,
                reset_on_submit=True,
            ),
        ),
        class_name="p-5 rounded-xl border border-gray-200 bg-white",
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
                row["plan"] + " · " + row["seats"].to_string() + " seats",
                class_name="text-[12.5px] font-medium text-gray-800",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                _inr(row["total_inr"]),
                class_name="text-[13px] font-semibold text-gray-900",
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
            _status_pill(row["status"]), class_name="px-4 py-3 align-middle"
        ),
        rx.el.td(
            rx.el.p(
                row["issued"],
                class_name="text-[11.5px] text-gray-600",
            ),
            rx.el.p(
                "Due " + row["due"],
                class_name="text-[11px] text-gray-400",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50/60 transition-colors",
    )


def _invoices_table() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Invoice history",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Every invoice issued to your workspace",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-14 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Invoice", class_name=header_cls),
                        rx.el.th("Plan / seats", class_name=header_cls),
                        rx.el.th("Total", class_name=header_cls),
                        rx.el.th("Method", class_name=header_cls),
                        rx.el.th("Status", class_name=header_cls),
                        rx.el.th("Dates", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(rx.foreach(BillingState.my_invoices, _invoice_row)),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.cond(
            BillingState.my_invoices.length() == 0,
            rx.el.div(
                rx.icon("receipt", class_name="h-6 w-6 text-gray-300"),
                rx.el.p(
                    "No invoices yet",
                    class_name="mt-2 text-[13px] font-medium text-gray-700",
                ),
                class_name="flex flex-col items-center justify-center py-12 text-center",
            ),
            rx.fragment(),
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _upgrade_history() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Plan change requests",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "History of your upgrade and downgrade requests",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-14 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.cond(
            BillingState.my_upgrade_requests.length() == 0,
            rx.el.div(
                rx.icon("inbox", class_name="h-6 w-6 text-gray-300"),
                rx.el.p(
                    "No plan change requests yet",
                    class_name="mt-2 text-[13px] font-medium text-gray-700",
                ),
                class_name="flex flex-col items-center justify-center py-10 text-center",
            ),
            rx.el.div(
                rx.foreach(
                    BillingState.my_upgrade_requests,
                    lambda u: rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                u["current_plan"] + " → " + u["requested_plan"],
                                class_name="text-[13px] font-semibold text-gray-900",
                            ),
                            rx.el.p(
                                u["seats"].to_string()
                                + " seats · "
                                + u["requested_by"]
                                + " · "
                                + u["created"],
                                class_name="text-[11.5px] text-gray-500 mt-0.5",
                            ),
                            rx.cond(
                                u["reason"] != "",
                                rx.el.p(
                                    u["reason"],
                                    class_name="mt-1.5 text-[12px] text-gray-600 leading-snug",
                                ),
                                rx.fragment(),
                            ),
                            rx.cond(
                                u["admin_note"] != "",
                                rx.el.p(
                                    "Admin note: " + u["admin_note"],
                                    class_name="mt-1.5 text-[11.5px] text-blue-700 leading-snug",
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
                        class_name="flex items-start justify-between gap-3 p-4 border-t border-gray-100 first:border-t-0",
                    ),
                ),
                class_name="flex flex-col",
            ),
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _summary_stats() -> rx.Component:
    s = BillingState.my_billing_summary
    return rx.el.div(
        stat_card(
            "Current plan",
            AuthState.current_company["plan"],
            "Status: " + AuthState.current_company["status"],
            "badge-check",
        ),
        stat_card(
            "Outstanding",
            _inr(s["outstanding"]),
            "Across pending and overdue invoices",
            "wallet",
        ),
        stat_card(
            "Paid to date",
            _inr(s["total_paid"]),
            s["invoices_count"].to_string() + " invoices issued",
            "circle-check",
        ),
        stat_card(
            "Overdue",
            s["overdue_count"].to_string(),
            "Please clear to avoid service impact",
            "triangle-alert",
        ),
        class_name="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6",
    )


def _header_actions() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.icon("mail", class_name="h-3.5 w-3.5"),
            "Email finance",
            href="mailto:finance@contractops.ai",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
        ),
        rx.el.a(
            rx.icon("layout-grid", class_name="h-3.5 w-3.5"),
            "Workspace",
            href="/workspace",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
        ),
        class_name="flex items-center gap-2",
    )


def _future_provider_note() -> rx.Component:
    return rx.el.div(
        rx.icon(
            "info",
            class_name="h-3.5 w-3.5 text-blue-600 mt-0.5 shrink-0",
        ),
        rx.el.p(
            rx.cond(
                BillingState.is_india,
                "One-click UPI, netbanking, and cards are on our roadmap — no ContractOps workflows will change. Until then, all payments are manually confirmed by our finance team.",
                "One-click international card and wire flows are on our roadmap — no ContractOps workflows will change. Until then, all payments are manually confirmed by our finance team.",
            ),
            class_name="text-[12px] text-gray-700 leading-relaxed",
        ),
        class_name="mb-6 flex items-start gap-2 p-3 rounded-md border border-blue-100 bg-blue-50/40",
    )


def _country_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("globe", class_name="h-4 w-4 text-blue-600"),
                class_name="h-9 w-9 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    "Billing country",
                    class_name="text-[13px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    rx.cond(
                        BillingState.is_india,
                        "India-based workspaces are invoiced in INR with GST. Pay via UPI, NEFT/RTGS, or cheque.",
                        "International workspaces are invoiced in "
                        + BillingState.currency_code
                        + ". Pay via SWIFT wire, ACH, or cheque — GST does not apply.",
                    ),
                    class_name="text-[12px] text-gray-600 leading-relaxed mt-0.5",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-start gap-3 min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.label(
                "Country",
                class_name="text-[11px] font-semibold text-gray-700 mb-1",
            ),
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        BillingState.country_options,
                        lambda c: rx.el.option(c, value=c),
                    ),
                    default_value=BillingState.billing_country,
                    key=BillingState.billing_country,
                    on_change=BillingState.set_billing_country,
                    class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 min-w-[14rem]",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
                ),
                class_name="relative",
            ),
            rx.cond(
                ~BillingState.is_india,
                rx.el.p(
                    "Amounts converted from INR at the current display rate.",
                    class_name="mt-1.5 text-[10.5px] text-gray-500",
                ),
                rx.fragment(),
            ),
            class_name="flex flex-col shrink-0",
        ),
        class_name="mb-6 flex items-start justify-between gap-4 flex-wrap p-4 rounded-xl border border-gray-200 bg-white",
    )


def billing_page() -> rx.Component:
    return page_shell(
        "billing",
        rx.el.div(
            page_header(
                "Billing",
                rx.cond(
                    BillingState.is_india,
                    "Pay via UPI, NEFT/RTGS, or cheque. Request a GST invoice and manage plan changes here.",
                    "Pay via international SWIFT wire, ACH, or cheque. Manage plan changes here — GST is India-only.",
                ),
                _header_actions(),
            ),
            _country_card(),
            _future_provider_note(),
            _summary_stats(),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        _open_invoice_card(),
                        rx.el.div(_upgrade_card(), class_name="mt-4"),
                        class_name="flex flex-col",
                    ),
                    class_name="lg:col-span-5",
                ),
                rx.el.div(
                    _payment_form(),
                    class_name="lg:col-span-7",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-6",
            ),
            _invoices_table(),
            rx.el.div(_upgrade_history(), class_name="mt-4"),
        ),
    )
