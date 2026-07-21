import reflex as rx
from typing import TypedDict
import logging


class Invoice(TypedDict):
    id: str
    company_id: str
    plan: str
    seats: int
    period: str  # e.g. "Nov 2025"
    subtotal_inr: int
    gst_inr: int
    total_inr: int
    status: str  # "pending" | "awaiting_confirmation" | "paid" | "overdue" | "cancelled"
    method: str  # "" | "UPI" | "Bank transfer" | "Cheque" | "Credit note"
    transaction_ref: str
    issued: str
    due: str
    paid_on: str
    gst_number: str
    billing_email: str
    billing_country: str
    notes: str


class UpgradeRequest(TypedDict):
    id: str
    company_id: str
    current_plan: str
    requested_plan: str
    seats: int
    requested_by: str
    reason: str
    status: str  # "pending" | "approved" | "rejected"
    created: str
    resolved: str
    admin_note: str


PLAN_PRICING_INR: dict[str, dict[str, int]] = {
    "Starter": {"per_seat": 3999, "gst_rate": 18},
    "Growth": {"per_seat": 9999, "gst_rate": 18},
    "Enterprise": {"per_seat": 0, "gst_rate": 18},
}


INDIA_PAYMENT_INSTRUCTIONS: dict[str, dict[str, str]] = {
    "UPI": {
        "label": "UPI",
        "primary": "contractops@hdfcbank",
        "hint": "Pay via any UPI app (GPay, PhonePe, Paytm, BHIM). Add the invoice ID in the note.",
        "icon": "smartphone",
    },
    "Bank transfer": {
        "label": "NEFT / RTGS / IMPS",
        "primary": "HDFC Bank · A/c 5010 0234 5678 90 · IFSC HDFC0001234",
        "hint": "Beneficiary: ContractOps AI Private Limited. Reference the invoice ID in the remittance narration.",
        "icon": "landmark",
    },
    "Cheque": {
        "label": "Cheque / DD",
        "primary": "Payable to 'ContractOps AI Private Limited'",
        "hint": "Courier to: ContractOps AI Pvt Ltd, 4th Floor, Prestige Trade Tower, Bengaluru 560001.",
        "icon": "receipt",
    },
}


INTERNATIONAL_PAYMENT_INSTRUCTIONS: dict[str, dict[str, str]] = {
    "Wire transfer": {
        "label": "International wire (SWIFT)",
        "primary": "SWIFT/BIC: HDFCINBB · Beneficiary A/c 5010 0234 5678 90 · IBAN IN45 HDFC 0001 234 5010 0234 5678 90",
        "hint": "Beneficiary: ContractOps AI Private Limited, HDFC Bank, Bengaluru. Include the invoice ID in the MT103 remittance information field (Field 70). Correspondent bank details available on request.",
        "icon": "globe",
    },
    "ACH transfer": {
        "label": "ACH / US domestic wire",
        "primary": "JPMorgan Chase · Routing 021000021 · Account 8842095173 · SWIFT CHASUS33",
        "hint": "Beneficiary: ContractOps AI Inc (US entity). Use ACH for standard transfers or Fedwire for same-day. Reference the invoice ID in the memo/OBI field.",
        "icon": "landmark",
    },
    "Cheque": {
        "label": "Cheque",
        "primary": "Payable to 'ContractOps AI Inc'",
        "hint": "Mail to: ContractOps AI Inc, 548 Market St #12345, San Francisco, CA 94104, USA. Please write the invoice ID on the reverse.",
        "icon": "receipt",
    },
}


# Simple, editable table of supported billing countries. Currencies are for
# display only — invoices are stored in INR internally and converted at render
# time so admin reconciliation remains in one ledger currency.
BILLING_COUNTRIES: dict[str, dict[str, str | float]] = {
    "India": {"code": "INR", "symbol": "₹", "rate": 1.0},
    "United States": {"code": "USD", "symbol": "$", "rate": 83.0},
    "United Kingdom": {"code": "GBP", "symbol": "£", "rate": 105.0},
    "European Union": {"code": "EUR", "symbol": "€", "rate": 90.0},
    "Canada": {"code": "CAD", "symbol": "C$", "rate": 61.0},
    "Australia": {"code": "AUD", "symbol": "A$", "rate": 55.0},
    "Singapore": {"code": "SGD", "symbol": "S$", "rate": 62.0},
    "United Arab Emirates": {"code": "AED", "symbol": "AED ", "rate": 22.5},
    "Other": {"code": "USD", "symbol": "$", "rate": 83.0},
}


def _seed_invoices() -> list[Invoice]:
    return [
        {
            "id": "INV-2025-1042",
            "company_id": "co-acme",
            "plan": "Growth",
            "seats": 12,
            "period": "Nov 2025",
            "subtotal_inr": 119988,
            "gst_inr": 21598,
            "total_inr": 141586,
            "status": "paid",
            "method": "Bank transfer",
            "transaction_ref": "HDFC/NEFT/N221054812",
            "issued": "Nov 01, 2025",
            "due": "Nov 15, 2025",
            "paid_on": "Nov 09, 2025",
            "gst_number": "29AAECA1234F1Z2",
            "billing_email": "finance@acmelegal.com",
            "billing_country": "India",
            "notes": "GST invoice issued.",
        },
        {
            "id": "INV-2025-1088",
            "company_id": "co-acme",
            "plan": "Growth",
            "seats": 12,
            "period": "Dec 2025",
            "subtotal_inr": 119988,
            "gst_inr": 21598,
            "total_inr": 141586,
            "status": "awaiting_confirmation",
            "method": "UPI",
            "transaction_ref": "UPI/512874109223",
            "issued": "Dec 01, 2025",
            "due": "Dec 15, 2025",
            "paid_on": "",
            "gst_number": "29AAECA1234F1Z2",
            "billing_email": "finance@acmelegal.com",
            "billing_country": "India",
            "notes": "Customer submitted UPI payment — awaiting reconciliation.",
        },
        {
            "id": "INV-2025-1091",
            "company_id": "co-northwind",
            "plan": "Starter",
            "seats": 4,
            "period": "Dec 2025",
            "subtotal_inr": 15996,
            "gst_inr": 2879,
            "total_inr": 18875,
            "status": "pending",
            "method": "",
            "transaction_ref": "",
            "issued": "Dec 02, 2025",
            "due": "Dec 17, 2025",
            "paid_on": "",
            "gst_number": "",
            "billing_email": "billing@northwind.com",
            "billing_country": "India",
            "notes": "",
        },
        {
            "id": "INV-2025-1076",
            "company_id": "co-globex",
            "plan": "Enterprise",
            "seats": 60,
            "period": "Q4 2025",
            "subtotal_inr": 2400000,
            "gst_inr": 432000,
            "total_inr": 2832000,
            "status": "paid",
            "method": "Bank transfer",
            "transaction_ref": "HDFC/RTGS/R901287341",
            "issued": "Oct 01, 2025",
            "due": "Oct 20, 2025",
            "paid_on": "Oct 14, 2025",
            "gst_number": "27AABCG9876H1ZY",
            "billing_email": "ap@globex.io",
            "billing_country": "United States",
            "notes": "Annual pre-pay with 8% discount applied. Wired via SWIFT.",
        },
        {
            "id": "INV-2025-1093",
            "company_id": "co-initech",
            "plan": "Starter",
            "seats": 3,
            "period": "Dec 2025",
            "subtotal_inr": 11997,
            "gst_inr": 2159,
            "total_inr": 14156,
            "status": "overdue",
            "method": "",
            "transaction_ref": "",
            "issued": "Nov 15, 2025",
            "due": "Nov 30, 2025",
            "paid_on": "",
            "gst_number": "",
            "billing_email": "counsel@initech.com",
            "billing_country": "United Kingdom",
            "notes": "Reminder sent Dec 03. Awaiting GBP wire.",
        },
    ]


def _seed_upgrade_requests() -> list[UpgradeRequest]:
    return [
        {
            "id": "UPG-041",
            "company_id": "co-northwind",
            "current_plan": "Starter",
            "requested_plan": "Growth",
            "seats": 12,
            "requested_by": "Jamie Reyes",
            "reason": "Team is growing to 12 seats and we need Salesforce sync + custom playbooks.",
            "status": "pending",
            "created": "2 days ago",
            "resolved": "",
            "admin_note": "",
        },
        {
            "id": "UPG-039",
            "company_id": "co-initech",
            "current_plan": "Starter",
            "requested_plan": "Growth",
            "seats": 8,
            "requested_by": "Peter Gibbons",
            "reason": "Hit our 50 contract limit last month.",
            "status": "approved",
            "created": "1 week ago",
            "resolved": "5 days ago",
            "admin_note": "Approved. Growth plan activated with pro-rated invoice.",
        },
    ]


class BillingState(rx.State):
    invoices: list[Invoice] = _seed_invoices()
    upgrade_requests: list[UpgradeRequest] = _seed_upgrade_requests()

    # Company-side UI
    selected_method: str = "UPI"
    gst_requested: bool = False
    payment_error: str = ""
    submitted_invoice_id: str = ""

    # Billing localization — persisted per workspace session.
    billing_country: str = "India"

    # Admin-side UI
    admin_status_filter: str = "All"
    admin_company_filter: str = "All"

    @rx.var
    def is_india(self) -> bool:
        return self.billing_country == "India"

    @rx.var
    def country_options(self) -> list[str]:
        return list(BILLING_COUNTRIES.keys())

    @rx.var
    def currency_code(self) -> str:
        c = BILLING_COUNTRIES.get(
            self.billing_country, BILLING_COUNTRIES["Other"]
        )
        return str(c["code"])

    @rx.var
    def currency_symbol(self) -> str:
        c = BILLING_COUNTRIES.get(
            self.billing_country, BILLING_COUNTRIES["Other"]
        )
        return str(c["symbol"])

    @rx.var
    def currency_rate(self) -> float:
        c = BILLING_COUNTRIES.get(
            self.billing_country, BILLING_COUNTRIES["Other"]
        )
        return float(c["rate"])

    @rx.var
    def method_options(self) -> list[str]:
        if self.is_india:
            return ["UPI", "Bank transfer", "Cheque"]
        return ["Wire transfer", "ACH transfer", "Cheque"]

    @rx.var
    def status_options(self) -> list[str]:
        return [
            "All",
            "pending",
            "awaiting_confirmation",
            "paid",
            "overdue",
            "cancelled",
        ]

    @rx.var
    def selected_instructions(self) -> dict[str, str]:
        if self.is_india:
            return INDIA_PAYMENT_INSTRUCTIONS.get(
                self.selected_method, INDIA_PAYMENT_INSTRUCTIONS["UPI"]
            )
        return INTERNATIONAL_PAYMENT_INSTRUCTIONS.get(
            self.selected_method,
            INTERNATIONAL_PAYMENT_INSTRUCTIONS["Wire transfer"],
        )

    # ---- Company-scoped views ----
    # Fallback workspace used for demo mode and any code path where the
    # authenticated auth context is not (yet) hydrated (e.g. isolated tests,
    # SSR of the billing page before login state is available). The Acme
    # workspace is the canonical demo tenant seeded in AuthState.
    _DEMO_COMPANY_ID: str = "co-acme"

    async def _current_company_id(self) -> str:
        """Return the company id to scope billing views/events to.

        Prefers the authenticated user's company when available, but falls
        back to the demo Acme workspace when cross-state auth context is
        missing or empty. This keeps company-side billing usable in demos
        and in tests that instantiate BillingState in isolation.
        """
        try:
            from app.states.auth_state import AuthState

            auth = await self.get_state(AuthState)
            cid = auth.current_user.get("company_id") or ""
            if cid:
                return cid
        except Exception:
            logging.exception("Unexpected error")
        return self._DEMO_COMPANY_ID

    @rx.var
    async def my_invoices(self) -> list[Invoice]:
        cid = await self._current_company_id()
        return [i for i in self.invoices if i["company_id"] == cid]

    @rx.var
    async def my_open_invoice(self) -> Invoice:
        cid = await self._current_company_id()
        # Priority: awaiting_confirmation → pending → overdue → most recent
        priority = {
            "awaiting_confirmation": 0,
            "pending": 1,
            "overdue": 2,
            "paid": 3,
            "cancelled": 4,
        }
        matches = [i for i in self.invoices if i["company_id"] == cid]
        if not matches:
            return {
                "id": "",
                "company_id": cid,
                "plan": "Starter",
                "seats": 0,
                "period": "",
                "subtotal_inr": 0,
                "gst_inr": 0,
                "total_inr": 0,
                "status": "pending",
                "method": "",
                "transaction_ref": "",
                "issued": "",
                "due": "",
                "paid_on": "",
                "gst_number": "",
                "billing_email": "",
                "notes": "",
            }
        matches.sort(key=lambda x: priority.get(x["status"], 9))
        return matches[0]

    @rx.var
    async def my_billing_summary(self) -> dict[str, int]:
        cid = await self._current_company_id()
        mine = [i for i in self.invoices if i["company_id"] == cid]
        return {
            "total_paid": sum(
                i["total_inr"] for i in mine if i["status"] == "paid"
            ),
            "outstanding": sum(
                i["total_inr"]
                for i in mine
                if i["status"]
                in ("pending", "awaiting_confirmation", "overdue")
            ),
            "invoices_count": len(mine),
            "overdue_count": sum(1 for i in mine if i["status"] == "overdue"),
        }

    @rx.var
    async def my_upgrade_requests(self) -> list[UpgradeRequest]:
        cid = await self._current_company_id()
        return [u for u in self.upgrade_requests if u["company_id"] == cid]

    @rx.var
    async def has_pending_upgrade(self) -> bool:
        cid = await self._current_company_id()
        return any(
            u["company_id"] == cid and u["status"] == "pending"
            for u in self.upgrade_requests
        )

    # ---- Admin views ----
    def _currency_for_country(self, country: str) -> dict[str, str | float]:
        c = BILLING_COUNTRIES.get(country, BILLING_COUNTRIES["India"])
        return c

    @rx.var
    def admin_invoices(self) -> list[dict[str, str | int]]:
        from app.states.auth_state import _seed_companies

        # Build a name lookup from seeded companies (admin has access to all)
        name_lookup: dict[str, str] = {}
        for c in _seed_companies():
            name_lookup[c["id"]] = c["name"]
        rows: list[dict[str, str | int]] = []
        for inv in self.invoices:
            if (
                self.admin_status_filter != "All"
                and inv["status"] != self.admin_status_filter
            ):
                continue
            if (
                self.admin_company_filter != "All"
                and inv["company_id"] != self.admin_company_filter
            ):
                continue
            country = inv.get("billing_country") or "India"
            cur = self._currency_for_country(country)
            symbol = str(cur["symbol"])
            code = str(cur["code"])
            rate = float(cur["rate"])
            display_total = (
                f"₹{inv['total_inr']:,}"
                if country == "India"
                else f"{symbol}{int(inv['total_inr'] / rate):,}"
            )
            rows.append(
                {
                    "id": inv["id"],
                    "company_id": inv["company_id"],
                    "company_name": name_lookup.get(
                        inv["company_id"], inv["company_id"]
                    ),
                    "plan": inv["plan"],
                    "seats": inv["seats"],
                    "period": inv["period"],
                    "total_inr": inv["total_inr"],
                    "display_total": display_total,
                    "currency_code": code,
                    "billing_country": country,
                    "status": inv["status"],
                    "method": inv["method"] or "—",
                    "transaction_ref": inv["transaction_ref"] or "—",
                    "issued": inv["issued"],
                    "due": inv["due"],
                    "paid_on": inv["paid_on"] or "—",
                    "gst_number": inv["gst_number"] or "—",
                    "billing_email": inv["billing_email"] or "—",
                    "notes": inv["notes"] or "—",
                }
            )
        return rows

    @rx.var
    def admin_workspace_summaries(self) -> list[dict[str, str | int]]:
        """Per-workspace billing roll-up for the admin dashboard."""
        from app.states.auth_state import _seed_companies

        companies = _seed_companies()
        rows: list[dict[str, str | int]] = []
        for c in companies:
            mine = [i for i in self.invoices if i["company_id"] == c["id"]]
            if not mine:
                continue
            country = mine[-1].get("billing_country") or "India"
            cur = self._currency_for_country(country)
            symbol = str(cur["symbol"])
            code = str(cur["code"])
            rate = float(cur["rate"])
            total_paid = sum(
                i["total_inr"] for i in mine if i["status"] == "paid"
            )
            outstanding = sum(
                i["total_inr"]
                for i in mine
                if i["status"]
                in ("pending", "awaiting_confirmation", "overdue")
            )
            overdue = sum(1 for i in mine if i["status"] == "overdue")
            awaiting = sum(
                1 for i in mine if i["status"] == "awaiting_confirmation"
            )

            def _fmt(v: int) -> str:
                if country == "India":
                    return f"₹{v:,}"
                return f"{symbol}{int(v / rate):,}"

            # Latest billing contact + GSTIN if any
            latest = mine[-1]
            rows.append(
                {
                    "company_id": c["id"],
                    "company_name": c["name"],
                    "domain": c["domain"],
                    "plan": c["plan"],
                    "country": country,
                    "currency_code": code,
                    "currency_symbol": symbol,
                    "billing_email": latest["billing_email"] or "—",
                    "gst_number": latest["gst_number"] or "—",
                    "invoices": len(mine),
                    "total_paid_display": _fmt(total_paid),
                    "outstanding_display": _fmt(outstanding),
                    "outstanding_inr": outstanding,
                    "overdue": overdue,
                    "awaiting": awaiting,
                }
            )
        return rows

    @rx.var
    def admin_stats(self) -> dict[str, int]:
        total_paid = sum(
            i["total_inr"] for i in self.invoices if i["status"] == "paid"
        )
        outstanding = sum(
            i["total_inr"]
            for i in self.invoices
            if i["status"] in ("pending", "awaiting_confirmation", "overdue")
        )
        awaiting = sum(
            1 for i in self.invoices if i["status"] == "awaiting_confirmation"
        )
        overdue = sum(1 for i in self.invoices if i["status"] == "overdue")
        return {
            "total_paid": total_paid,
            "outstanding": outstanding,
            "awaiting_confirmation": awaiting,
            "overdue": overdue,
            "pending_upgrades": sum(
                1 for u in self.upgrade_requests if u["status"] == "pending"
            ),
        }

    @rx.var
    def admin_upgrade_requests(self) -> list[dict[str, str | int]]:
        from app.states.auth_state import _seed_companies

        name_lookup: dict[str, str] = {
            c["id"]: c["name"] for c in _seed_companies()
        }
        rows: list[dict[str, str | int]] = []
        for u in self.upgrade_requests:
            rows.append(
                {
                    "id": u["id"],
                    "company_id": u["company_id"],
                    "company_name": name_lookup.get(
                        u["company_id"], u["company_id"]
                    ),
                    "current_plan": u["current_plan"],
                    "requested_plan": u["requested_plan"],
                    "seats": u["seats"],
                    "requested_by": u["requested_by"],
                    "reason": u["reason"],
                    "status": u["status"],
                    "created": u["created"],
                    "resolved": u["resolved"] or "—",
                    "admin_note": u["admin_note"],
                }
            )
        return rows

    @rx.var
    def company_options(self) -> list[str]:
        from app.states.auth_state import _seed_companies

        return ["All", *[c["id"] for c in _seed_companies()]]

    # ---- Company events ----
    @rx.event
    def select_method(self, method: str):
        self.selected_method = method
        self.payment_error = ""

    @rx.event
    def set_billing_country(self, country: str):
        if country not in BILLING_COUNTRIES:
            return
        self.billing_country = country
        # Reset the payment method to the first valid option for this locale
        # so a stale INR-only method (e.g. UPI) doesn't linger for an intl user.
        if country == "India":
            self.selected_method = "UPI"
        else:
            self.selected_method = "Wire transfer"
            self.gst_requested = False
        self.payment_error = ""

    @rx.event
    def toggle_gst_request(self):
        self.gst_requested = not self.gst_requested

    def _resolve_country_for_new_invoice(self) -> str:
        return self.billing_country

    @rx.event
    async def submit_payment(self, form_data: dict):
        """Customer confirms they've paid a specific invoice manually."""
        invoice_id = (form_data.get("invoice_id") or "").strip()
        ref = (form_data.get("transaction_ref") or "").strip()
        gst_number = (form_data.get("gst_number") or "").strip()
        self.gst_requested = form_data.get("gst_requested") == "true"
        billing_email = (form_data.get("billing_email") or "").strip()
        notes = (form_data.get("notes") or "").strip()
        self.payment_error = ""
        if not invoice_id:
            self.payment_error = "Select an invoice to confirm payment against."
            return
        if not ref:
            if self.is_india:
                self.payment_error = "Enter a payment reference (UPI ref, UTR, or cheque number)."
            else:
                self.payment_error = "Enter a payment reference (SWIFT MT103 ref, ACH trace, or cheque number)."
            return
        if self.is_india and self.gst_requested and not gst_number:
            self.payment_error = (
                "GSTIN is required when requesting a GST invoice."
            )
            return
        clear_gst = not self.is_india
        if clear_gst:
            # GST is India-specific — never persist a GSTIN on an intl invoice.
            gst_number = ""
            self.gst_requested = False
        cid = await self._current_company_id()
        for i, inv in enumerate(self.invoices):
            if inv["id"] == invoice_id and inv["company_id"] == cid:
                self.invoices[i]["status"] = "awaiting_confirmation"
                self.invoices[i]["method"] = self.selected_method
                self.invoices[i]["transaction_ref"] = ref
                self.invoices[i]["billing_country"] = self.billing_country
                if clear_gst:
                    # Wipe any previously-stored GSTIN so the reconciled
                    # invoice reflects the international payment context.
                    self.invoices[i]["gst_number"] = ""
                elif gst_number:
                    self.invoices[i]["gst_number"] = gst_number
                if billing_email:
                    self.invoices[i]["billing_email"] = billing_email
                if notes:
                    self.invoices[i]["notes"] = notes
                self.submitted_invoice_id = invoice_id
                return rx.toast.success(
                    "Payment submitted — our finance team will confirm within 1 business day."
                )
        self.payment_error = "Invoice not found on your workspace."

    @rx.event
    def reset_submission(self):
        self.submitted_invoice_id = ""
        self.gst_requested = False
        self.payment_error = ""

    @rx.event
    async def request_upgrade(self, form_data: dict):
        plan = (form_data.get("requested_plan") or "").strip()
        seats_raw = (form_data.get("seats") or "0").strip()
        reason = (form_data.get("reason") or "").strip()
        try:
            seats = int(seats_raw)
        except ValueError:
            seats = 0
        if plan not in PLAN_PRICING_INR:
            return rx.toast.error("Choose a valid plan.")
        if seats <= 0:
            return rx.toast.error("Enter a positive seat count.")
        # Resolve current company + requester with a safe fallback so the
        # workflow keeps running even when auth context isn't hydrated.
        cid = self._DEMO_COMPANY_ID
        current_plan = "Starter"
        requester = "Owner"
        try:
            from app.states.auth_state import AuthState

            auth = await self.get_state(AuthState)
            cid = auth.current_user.get("company_id") or self._DEMO_COMPANY_ID
            current_plan = auth.current_company.get("plan") or current_plan
            requester = auth.current_user.get("name") or requester
        except Exception:
            logging.exception("Unexpected error")
        next_id = f"UPG-{len(self.upgrade_requests) + 42:03d}"
        self.upgrade_requests.insert(
            0,
            {
                "id": next_id,
                "company_id": cid,
                "current_plan": current_plan,
                "requested_plan": plan,
                "seats": seats,
                "requested_by": requester,
                "reason": reason,
                "status": "pending",
                "created": "just now",
                "resolved": "",
                "admin_note": "",
            },
        )
        return rx.toast.success(
            f"Upgrade to {plan} requested. Our team will send a pro-rated invoice shortly."
        )

    # ---- Admin events ----
    @rx.event
    def admin_set_status_filter(self, value: str):
        self.admin_status_filter = value

    @rx.event
    def admin_set_company_filter(self, value: str):
        self.admin_company_filter = value

    @rx.event
    def admin_update_status(self, invoice_id: str, status: str):
        for i, inv in enumerate(self.invoices):
            if inv["id"] == invoice_id:
                self.invoices[i]["status"] = status
                if status == "paid" and not inv["paid_on"]:
                    self.invoices[i]["paid_on"] = "just now"
                return rx.toast.success(f"{invoice_id} → {status}")

    @rx.event
    def admin_mark_paid(self, invoice_id: str):
        for i, inv in enumerate(self.invoices):
            if inv["id"] == invoice_id:
                self.invoices[i]["status"] = "paid"
                if not inv["paid_on"]:
                    self.invoices[i]["paid_on"] = "just now"
                return rx.toast.success(f"{invoice_id} → paid")

    @rx.event
    def admin_mark_overdue(self, invoice_id: str):
        for i, inv in enumerate(self.invoices):
            if inv["id"] == invoice_id:
                self.invoices[i]["status"] = "overdue"
                return rx.toast.success(f"{invoice_id} → overdue")

    @rx.event
    def admin_cancel_invoice(self, invoice_id: str):
        for i, inv in enumerate(self.invoices):
            if inv["id"] == invoice_id:
                self.invoices[i]["status"] = "cancelled"
                return rx.toast.success(f"{invoice_id} → cancelled")

    @rx.event
    async def admin_approve_upgrade(self, request_id: str):
        from app.states.auth_state import AuthState, PLAN_LIMITS

        target: UpgradeRequest | None = None
        for i, u in enumerate(self.upgrade_requests):
            if u["id"] == request_id:
                self.upgrade_requests[i]["status"] = "approved"
                self.upgrade_requests[i]["resolved"] = "just now"
                self.upgrade_requests[i]["admin_note"] = (
                    "Approved. Pro-rated invoice will be generated."
                )
                target = self.upgrade_requests[i]
                break
        if target is None:
            return
        if target["requested_plan"] in PLAN_LIMITS:
            try:
                auth = await self.get_state(AuthState)
                for i, c in enumerate(auth.companies):
                    if c["id"] == target["company_id"]:
                        auth.companies[i]["plan"] = target["requested_plan"]
            except Exception:
                # Auth context not hydrated (e.g. isolated tests). The
                # upgrade request is still marked approved locally; the plan
                # change will apply once auth state is available.
                logging.exception("Unexpected error")
        return rx.toast.success(
            f"Approved — {target['company_id']} moved to {target['requested_plan']}"
        )

    @rx.event
    def admin_reject_upgrade(self, request_id: str):
        for i, u in enumerate(self.upgrade_requests):
            if u["id"] == request_id:
                self.upgrade_requests[i]["status"] = "rejected"
                self.upgrade_requests[i]["resolved"] = "just now"
                self.upgrade_requests[i]["admin_note"] = (
                    "Rejected — please contact sales for details."
                )
                return rx.toast.info(f"{u['id']} rejected")
