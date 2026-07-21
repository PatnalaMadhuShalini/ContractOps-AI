import reflex as rx
from typing import TypedDict


class Approval(TypedDict):
    id: str
    contract: str
    counterparty: str
    type: str
    value: str
    requester: str
    requester_initials: str
    approver: str
    approver_initials: str
    priority: str
    reason: str
    requested: str
    status: str
    stage: str


def _seed() -> list[Approval]:
    return [
        {
            "id": "APR-1042",
            "contract": "Acme MSA — Vendor v3",
            "counterparty": "Acme Corp",
            "type": "MSA",
            "value": "$480,000 ARR",
            "requester": "Alex Keller",
            "requester_initials": "AK",
            "approver": "Sarah Reeves",
            "approver_initials": "SR",
            "priority": "High",
            "reason": "Liability cap deviates from playbook (6mo vs 12mo)",
            "requested": "12 min ago",
            "status": "Pending",
            "stage": "GC review",
        },
        {
            "id": "APR-1041",
            "contract": "Globex DPA — 2024 addendum",
            "counterparty": "Globex Systems",
            "type": "DPA",
            "value": "—",
            "requester": "Marcus Lin",
            "requester_initials": "ML",
            "approver": "Sarah Reeves",
            "approver_initials": "SR",
            "priority": "High",
            "reason": "Sub-processor consent missing; 2010 SCCs referenced",
            "requested": "45 min ago",
            "status": "Pending",
            "stage": "GC review",
        },
        {
            "id": "APR-1039",
            "contract": "Initech SOW — Q4 renewal",
            "counterparty": "Initech LLC",
            "type": "SOW",
            "value": "$92,000",
            "requester": "Alex Keller",
            "requester_initials": "AK",
            "approver": "Jordan Pace",
            "approver_initials": "JP",
            "priority": "Medium",
            "reason": "Payment terms — Net 45 vs. standard Net 30",
            "requested": "3 hours ago",
            "status": "Pending",
            "stage": "Finance review",
        },
        {
            "id": "APR-1036",
            "contract": "Umbrella SaaS agreement",
            "counterparty": "Umbrella Corp",
            "type": "SaaS",
            "value": "$210,000 ARR",
            "requester": "Priya Shah",
            "requester_initials": "PS",
            "approver": "Sarah Reeves",
            "approver_initials": "SR",
            "priority": "Low",
            "reason": "Standard playbook — routine sign-off",
            "requested": "Yesterday",
            "status": "Approved",
            "stage": "Approved",
        },
        {
            "id": "APR-1035",
            "contract": "Vandelay MSA renewal",
            "counterparty": "Vandelay Industries",
            "type": "MSA",
            "value": "$340,000 ARR",
            "requester": "Priya Shah",
            "requester_initials": "PS",
            "approver": "Sarah Reeves",
            "approver_initials": "SR",
            "priority": "Medium",
            "reason": "Indemnification carve-outs requested",
            "requested": "2 days ago",
            "status": "Approved",
            "stage": "Approved",
        },
        {
            "id": "APR-1033",
            "contract": "Soylent NDA — mutual",
            "counterparty": "Soylent Foods",
            "type": "NDA",
            "value": "—",
            "requester": "Marcus Lin",
            "requester_initials": "ML",
            "approver": "Jordan Pace",
            "approver_initials": "JP",
            "priority": "Low",
            "reason": "Term extended to 5 years",
            "requested": "3 days ago",
            "status": "Rejected",
            "stage": "Sent back",
        },
        {
            "id": "APR-1029",
            "contract": "Northwind NDA — mutual",
            "counterparty": "Northwind Inc.",
            "type": "NDA",
            "value": "—",
            "requester": "Priya Shah",
            "requester_initials": "PS",
            "approver": "Auto-approved",
            "approver_initials": "AI",
            "priority": "Low",
            "reason": "Matches standard playbook — no deviations",
            "requested": "4 days ago",
            "status": "Approved",
            "stage": "Auto-approved",
        },
    ]


class ApprovalsState(rx.State):
    approvals: list[Approval] = _seed()
    status_filter: str = "All"
    priority_filter: str = "All"
    type_filter: str = "All"
    search_query: str = ""

    @rx.var
    def status_options(self) -> list[str]:
        return ["All", "Pending", "Approved", "Rejected"]

    @rx.var
    def priority_options(self) -> list[str]:
        return ["All", "High", "Medium", "Low"]

    @rx.var
    def type_options(self) -> list[str]:
        return ["All", "MSA", "NDA", "DPA", "SOW", "SaaS"]

    @rx.var
    def filtered(self) -> list[Approval]:
        q = self.search_query.lower().strip()
        out: list[Approval] = []
        for a in self.approvals:
            if (
                self.status_filter != "All"
                and a["status"] != self.status_filter
            ):
                continue
            if (
                self.priority_filter != "All"
                and a["priority"] != self.priority_filter
            ):
                continue
            if self.type_filter != "All" and a["type"] != self.type_filter:
                continue
            if (
                q
                and q not in a["contract"].lower()
                and q not in a["counterparty"].lower()
                and q not in a["requester"].lower()
            ):
                continue
            out.append(a)
        return out

    @rx.var
    def pending_count(self) -> int:
        return sum(1 for a in self.approvals if a["status"] == "Pending")

    @rx.var
    def urgent_count(self) -> int:
        return sum(
            1
            for a in self.approvals
            if a["status"] == "Pending" and a["priority"] == "High"
        )

    @rx.var
    def approved_this_week(self) -> int:
        return sum(1 for a in self.approvals if a["status"] == "Approved")

    @rx.var
    def rejected_count(self) -> int:
        return sum(1 for a in self.approvals if a["status"] == "Rejected")

    @rx.event
    def set_status(self, value: str):
        self.status_filter = value

    @rx.event
    def set_priority(self, value: str):
        self.priority_filter = value

    @rx.event
    def set_type(self, value: str):
        self.type_filter = value

    @rx.event
    def set_search(self, value: str):
        self.search_query = value

    @rx.event
    def approve(self, approval_id: str):
        for i, a in enumerate(self.approvals):
            if a["id"] == approval_id:
                self.approvals[i]["status"] = "Approved"
                self.approvals[i]["stage"] = "Approved"
                self.approvals[i]["requested"] = "just now"
                return rx.toast.success(f"Approved {approval_id}")
        return rx.toast.error("Approval not found")

    @rx.event
    def reject(self, approval_id: str):
        for i, a in enumerate(self.approvals):
            if a["id"] == approval_id:
                self.approvals[i]["status"] = "Rejected"
                self.approvals[i]["stage"] = "Sent back"
                self.approvals[i]["requested"] = "just now"
                return rx.toast.info(f"Sent {approval_id} back to requester")
        return rx.toast.error("Approval not found")

    @rx.event
    def reset_filters(self):
        self.status_filter = "All"
        self.priority_filter = "All"
        self.type_filter = "All"
        self.search_query = ""
