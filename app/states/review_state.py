import reflex as rx
from typing import TypedDict


class KeyTerm(TypedDict):
    label: str
    value: str
    icon: str
    confidence: int


class Clause(TypedDict):
    id: str
    title: str
    category: str
    risk: str
    playbook_status: str
    excerpt: str
    playbook_standard: str
    suggested_redline: str
    rationale: str


class ActivityEntry(TypedDict):
    actor: str
    action: str
    when: str
    icon: str


class Contract(TypedDict):
    id: str
    title: str
    counterparty: str
    type: str
    value: str
    owner: str
    owner_initials: str
    updated: str
    stage: str
    risk_score: int
    priority: str
    playbook: str
    pages: int
    key_terms: list[KeyTerm]
    clauses: list[Clause]
    activity: list[ActivityEntry]


STAGES: list[str] = ["Intake", "AI Review", "Approval", "Signed"]


def _sample_contracts() -> list[Contract]:
    return [
        {
            "id": "acme-msa-v3",
            "title": "Acme MSA — Vendor v3",
            "counterparty": "Acme Corp",
            "type": "MSA",
            "value": "$480,000 ARR",
            "owner": "Alex Keller",
            "owner_initials": "AK",
            "updated": "2m ago",
            "stage": "AI Review",
            "risk_score": 62,
            "priority": "Medium",
            "playbook": "Enterprise SaaS",
            "pages": 42,
            "key_terms": [
                {
                    "label": "Contract value",
                    "value": "$480,000 / year",
                    "icon": "circle-dollar-sign",
                    "confidence": 98,
                },
                {
                    "label": "Term",
                    "value": "24 months",
                    "icon": "calendar",
                    "confidence": 96,
                },
                {
                    "label": "Auto-renewal",
                    "value": "Yes — no notice window",
                    "icon": "repeat",
                    "confidence": 91,
                },
                {
                    "label": "Governing law",
                    "value": "Delaware",
                    "icon": "landmark",
                    "confidence": 99,
                },
                {
                    "label": "Liability cap",
                    "value": "6 months of fees",
                    "icon": "shield",
                    "confidence": 94,
                },
                {
                    "label": "Payment terms",
                    "value": "Net 45",
                    "icon": "wallet",
                    "confidence": 97,
                },
                {
                    "label": "Data processing",
                    "value": "DPA v2.1 attached",
                    "icon": "database",
                    "confidence": 92,
                },
                {
                    "label": "Termination",
                    "value": "For convenience, 90 days",
                    "icon": "log-out",
                    "confidence": 95,
                },
            ],
            "clauses": [
                {
                    "id": "c1",
                    "title": "Limitation of liability",
                    "category": "Liability",
                    "risk": "High",
                    "playbook_status": "Deviates",
                    "excerpt": "Provider's aggregate liability shall not exceed the fees paid in the six (6) months preceding the claim.",
                    "playbook_standard": "Liability cap should be at least 12 months of fees; carve-outs required for IP indemnity and confidentiality.",
                    "suggested_redline": "…shall not exceed the fees paid in the twelve (12) months preceding the claim, excluding claims arising from breach of confidentiality, IP indemnification, or gross negligence.",
                    "rationale": "6-month cap is below playbook minimum. Recommend counter to 12 months with standard carve-outs.",
                },
                {
                    "id": "c2",
                    "title": "Auto-renewal",
                    "category": "Term",
                    "risk": "High",
                    "playbook_status": "Deviates",
                    "excerpt": "This Agreement shall automatically renew for successive one-year terms unless terminated by either party.",
                    "playbook_standard": "Auto-renewal requires 60-day written notice window before renewal date.",
                    "suggested_redline": "…automatically renew for successive one-year terms unless either party provides written notice of non-renewal at least sixty (60) days before the end of the then-current term.",
                    "rationale": "No notice window creates unbounded commitment risk. Insert 60-day notice per playbook.",
                },
                {
                    "id": "c3",
                    "title": "Governing law",
                    "category": "Jurisdiction",
                    "risk": "Low",
                    "playbook_status": "Matches",
                    "excerpt": "This Agreement shall be governed by the laws of the State of Delaware.",
                    "playbook_standard": "Delaware, New York, or California acceptable.",
                    "suggested_redline": "",
                    "rationale": "Matches standard playbook. Auto-approved.",
                },
                {
                    "id": "c4",
                    "title": "Payment terms",
                    "category": "Commercial",
                    "risk": "Medium",
                    "playbook_status": "Deviates",
                    "excerpt": "Customer shall pay all undisputed invoices within forty-five (45) days of receipt.",
                    "playbook_standard": "Net 30 preferred; Net 45 acceptable only for enterprise deals >$250K ARR.",
                    "suggested_redline": "",
                    "rationale": "Net 45 acceptable for this deal size — flagged for visibility only.",
                },
                {
                    "id": "c5",
                    "title": "Confidentiality",
                    "category": "IP & Data",
                    "risk": "Low",
                    "playbook_status": "Matches",
                    "excerpt": "Each party agrees to hold in confidence all Confidential Information for a period of five (5) years.",
                    "playbook_standard": "Minimum 3 years; trade secrets in perpetuity.",
                    "suggested_redline": "",
                    "rationale": "Exceeds playbook minimum. No action required.",
                },
                {
                    "id": "c6",
                    "title": "Data processing addendum",
                    "category": "IP & Data",
                    "risk": "Medium",
                    "playbook_status": "Review",
                    "excerpt": "The parties agree to the Data Processing Addendum attached as Exhibit B.",
                    "playbook_standard": "DPA must reference GDPR Art. 28 obligations and current SCCs.",
                    "suggested_redline": "",
                    "rationale": "Exhibit B references SCCs from 2010 — request update to 2021 EU SCCs.",
                },
            ],
            "activity": [
                {
                    "actor": "ContractOps AI",
                    "action": "Completed clause review · 6 findings",
                    "when": "2m ago",
                    "icon": "sparkles",
                },
                {
                    "actor": "Alex Keller",
                    "action": "Uploaded Acme MSA — Vendor v3.docx",
                    "when": "4m ago",
                    "icon": "upload",
                },
                {
                    "actor": "Salesforce",
                    "action": "Linked opportunity #OPP-4821",
                    "when": "12m ago",
                    "icon": "link",
                },
            ],
        },
        {
            "id": "northwind-nda",
            "title": "Northwind NDA — mutual",
            "counterparty": "Northwind Inc.",
            "type": "NDA",
            "value": "—",
            "owner": "Priya Shah",
            "owner_initials": "PS",
            "updated": "18m ago",
            "stage": "AI Review",
            "risk_score": 84,
            "priority": "Low",
            "playbook": "Standard NDA",
            "pages": 6,
            "key_terms": [
                {
                    "label": "Type",
                    "value": "Mutual",
                    "icon": "arrow-left-right",
                    "confidence": 99,
                },
                {
                    "label": "Term",
                    "value": "3 years",
                    "icon": "calendar",
                    "confidence": 98,
                },
                {
                    "label": "Governing law",
                    "value": "New York",
                    "icon": "landmark",
                    "confidence": 99,
                },
                {
                    "label": "Residual clause",
                    "value": "Not present",
                    "icon": "circle-check",
                    "confidence": 96,
                },
            ],
            "clauses": [
                {
                    "id": "n1",
                    "title": "Term of confidentiality",
                    "category": "IP & Data",
                    "risk": "Low",
                    "playbook_status": "Matches",
                    "excerpt": "Confidentiality obligations survive for three (3) years after disclosure.",
                    "playbook_standard": "Minimum 3 years for mutual NDAs.",
                    "suggested_redline": "",
                    "rationale": "Matches playbook.",
                },
                {
                    "id": "n2",
                    "title": "Governing law",
                    "category": "Jurisdiction",
                    "risk": "Low",
                    "playbook_status": "Matches",
                    "excerpt": "Governed by laws of the State of New York.",
                    "playbook_standard": "NY, DE, CA acceptable.",
                    "suggested_redline": "",
                    "rationale": "Standard.",
                },
                {
                    "id": "n3",
                    "title": "Injunctive relief",
                    "category": "Liability",
                    "risk": "Low",
                    "playbook_status": "Matches",
                    "excerpt": "Either party may seek injunctive relief without posting bond.",
                    "playbook_standard": "Injunctive relief permitted.",
                    "suggested_redline": "",
                    "rationale": "Matches standard.",
                },
            ],
            "activity": [
                {
                    "actor": "ContractOps AI",
                    "action": "Completed clause review · 0 findings",
                    "when": "18m ago",
                    "icon": "sparkles",
                },
                {
                    "actor": "Priya Shah",
                    "action": "Forwarded from legal@northwind.com",
                    "when": "22m ago",
                    "icon": "mail",
                },
            ],
        },
        {
            "id": "globex-dpa",
            "title": "Globex DPA — 2024 addendum",
            "counterparty": "Globex Systems",
            "type": "DPA",
            "value": "—",
            "owner": "Marcus Lin",
            "owner_initials": "ML",
            "updated": "1h ago",
            "stage": "Approval",
            "risk_score": 41,
            "priority": "High",
            "playbook": "GDPR Processor",
            "pages": 18,
            "key_terms": [
                {
                    "label": "Sub-processors",
                    "value": "12 listed",
                    "icon": "users",
                    "confidence": 93,
                },
                {
                    "label": "Data transfers",
                    "value": "EU → US via SCCs",
                    "icon": "globe",
                    "confidence": 89,
                },
                {
                    "label": "Breach notice",
                    "value": "72 hours",
                    "icon": "bell",
                    "confidence": 97,
                },
                {
                    "label": "Audit rights",
                    "value": "Once per year, 30-day notice",
                    "icon": "clipboard-check",
                    "confidence": 95,
                },
            ],
            "clauses": [
                {
                    "id": "g1",
                    "title": "Sub-processor consent",
                    "category": "IP & Data",
                    "risk": "High",
                    "playbook_status": "Deviates",
                    "excerpt": "Processor may engage sub-processors without prior notice to Controller.",
                    "playbook_standard": "Sub-processors require 30-day prior written notice with right to object.",
                    "suggested_redline": "Processor shall provide Controller with at least thirty (30) days' prior written notice of any new sub-processor, with Controller's right to object on reasonable grounds.",
                    "rationale": "No notice violates GDPR Art. 28(2). Redline required before approval.",
                },
                {
                    "id": "g2",
                    "title": "Data breach notification",
                    "category": "IP & Data",
                    "risk": "Medium",
                    "playbook_status": "Review",
                    "excerpt": "Processor shall notify Controller of a personal data breach within seventy-two (72) hours.",
                    "playbook_standard": "Notify without undue delay and no later than 48 hours.",
                    "suggested_redline": "…within forty-eight (48) hours of becoming aware of a personal data breach.",
                    "rationale": "Playbook is stricter than GDPR baseline — propose 48 hours.",
                },
                {
                    "id": "g3",
                    "title": "International transfers",
                    "category": "IP & Data",
                    "risk": "High",
                    "playbook_status": "Deviates",
                    "excerpt": "Transfers shall rely on the 2010 Standard Contractual Clauses.",
                    "playbook_standard": "Use 2021 EU SCCs (Module 2 for processor transfers).",
                    "suggested_redline": "Transfers shall rely on the 2021 Standard Contractual Clauses adopted by the European Commission (Module 2).",
                    "rationale": "2010 SCCs are invalid post-Schrems II. Must be updated.",
                },
            ],
            "activity": [
                {
                    "actor": "Marcus Lin",
                    "action": "Requested GC review",
                    "when": "45m ago",
                    "icon": "user-check",
                },
                {
                    "actor": "ContractOps AI",
                    "action": "Completed clause review · 3 findings",
                    "when": "1h ago",
                    "icon": "sparkles",
                },
            ],
        },
        {
            "id": "initech-sow",
            "title": "Initech SOW — Q4 renewal",
            "counterparty": "Initech LLC",
            "type": "SOW",
            "value": "$92,000",
            "owner": "Alex Keller",
            "owner_initials": "AK",
            "updated": "3h ago",
            "stage": "Intake",
            "risk_score": 78,
            "priority": "Low",
            "playbook": "Professional Services",
            "pages": 9,
            "key_terms": [
                {
                    "label": "Contract value",
                    "value": "$92,000",
                    "icon": "circle-dollar-sign",
                    "confidence": 99,
                },
                {
                    "label": "Term",
                    "value": "Q4 2025 (3 months)",
                    "icon": "calendar",
                    "confidence": 98,
                },
                {
                    "label": "Deliverables",
                    "value": "4 milestones",
                    "icon": "list-checks",
                    "confidence": 96,
                },
                {
                    "label": "Payment terms",
                    "value": "Net 30",
                    "icon": "wallet",
                    "confidence": 99,
                },
            ],
            "clauses": [
                {
                    "id": "i1",
                    "title": "Acceptance testing",
                    "category": "Commercial",
                    "risk": "Low",
                    "playbook_status": "Matches",
                    "excerpt": "Customer has 15 business days to accept or reject each deliverable.",
                    "playbook_standard": "10–15 business day acceptance window acceptable.",
                    "suggested_redline": "",
                    "rationale": "Standard SOW acceptance term.",
                },
                {
                    "id": "i2",
                    "title": "Change orders",
                    "category": "Commercial",
                    "risk": "Low",
                    "playbook_status": "Matches",
                    "excerpt": "Any scope changes require a mutually signed change order.",
                    "playbook_standard": "Change orders must be in writing and signed.",
                    "suggested_redline": "",
                    "rationale": "Matches playbook.",
                },
            ],
            "activity": [
                {
                    "actor": "Alex Keller",
                    "action": "Uploaded Initech SOW — Q4.pdf",
                    "when": "3h ago",
                    "icon": "upload",
                },
            ],
        },
        {
            "id": "umbrella-saas",
            "title": "Umbrella SaaS agreement",
            "counterparty": "Umbrella Corp",
            "type": "SaaS",
            "value": "$210,000 ARR",
            "owner": "Priya Shah",
            "owner_initials": "PS",
            "updated": "Yesterday",
            "stage": "Signed",
            "risk_score": 91,
            "priority": "Low",
            "playbook": "Enterprise SaaS",
            "pages": 28,
            "key_terms": [
                {
                    "label": "Contract value",
                    "value": "$210,000 / year",
                    "icon": "circle-dollar-sign",
                    "confidence": 99,
                },
                {
                    "label": "Term",
                    "value": "12 months",
                    "icon": "calendar",
                    "confidence": 99,
                },
                {
                    "label": "SLA",
                    "value": "99.9% uptime",
                    "icon": "activity",
                    "confidence": 97,
                },
                {
                    "label": "Signed",
                    "value": "Countersigned yesterday",
                    "icon": "circle-check",
                    "confidence": 100,
                },
            ],
            "clauses": [
                {
                    "id": "u1",
                    "title": "Service level agreement",
                    "category": "Commercial",
                    "risk": "Low",
                    "playbook_status": "Matches",
                    "excerpt": "Provider commits to 99.9% monthly uptime with service credits for downtime.",
                    "playbook_standard": "Minimum 99.5% uptime with service credits.",
                    "suggested_redline": "",
                    "rationale": "Exceeds playbook minimum.",
                },
            ],
            "activity": [
                {
                    "actor": "DocuSign",
                    "action": "Contract countersigned",
                    "when": "Yesterday",
                    "icon": "circle-check",
                },
                {
                    "actor": "Priya Shah",
                    "action": "Approved and sent for signature",
                    "when": "2 days ago",
                    "icon": "user-check",
                },
            ],
        },
    ]


class ReviewState(rx.State):
    contracts: list[Contract] = _sample_contracts()
    selected_id: str = "acme-msa-v3"
    filter_type: str = "All"
    filter_stage: str = "All"
    search_query: str = ""
    active_tab: str = "terms"
    accepted_clauses: list[str] = []
    rejected_clauses: list[str] = []
    upload_files: list[str] = []
    is_uploading: bool = False

    @rx.var
    def contract_types(self) -> list[str]:
        return ["All", "MSA", "NDA", "DPA", "SOW", "SaaS"]

    @rx.var
    def stage_options(self) -> list[str]:
        return ["All", "Intake", "AI Review", "Approval", "Signed"]

    @rx.var
    def filtered_contracts(self) -> list[Contract]:
        q = self.search_query.lower().strip()
        out: list[Contract] = []
        for c in self.contracts:
            if self.filter_type != "All" and c["type"] != self.filter_type:
                continue
            if self.filter_stage != "All" and c["stage"] != self.filter_stage:
                continue
            if (
                q
                and q not in c["title"].lower()
                and q not in c["counterparty"].lower()
            ):
                continue
            out.append(c)
        return out

    @rx.var
    def selected(self) -> Contract:
        for c in self.contracts:
            if c["id"] == self.selected_id:
                return c
        return self.contracts[0]

    @rx.var
    def stage_index(self) -> int:
        stage = self.selected["stage"]
        if stage in STAGES:
            return STAGES.index(stage)
        return 0

    @rx.var
    def clause_counts(self) -> dict[str, int]:
        counts = {
            "High": 0,
            "Medium": 0,
            "Low": 0,
            "Deviates": 0,
            "Matches": 0,
            "Review": 0,
        }
        for cl in self.selected["clauses"]:
            counts[cl["risk"]] = counts.get(cl["risk"], 0) + 1
            counts[cl["playbook_status"]] = (
                counts.get(cl["playbook_status"], 0) + 1
            )
        return counts

    @rx.var
    def total_clauses(self) -> int:
        return len(self.selected["clauses"])

    @rx.var
    def playbook_match_pct(self) -> int:
        total = len(self.selected["clauses"])
        if total == 0:
            return 100
        matches = sum(
            1
            for cl in self.selected["clauses"]
            if cl["playbook_status"] == "Matches"
        )
        return round(matches * 100 / total)

    @rx.event
    def select_contract(self, contract_id: str):
        self.selected_id = contract_id
        self.active_tab = "terms"

    @rx.event
    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def set_type_filter(self, value: str):
        self.filter_type = value

    @rx.event
    def set_stage_filter(self, value: str):
        self.filter_stage = value

    @rx.event
    def set_search(self, value: str):
        self.search_query = value

    @rx.event
    def accept_clause(self, clause_id: str):
        if clause_id in self.rejected_clauses:
            self.rejected_clauses.remove(clause_id)
        if clause_id in self.accepted_clauses:
            self.accepted_clauses.remove(clause_id)
        else:
            self.accepted_clauses.append(clause_id)

    @rx.event
    def reject_clause(self, clause_id: str):
        if clause_id in self.accepted_clauses:
            self.accepted_clauses.remove(clause_id)
        if clause_id in self.rejected_clauses:
            self.rejected_clauses.remove(clause_id)
        else:
            self.rejected_clauses.append(clause_id)

    @rx.event
    def advance_stage(self):
        idx = (
            STAGES.index(self.selected["stage"])
            if self.selected["stage"] in STAGES
            else 0
        )
        if idx < len(STAGES) - 1:
            for i, c in enumerate(self.contracts):
                if c["id"] == self.selected_id:
                    self.contracts[i]["stage"] = STAGES[idx + 1]
                    self.contracts[i]["updated"] = "just now"
                    return rx.toast.success(f"Moved to {STAGES[idx + 1]}")
        return rx.toast.info("Already at final stage")

    @rx.event
    def send_for_signature(self):
        for i, c in enumerate(self.contracts):
            if c["id"] == self.selected_id:
                self.contracts[i]["stage"] = "Signed"
                self.contracts[i]["updated"] = "just now"
        return rx.toast.success("Sent for e-signature via DocuSign")

    @rx.event
    def request_changes(self):
        return rx.toast.info("Redline sent to counterparty")

    @rx.event
    def approve_all(self):
        ids = [cl["id"] for cl in self.selected["clauses"]]
        self.accepted_clauses = list({*self.accepted_clauses, *ids})
        self.rejected_clauses = [
            x for x in self.rejected_clauses if x not in ids
        ]
        return rx.toast.success("All AI suggestions accepted")

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_uploading = True
        for file in files:
            data = await file.read()
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            path = upload_dir / file.name
            with path.open("wb") as f:
                f.write(data)
            self.upload_files.append(file.name)
        self.is_uploading = False
        return rx.toast.success(
            f"Uploaded {len(files)} file(s) — AI review queued"
        )

    @rx.event
    def clear_uploads(self):
        self.upload_files = []
