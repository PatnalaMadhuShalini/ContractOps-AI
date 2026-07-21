import reflex as rx
from typing import TypedDict


class VolumePoint(TypedDict):
    label: str
    signed: int
    in_review: int


class TypeBreakdown(TypedDict):
    type: str
    count: int


class TeamRow(TypedDict):
    name: str
    initials: str
    role: str
    reviewed: int
    avg_hours: float
    approval_rate: int


class Counterparty(TypedDict):
    name: str
    contracts: int
    value: str
    risk: str


_PERIOD_DATA: dict[str, list[VolumePoint]] = {
    "7d": [
        {"label": "Mon", "signed": 6, "in_review": 3},
        {"label": "Tue", "signed": 9, "in_review": 5},
        {"label": "Wed", "signed": 11, "in_review": 4},
        {"label": "Thu", "signed": 8, "in_review": 7},
        {"label": "Fri", "signed": 14, "in_review": 6},
        {"label": "Sat", "signed": 2, "in_review": 1},
        {"label": "Sun", "signed": 1, "in_review": 2},
    ],
    "30d": [
        {"label": "W1", "signed": 42, "in_review": 18},
        {"label": "W2", "signed": 51, "in_review": 22},
        {"label": "W3", "signed": 47, "in_review": 19},
        {"label": "W4", "signed": 63, "in_review": 24},
    ],
    "90d": [
        {"label": "M1", "signed": 168, "in_review": 72},
        {"label": "M2", "signed": 204, "in_review": 84},
        {"label": "M3", "signed": 241, "in_review": 91},
    ],
    "ytd": [
        {"label": "Jan", "signed": 128, "in_review": 54},
        {"label": "Feb", "signed": 142, "in_review": 61},
        {"label": "Mar", "signed": 168, "in_review": 72},
        {"label": "Apr", "signed": 155, "in_review": 66},
        {"label": "May", "signed": 189, "in_review": 78},
        {"label": "Jun", "signed": 204, "in_review": 84},
        {"label": "Jul", "signed": 221, "in_review": 89},
        {"label": "Aug", "signed": 241, "in_review": 91},
    ],
}

_KPIS: dict[str, dict[str, str]] = {
    "7d": {"volume": "51", "cycle": "1.4d", "value": "$1.2M", "auto": "68%"},
    "30d": {"volume": "203", "cycle": "1.6d", "value": "$4.8M", "auto": "71%"},
    "90d": {"volume": "613", "cycle": "1.8d", "value": "$14.2M", "auto": "73%"},
    "ytd": {
        "volume": "1,448",
        "cycle": "2.1d",
        "value": "$32.7M",
        "auto": "70%",
    },
}


class AnalyticsState(rx.State):
    period: str = "30d"
    report_type: str = "overview"

    @rx.var
    def period_options(self) -> list[dict[str, str]]:
        return [
            {"key": "7d", "label": "Last 7 days"},
            {"key": "30d", "label": "Last 30 days"},
            {"key": "90d", "label": "Last 90 days"},
            {"key": "ytd", "label": "Year to date"},
        ]

    @rx.var
    def report_options(self) -> list[dict[str, str]]:
        return [
            {"key": "overview", "label": "Overview"},
            {"key": "cycle", "label": "Cycle time"},
            {"key": "volume", "label": "Volume by type"},
            {"key": "team", "label": "Team performance"},
        ]

    @rx.var
    def volume_data(self) -> list[VolumePoint]:
        return _PERIOD_DATA.get(self.period, _PERIOD_DATA["30d"])

    @rx.var
    def type_breakdown(self) -> list[TypeBreakdown]:
        multipliers = {"7d": 1, "30d": 4, "90d": 12, "ytd": 30}
        m = multipliers.get(self.period, 4)
        base = [
            {"type": "MSA", "count": 12 * m},
            {"type": "NDA", "count": 21 * m},
            {"type": "DPA", "count": 6 * m},
            {"type": "SOW", "count": 9 * m},
            {"type": "SaaS", "count": 8 * m},
            {"type": "Vendor", "count": 4 * m},
        ]
        return base

    @rx.var
    def kpis(self) -> dict[str, str]:
        return _KPIS.get(self.period, _KPIS["30d"])

    @rx.var
    def cycle_by_type(self) -> list[dict[str, str | float]]:
        return [
            {"type": "NDA", "hours": 3.2},
            {"type": "SOW", "hours": 14.5},
            {"type": "MSA", "hours": 36.8},
            {"type": "SaaS", "hours": 22.1},
            {"type": "DPA", "hours": 41.2},
        ]

    @rx.var
    def team(self) -> list[TeamRow]:
        return [
            {
                "name": "Sarah Reeves",
                "initials": "SR",
                "role": "General Counsel",
                "reviewed": 87,
                "avg_hours": 4.1,
                "approval_rate": 94,
            },
            {
                "name": "Alex Keller",
                "initials": "AK",
                "role": "Contract Manager",
                "reviewed": 142,
                "avg_hours": 2.8,
                "approval_rate": 91,
            },
            {
                "name": "Priya Shah",
                "initials": "PS",
                "role": "Legal Ops",
                "reviewed": 118,
                "avg_hours": 3.2,
                "approval_rate": 96,
            },
            {
                "name": "Marcus Lin",
                "initials": "ML",
                "role": "Privacy Counsel",
                "reviewed": 63,
                "avg_hours": 5.4,
                "approval_rate": 89,
            },
            {
                "name": "Jordan Pace",
                "initials": "JP",
                "role": "Finance",
                "reviewed": 41,
                "avg_hours": 2.1,
                "approval_rate": 98,
            },
        ]

    @rx.var
    def counterparties(self) -> list[Counterparty]:
        return [
            {
                "name": "Acme Corp",
                "contracts": 14,
                "value": "$1.2M",
                "risk": "Medium",
            },
            {
                "name": "Northwind Inc.",
                "contracts": 9,
                "value": "$680K",
                "risk": "Low",
            },
            {
                "name": "Globex Systems",
                "contracts": 7,
                "value": "$420K",
                "risk": "High",
            },
            {
                "name": "Umbrella Corp",
                "contracts": 6,
                "value": "$780K",
                "risk": "Low",
            },
            {
                "name": "Initech LLC",
                "contracts": 12,
                "value": "$540K",
                "risk": "Medium",
            },
            {
                "name": "Vandelay Industries",
                "contracts": 5,
                "value": "$340K",
                "risk": "Low",
            },
        ]

    @rx.event
    def set_period(self, value: str):
        self.period = value

    @rx.event
    def set_report(self, value: str):
        self.report_type = value

    @rx.event
    def export_report(self):
        return rx.toast.success(
            f"Exporting {self.report_type} report ({self.period}) as CSV"
        )

    @rx.event
    def schedule_report(self):
        return rx.toast.info(
            "Weekly email report scheduled for Mondays 9:00 AM"
        )
