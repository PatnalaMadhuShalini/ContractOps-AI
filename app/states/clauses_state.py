import reflex as rx
from typing import TypedDict


class ClauseTemplate(TypedDict):
    id: str
    title: str
    category: str
    description: str
    body: str
    usage_count: int
    risk_level: str
    last_updated: str
    author: str
    tags: list[str]


def _seed() -> list[ClauseTemplate]:
    return [
        {
            "id": "cl-lim-01",
            "title": "Limitation of liability — 12 months (standard)",
            "category": "Liability",
            "description": "Standard mutual liability cap at 12 months of fees with carve-outs for IP, confidentiality, and gross negligence.",
            "body": "EXCEPT FOR BREACHES OF CONFIDENTIALITY, INDEMNIFICATION OBLIGATIONS, OR GROSS NEGLIGENCE OR WILLFUL MISCONDUCT, EACH PARTY'S AGGREGATE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT SHALL NOT EXCEED THE FEES PAID OR PAYABLE BY CUSTOMER TO PROVIDER IN THE TWELVE (12) MONTHS PRECEDING THE EVENT GIVING RISE TO THE CLAIM.",
            "usage_count": 184,
            "risk_level": "Low",
            "last_updated": "3 days ago",
            "author": "Sarah Reeves",
            "tags": ["MSA", "SaaS", "Enterprise"],
        },
        {
            "id": "cl-lim-02",
            "title": "Liability cap fallback — 6 months (approved deviation)",
            "category": "Liability",
            "description": "Pre-approved fallback for SMB deals under $50K ARR when counterparty rejects 12-month cap.",
            "body": "Provider's aggregate liability shall not exceed the fees paid in the six (6) months preceding the claim, provided that this limitation shall not apply to breaches of Section 8 (Confidentiality) or Section 9 (Indemnification).",
            "usage_count": 42,
            "risk_level": "Medium",
            "last_updated": "1 week ago",
            "author": "Sarah Reeves",
            "tags": ["SMB", "Fallback"],
        },
        {
            "id": "cl-ren-01",
            "title": "Auto-renewal with 60-day notice",
            "category": "Term",
            "description": "Standard auto-renewal with a 60-day non-renewal notice window and no price increase caps.",
            "body": "This Agreement shall automatically renew for successive one-year terms unless either party provides written notice of non-renewal at least sixty (60) days prior to the end of the then-current term.",
            "usage_count": 261,
            "risk_level": "Low",
            "last_updated": "2 weeks ago",
            "author": "Alex Keller",
            "tags": ["MSA", "SaaS"],
        },
        {
            "id": "cl-gov-01",
            "title": "Governing law — Delaware",
            "category": "Jurisdiction",
            "description": "Default governing law and exclusive venue in Delaware.",
            "body": "This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to conflict-of-law principles. The parties consent to the exclusive jurisdiction of the state and federal courts located in Wilmington, Delaware.",
            "usage_count": 312,
            "risk_level": "Low",
            "last_updated": "1 month ago",
            "author": "Sarah Reeves",
            "tags": ["Standard"],
        },
        {
            "id": "cl-gov-02",
            "title": "Governing law — New York",
            "category": "Jurisdiction",
            "description": "Alternate governing law for East-coast enterprise customers.",
            "body": "This Agreement shall be governed by the laws of the State of New York. The parties consent to the exclusive jurisdiction of the courts located in New York County, New York.",
            "usage_count": 88,
            "risk_level": "Low",
            "last_updated": "1 month ago",
            "author": "Sarah Reeves",
            "tags": ["Alternate"],
        },
        {
            "id": "cl-conf-01",
            "title": "Confidentiality — 3 year mutual",
            "category": "IP & Data",
            "description": "Standard mutual confidentiality clause with 3-year survival and trade-secret carve-out.",
            "body": "Each party agrees to hold the other party's Confidential Information in strict confidence for a period of three (3) years from disclosure; trade secrets shall be protected for as long as they qualify as such under applicable law.",
            "usage_count": 297,
            "risk_level": "Low",
            "last_updated": "2 weeks ago",
            "author": "Priya Shah",
            "tags": ["NDA", "MSA"],
        },
        {
            "id": "cl-dpa-01",
            "title": "GDPR sub-processor consent",
            "category": "IP & Data",
            "description": "Processor must give 30-day prior written notice of new sub-processors with right to object.",
            "body": "Processor shall provide Controller with at least thirty (30) days' prior written notice of any new sub-processor, and Controller shall have the right to object on reasonable grounds. If Controller objects and the parties cannot agree on a resolution, Controller may terminate the applicable Order.",
            "usage_count": 74,
            "risk_level": "Medium",
            "last_updated": "5 days ago",
            "author": "Marcus Lin",
            "tags": ["DPA", "GDPR"],
        },
        {
            "id": "cl-dpa-02",
            "title": "2021 EU SCCs — Module 2",
            "category": "IP & Data",
            "description": "Reference to 2021 EU Standard Contractual Clauses for controller-to-processor transfers.",
            "body": "International transfers of Personal Data shall be governed by the Standard Contractual Clauses adopted by the European Commission on 4 June 2021 (2021/914), Module 2 (Controller-to-Processor).",
            "usage_count": 58,
            "risk_level": "Medium",
            "last_updated": "5 days ago",
            "author": "Marcus Lin",
            "tags": ["DPA", "GDPR", "SCCs"],
        },
        {
            "id": "cl-pay-01",
            "title": "Payment terms — Net 30",
            "category": "Commercial",
            "description": "Default payment terms for standard commercial deals.",
            "body": "Customer shall pay all undisputed invoices within thirty (30) days of the invoice date. Late payments shall accrue interest at 1.5% per month or the maximum rate permitted by law, whichever is lower.",
            "usage_count": 341,
            "risk_level": "Low",
            "last_updated": "3 weeks ago",
            "author": "Jordan Pace",
            "tags": ["Standard"],
        },
        {
            "id": "cl-pay-02",
            "title": "Payment terms — Net 45 (enterprise)",
            "category": "Commercial",
            "description": "Extended payment terms for enterprise deals over $250K ARR.",
            "body": "Customer shall pay all undisputed invoices within forty-five (45) days of the invoice date. This payment schedule applies only to Orders with an annual contract value of $250,000 or greater.",
            "usage_count": 68,
            "risk_level": "Medium",
            "last_updated": "3 weeks ago",
            "author": "Jordan Pace",
            "tags": ["Enterprise"],
        },
        {
            "id": "cl-term-01",
            "title": "Termination for convenience — 90 days",
            "category": "Term",
            "description": "Standard mutual termination for convenience with 90 days written notice.",
            "body": "Either party may terminate this Agreement for convenience upon ninety (90) days prior written notice to the other party. Upon such termination, Customer shall pay all fees accrued through the effective date of termination.",
            "usage_count": 129,
            "risk_level": "Low",
            "last_updated": "2 weeks ago",
            "author": "Alex Keller",
            "tags": ["MSA"],
        },
        {
            "id": "cl-ip-01",
            "title": "IP ownership — customer data",
            "category": "IP & Data",
            "description": "Customer retains all rights to customer data; provider owns product IP.",
            "body": "As between the parties, Customer retains all right, title, and interest in and to Customer Data. Provider retains all right, title, and interest in and to the Services, including all improvements, derivatives, and modifications thereto.",
            "usage_count": 218,
            "risk_level": "Low",
            "last_updated": "1 month ago",
            "author": "Sarah Reeves",
            "tags": ["MSA", "SaaS"],
        },
    ]


class ClausesState(rx.State):
    templates: list[ClauseTemplate] = _seed()
    search_query: str = ""
    category_filter: str = "All"
    selected_id: str = "cl-lim-01"
    copied_id: str = ""

    @rx.var
    def categories(self) -> list[str]:
        return [
            "All",
            "Liability",
            "Term",
            "Jurisdiction",
            "IP & Data",
            "Commercial",
        ]

    @rx.var
    def category_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {"All": len(self.templates)}
        for t in self.templates:
            counts[t["category"]] = counts.get(t["category"], 0) + 1
        return counts

    @rx.var
    def filtered(self) -> list[ClauseTemplate]:
        q = self.search_query.lower().strip()
        out: list[ClauseTemplate] = []
        for t in self.templates:
            if (
                self.category_filter != "All"
                and t["category"] != self.category_filter
            ):
                continue
            if (
                q
                and q not in t["title"].lower()
                and q not in t["description"].lower()
                and q not in t["body"].lower()
            ):
                continue
            out.append(t)
        return out

    @rx.var
    def selected(self) -> ClauseTemplate:
        for t in self.templates:
            if t["id"] == self.selected_id:
                return t
        return self.templates[0]

    @rx.var
    def total_usage(self) -> int:
        return sum(t["usage_count"] for t in self.templates)

    @rx.event
    def set_search(self, value: str):
        self.search_query = value

    @rx.event
    def set_category(self, value: str):
        self.category_filter = value

    @rx.event
    def select(self, clause_id: str):
        self.selected_id = clause_id
        self.copied_id = ""

    @rx.event
    def copy_clause(self, clause_id: str):
        self.copied_id = clause_id
        return rx.toast.success("Clause copied to clipboard")

    @rx.event
    def insert_clause(self, clause_id: str):
        for i, t in enumerate(self.templates):
            if t["id"] == clause_id:
                self.templates[i]["usage_count"] = t["usage_count"] + 1
                return rx.toast.success(f"Inserted into active contract")
        return rx.toast.error("Clause not found")
