import reflex as rx
from typing import TypedDict


class LeadNote(TypedDict):
    author: str
    body: str
    when: str


class Lead(TypedDict):
    id: str
    name: str
    initials: str
    email: str
    company: str
    phone: str
    team_size: str
    interest: str  # "demo" | "sales" | "trial"
    message: str
    source: str
    stage: str
    status: str  # "open" | "won" | "lost"
    priority: str  # "High" | "Medium" | "Low"
    owner: str
    created: str
    notes: list[LeadNote]


class EmailDraft(TypedDict):
    id: str
    lead_id: str
    template: str
    to_name: str
    to_email: str
    from_name: str
    from_email: str
    subject: str
    body: str
    created: str
    status: str  # "draft" | "sent"
    kind: str  # "external" | "internal"


LEAD_STAGES: list[str] = [
    "New",
    "Contacted",
    "Qualified",
    "Demo scheduled",
    "Proposal",
    "Won",
    "Lost",
]

LEAD_STATUSES: list[str] = ["open", "won", "lost"]

SALES_OWNERS: list[str] = [
    "Unassigned",
    "Sarah Reeves",
    "Alex Keller",
    "Jordan Pace",
    "Priya Shah",
]


def _initials(name: str) -> str:
    parts = [p for p in name.strip().split() if p]
    if not parts:
        return "L"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def _seed_leads() -> list[Lead]:
    return [
        {
            "id": "L-1042",
            "name": "Morgan Whitfield",
            "initials": "MW",
            "email": "morgan@brightlabs.io",
            "company": "Brightlabs",
            "phone": "+1 (415) 555-0142",
            "team_size": "50-200",
            "interest": "demo",
            "message": "Interested in replacing our email-based redline workflow. ~30 MSAs per month.",
            "source": "Website · Book a demo",
            "stage": "Demo scheduled",
            "status": "open",
            "priority": "High",
            "owner": "Sarah Reeves",
            "created": "12 min ago",
            "notes": [
                {
                    "author": "Sarah Reeves",
                    "body": "Confirmed demo for Thursday 2pm. Sending calendar invite.",
                    "when": "5 min ago",
                },
            ],
        },
        {
            "id": "L-1041",
            "name": "Devon Park",
            "initials": "DP",
            "email": "devon@northstack.ai",
            "company": "Northstack AI",
            "phone": "+1 (628) 555-0117",
            "team_size": "10-50",
            "interest": "sales",
            "message": "Do you support SOC 2 evidence for procurement? We're closing a large enterprise deal.",
            "source": "Website · Contact sales",
            "stage": "Contacted",
            "status": "open",
            "priority": "Medium",
            "owner": "Jordan Pace",
            "created": "2 hours ago",
            "notes": [],
        },
        {
            "id": "L-1039",
            "name": "Riya Menon",
            "initials": "RM",
            "email": "riya@planetscale.legal",
            "company": "Planetscale Legal",
            "phone": "+91 98765 40120",
            "team_size": "200-1000",
            "interest": "sales",
            "message": "Evaluating Ironclad vs. ContractOps. Need pricing for 40 seats + Salesforce sync.",
            "source": "Website · Contact sales",
            "stage": "Qualified",
            "status": "open",
            "priority": "High",
            "owner": "Sarah Reeves",
            "created": "Yesterday",
            "notes": [
                {
                    "author": "Sarah Reeves",
                    "body": "Sent enterprise pricing sheet. Follow up on Friday.",
                    "when": "Yesterday",
                },
            ],
        },
        {
            "id": "L-1035",
            "name": "Ellis Fontaine",
            "initials": "EF",
            "email": "ellis@vandelay.co",
            "company": "Vandelay Industries",
            "phone": "+44 20 7946 0195",
            "team_size": "10-50",
            "interest": "trial",
            "message": "Started free trial last week — how do we upload our playbook?",
            "source": "Website · Start free trial",
            "stage": "Proposal",
            "status": "open",
            "priority": "Medium",
            "owner": "Alex Keller",
            "created": "3 days ago",
            "notes": [
                {
                    "author": "Alex Keller",
                    "body": "Walked through playbook import. Sent proposal for Growth plan × 12 seats.",
                    "when": "2 days ago",
                },
            ],
        },
        {
            "id": "L-1032",
            "name": "Thea Okoro",
            "initials": "TO",
            "email": "thea@harborline.com",
            "company": "Harborline Shipping",
            "phone": "+1 (713) 555-0198",
            "team_size": "1000+",
            "interest": "demo",
            "message": "Global procurement team, 80+ jurisdictions. Need EU data residency.",
            "source": "Website · Book a demo",
            "stage": "Won",
            "status": "won",
            "priority": "High",
            "owner": "Sarah Reeves",
            "created": "1 week ago",
            "notes": [
                {
                    "author": "Sarah Reeves",
                    "body": "Signed Enterprise contract — $220K ARR. Kickoff Monday.",
                    "when": "2 days ago",
                },
            ],
        },
        {
            "id": "L-1028",
            "name": "Kai Fischer",
            "initials": "KF",
            "email": "kai@meridian.dev",
            "company": "Meridian Dev Co.",
            "phone": "+49 30 1234567",
            "team_size": "1-10",
            "interest": "sales",
            "message": "Too small for now — will revisit next year.",
            "source": "Website · Contact sales",
            "stage": "Lost",
            "status": "lost",
            "priority": "Low",
            "owner": "Jordan Pace",
            "created": "2 weeks ago",
            "notes": [],
        },
    ]


def _seed_drafts() -> list[EmailDraft]:
    return [
        {
            "id": "E-3021",
            "lead_id": "L-1042",
            "template": "Demo confirmation",
            "to_name": "Morgan Whitfield",
            "to_email": "morgan@brightlabs.io",
            "from_name": "Sarah Reeves",
            "from_email": "sarah@contractops.ai",
            "subject": "Your ContractOps AI demo — Thursday 2:00 PM PT",
            "body": (
                "Hi Morgan,\n\n"
                "Thanks for booking time with us — I'm looking forward to walking you through "
                "how ContractOps AI can compress your MSA review cycle from days to hours.\n\n"
                "I'll bring a live playbook demo tailored to a 50–200 person legal ops team, "
                "and we can dig into your ~30 MSAs/month workflow.\n\n"
                "Calendar invite is on its way. Reply here if you'd like to add anyone from your team.\n\n"
                "Best,\nSarah Reeves\nContractOps AI"
            ),
            "created": "5 min ago",
            "status": "draft",
            "kind": "external",
        },
        {
            "id": "E-3020",
            "lead_id": "L-1042",
            "template": "Internal alert",
            "to_name": "Sales team",
            "to_email": "sales@contractops.ai",
            "from_name": "ContractOps AI",
            "from_email": "no-reply@contractops.ai",
            "subject": "🔥 New demo request — Brightlabs (High priority)",
            "body": (
                "A new demo request just landed.\n\n"
                "Lead: Morgan Whitfield · morgan@brightlabs.io\n"
                "Company: Brightlabs (50–200 employees)\n"
                "Interest: Book a demo\n"
                "Priority: High\n\n"
                "Message: Interested in replacing our email-based redline workflow. ~30 MSAs per month.\n\n"
                "Assigned to: Sarah Reeves\n"
                "Open in CRM: /leads"
            ),
            "created": "12 min ago",
            "status": "draft",
            "kind": "internal",
        },
        {
            "id": "E-3018",
            "lead_id": "L-1041",
            "template": "Contact sales follow-up",
            "to_name": "Devon Park",
            "to_email": "devon@northstack.ai",
            "from_name": "Jordan Pace",
            "from_email": "jordan@contractops.ai",
            "subject": "Re: SOC 2 evidence for procurement",
            "body": (
                "Hi Devon,\n\n"
                "Great question — yes, we ship a full SOC 2 Type II report along with our "
                "trust center summary, and we can turn around a security questionnaire in under "
                "48 hours.\n\n"
                "I've attached our latest SOC 2 report and DPA. Happy to jump on a 20-minute call "
                "this week to walk through what your procurement team typically asks for.\n\n"
                "Best,\nJordan"
            ),
            "created": "1 hour ago",
            "status": "draft",
            "kind": "external",
        },
        {
            "id": "E-3015",
            "lead_id": "L-1039",
            "template": "Pricing proposal",
            "to_name": "Riya Menon",
            "to_email": "riya@planetscale.legal",
            "from_name": "Sarah Reeves",
            "from_email": "sarah@contractops.ai",
            "subject": "ContractOps AI — pricing for Planetscale Legal (40 seats)",
            "body": (
                "Hi Riya,\n\n"
                "As promised, here's a tailored proposal for Planetscale Legal:\n\n"
                "• 40 Growth seats @ $99/user/mo (annual) — $47,520/year\n"
                "• Native Salesforce sync — included\n"
                "• Custom playbook onboarding — included\n"
                "• Dedicated CSM — included at 40+ seats\n\n"
                "This comes in ~35% below the Ironclad quote you shared. Let's find 20 minutes "
                "on Friday to walk through it.\n\n"
                "Sarah"
            ),
            "created": "Yesterday",
            "status": "sent",
            "kind": "external",
        },
    ]


class CrmState(rx.State):
    leads: list[Lead] = _seed_leads()
    email_drafts: list[EmailDraft] = _seed_drafts()

    # Landing page submission state
    contact_submitted: bool = False
    demo_submitted: bool = False
    contact_error: str = ""
    demo_error: str = ""

    # Admin CRM UI state
    active_tab: str = "leads"
    selected_lead_id: str = "L-1042"
    stage_filter: str = "All"
    status_filter: str = "All"
    interest_filter: str = "All"
    search_query: str = ""
    lead_email_filter: str = "All"

    @rx.var
    def stage_options(self) -> list[str]:
        return ["All", *LEAD_STAGES]

    @rx.var
    def status_options(self) -> list[str]:
        return ["All", "open", "won", "lost"]

    @rx.var
    def interest_options(self) -> list[str]:
        return ["All", "demo", "sales", "trial"]

    @rx.var
    def stage_choices(self) -> list[str]:
        return LEAD_STAGES

    @rx.var
    def owner_choices(self) -> list[str]:
        return SALES_OWNERS

    @rx.var
    def filtered_leads(self) -> list[Lead]:
        q = self.search_query.lower().strip()
        out: list[Lead] = []
        for L in self.leads:
            if self.stage_filter != "All" and L["stage"] != self.stage_filter:
                continue
            if (
                self.status_filter != "All"
                and L["status"] != self.status_filter
            ):
                continue
            if (
                self.interest_filter != "All"
                and L["interest"] != self.interest_filter
            ):
                continue
            if (
                q
                and q not in L["name"].lower()
                and q not in L["company"].lower()
                and q not in L["email"].lower()
            ):
                continue
            out.append(L)
        return out

    @rx.var
    def selected_lead(self) -> Lead:
        for L in self.leads:
            if L["id"] == self.selected_lead_id:
                return L
        if len(self.leads) > 0:
            return self.leads[0]
        return {
            "id": "",
            "name": "—",
            "initials": "—",
            "email": "",
            "company": "",
            "phone": "",
            "team_size": "",
            "interest": "",
            "message": "",
            "source": "",
            "stage": "New",
            "status": "open",
            "priority": "Low",
            "owner": "Unassigned",
            "created": "",
            "notes": [],
        }

    @rx.var
    def selected_lead_drafts(self) -> list[EmailDraft]:
        return [
            d
            for d in self.email_drafts
            if d["lead_id"] == self.selected_lead_id
        ]

    @rx.var
    def filtered_drafts(self) -> list[EmailDraft]:
        if self.lead_email_filter == "All":
            return self.email_drafts
        return [
            d
            for d in self.email_drafts
            if d["status"] == self.lead_email_filter
        ]

    @rx.var
    def stats(self) -> dict[str, int]:
        new_count = sum(1 for L in self.leads if L["stage"] == "New")
        open_count = sum(1 for L in self.leads if L["status"] == "open")
        won_count = sum(1 for L in self.leads if L["status"] == "won")
        drafts_count = sum(
            1 for d in self.email_drafts if d["status"] == "draft"
        )
        return {
            "total": len(self.leads),
            "new": new_count,
            "open": open_count,
            "won": won_count,
            "drafts": drafts_count,
        }

    @rx.var
    def pipeline_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {s: 0 for s in LEAD_STAGES}
        for L in self.leads:
            if L["stage"] in counts:
                counts[L["stage"]] = counts[L["stage"]] + 1
        return counts

    # ---- Landing page capture ----
    def _next_lead_id(self) -> str:
        n = 1042 + len(self.leads)
        while any(L["id"] == f"L-{n}" for L in self.leads):
            n += 1
        return f"L-{n}"

    def _next_draft_id(self) -> str:
        n = 3022 + len(self.email_drafts)
        while any(d["id"] == f"E-{n}" for d in self.email_drafts):
            n += 1
        return f"E-{n}"

    def _prepare_emails(self, lead: Lead) -> None:
        """Prepare external ack + internal alert email drafts for a new lead."""
        if lead["interest"] == "demo":
            subject_ext = "Your ContractOps AI demo — we'll be in touch shortly"
            body_ext = (
                f"Hi {lead['name'].split()[0]},\n\n"
                "Thanks for requesting a demo of ContractOps AI. A member of our team will "
                "reach out within one business day to schedule a time that works for you.\n\n"
                "In the meantime, feel free to explore our product tour: "
                "https://contractops.ai/product\n\n"
                "Best,\nThe ContractOps AI team"
            )
            internal_subject = f"🔥 New demo request — {lead['company']}"
        elif lead["interest"] == "trial":
            subject_ext = "Welcome to your ContractOps AI trial"
            body_ext = (
                f"Hi {lead['name'].split()[0]},\n\n"
                "Your 14-day free trial of ContractOps AI is ready. We've provisioned a "
                "workspace for you — check your inbox for login details.\n\n"
                "Have questions? Just reply to this email.\n\n"
                "Best,\nThe ContractOps AI team"
            )
            internal_subject = f"🎉 New trial started — {lead['company']}"
        else:
            subject_ext = "Thanks for reaching out to ContractOps AI"
            body_ext = (
                f"Hi {lead['name'].split()[0]},\n\n"
                "Thanks for getting in touch. Someone from our sales team will follow up "
                "within one business day with pricing details and next steps.\n\n"
                "Best,\nThe ContractOps AI team"
            )
            internal_subject = f"📩 New sales inquiry — {lead['company']}"
        # External ack
        self.email_drafts.append(
            {
                "id": self._next_draft_id(),
                "lead_id": lead["id"],
                "template": "Auto-acknowledgement",
                "to_name": lead["name"],
                "to_email": lead["email"],
                "from_name": "ContractOps AI",
                "from_email": "hello@contractops.ai",
                "subject": subject_ext,
                "body": body_ext,
                "created": "just now",
                "status": "draft",
                "kind": "external",
            }
        )
        # Internal alert
        self.email_drafts.append(
            {
                "id": self._next_draft_id(),
                "lead_id": lead["id"],
                "template": "Internal alert",
                "to_name": "Sales team",
                "to_email": "sales@contractops.ai",
                "from_name": "ContractOps AI",
                "from_email": "no-reply@contractops.ai",
                "subject": internal_subject,
                "body": (
                    f"A new lead just landed from the website.\n\n"
                    f"Lead: {lead['name']} · {lead['email']}\n"
                    f"Company: {lead['company']} ({lead['team_size'] or 'size not specified'})\n"
                    f"Interest: {lead['interest']}\n"
                    f"Priority: {lead['priority']}\n"
                    f"Source: {lead['source']}\n\n"
                    f"Message:\n{lead['message'] or '(no message provided)'}\n\n"
                    f"Open in CRM: /leads"
                ),
                "created": "just now",
                "status": "draft",
                "kind": "internal",
            }
        )

    def _create_lead(
        self, form_data: dict, interest: str, source: str
    ) -> Lead | None:
        name = (form_data.get("name") or "").strip()
        email = (form_data.get("email") or "").strip().lower()
        company = (form_data.get("company") or "").strip()
        phone = (form_data.get("phone") or "").strip()
        team_size = (form_data.get("team_size") or "").strip()
        message = (form_data.get("message") or "").strip()
        if not name or not email or not company:
            return None
        priority = "Medium"
        if team_size in ("200-1000", "1000+"):
            priority = "High"
        elif team_size == "1-10":
            priority = "Low"
        lead: Lead = {
            "id": self._next_lead_id(),
            "name": name,
            "initials": _initials(name),
            "email": email,
            "company": company,
            "phone": phone,
            "team_size": team_size or "—",
            "interest": interest,
            "message": message,
            "source": source,
            "stage": "New",
            "status": "open",
            "priority": priority,
            "owner": "Unassigned",
            "created": "just now",
            "notes": [],
        }
        self.leads.insert(0, lead)
        self._prepare_emails(lead)
        return lead

    @rx.event
    def submit_contact(self, form_data: dict):
        self.contact_error = ""
        lead = self._create_lead(
            form_data, interest="sales", source="Website · Contact sales"
        )
        if lead is None:
            self.contact_error = (
                "Please fill in your name, work email, and company."
            )
            return
        self.contact_submitted = True
        return rx.toast.success(
            "Thanks! We'll be in touch within one business day."
        )

    @rx.event
    def submit_demo(self, form_data: dict):
        self.demo_error = ""
        lead = self._create_lead(
            form_data, interest="demo", source="Website · Book a demo"
        )
        if lead is None:
            self.demo_error = (
                "Please fill in your name, work email, and company."
            )
            return
        self.demo_submitted = True
        return rx.toast.success("Demo requested — check your inbox shortly.")

    @rx.event
    def reset_contact_form(self):
        self.contact_submitted = False
        self.contact_error = ""

    @rx.event
    def reset_demo_form(self):
        self.demo_submitted = False
        self.demo_error = ""

    # ---- Admin CRM events ----
    @rx.event
    def set_tab(self, key: str):
        self.active_tab = key

    @rx.event
    def select_lead(self, lead_id: str):
        self.selected_lead_id = lead_id

    @rx.event
    def set_stage_filter(self, value: str):
        self.stage_filter = value

    @rx.event
    def set_status_filter(self, value: str):
        self.status_filter = value

    @rx.event
    def set_interest_filter(self, value: str):
        self.interest_filter = value

    @rx.event
    def set_search(self, value: str):
        self.search_query = value

    @rx.event
    def set_email_filter(self, value: str):
        self.lead_email_filter = value

    @rx.event
    def reset_filters(self):
        self.stage_filter = "All"
        self.status_filter = "All"
        self.interest_filter = "All"
        self.search_query = ""

    @rx.event
    def update_stage(self, lead_id: str, stage: str):
        if stage not in LEAD_STAGES:
            return
        for i, L in enumerate(self.leads):
            if L["id"] == lead_id:
                self.leads[i]["stage"] = stage
                if stage == "Won":
                    self.leads[i]["status"] = "won"
                elif stage == "Lost":
                    self.leads[i]["status"] = "lost"
                else:
                    self.leads[i]["status"] = "open"
                return rx.toast.success(f"{lead_id} → {stage}")

    @rx.event
    def update_status(self, lead_id: str, status: str):
        if status not in LEAD_STATUSES:
            return
        for i, L in enumerate(self.leads):
            if L["id"] == lead_id:
                self.leads[i]["status"] = status
                if status == "won":
                    self.leads[i]["stage"] = "Won"
                elif status == "lost":
                    self.leads[i]["stage"] = "Lost"
                return rx.toast.info(f"{lead_id} marked {status}")

    @rx.event
    def assign_owner(self, lead_id: str, owner: str):
        for i, L in enumerate(self.leads):
            if L["id"] == lead_id:
                self.leads[i]["owner"] = owner
                return rx.toast.success(f"Assigned to {owner}")

    @rx.event
    def add_note(self, form_data: dict):
        body = (form_data.get("note") or "").strip()
        if not body:
            return
        for i, L in enumerate(self.leads):
            if L["id"] == self.selected_lead_id:
                self.leads[i]["notes"] = [
                    {
                        "author": "Platform Admin",
                        "body": body,
                        "when": "just now",
                    },
                    *L["notes"],
                ]
                return rx.toast.success("Note added")

    @rx.event
    def delete_lead(self, lead_id: str):
        self.leads = [L for L in self.leads if L["id"] != lead_id]
        self.email_drafts = [
            d for d in self.email_drafts if d["lead_id"] != lead_id
        ]
        if self.selected_lead_id == lead_id and self.leads:
            self.selected_lead_id = self.leads[0]["id"]
        return rx.toast.info(f"Deleted {lead_id}")

    @rx.event
    def mark_email_sent(self, email_id: str):
        for i, d in enumerate(self.email_drafts):
            if d["id"] == email_id:
                self.email_drafts[i]["status"] = "sent"
                return rx.toast.success("Marked as sent")

    @rx.event
    def mark_email_draft(self, email_id: str):
        for i, d in enumerate(self.email_drafts):
            if d["id"] == email_id:
                self.email_drafts[i]["status"] = "draft"
                return rx.toast.info("Reverted to draft")

    @rx.event
    def delete_email(self, email_id: str):
        self.email_drafts = [
            d for d in self.email_drafts if d["id"] != email_id
        ]
        return rx.toast.info("Draft deleted")

    @rx.event
    def copy_email(self, email_id: str):
        for d in self.email_drafts:
            if d["id"] == email_id:
                payload = f"To: {d['to_email']}\nSubject: {d['subject']}\n\n{d['body']}"
                return [
                    rx.set_clipboard(payload),
                    rx.toast.success("Email copied to clipboard"),
                ]
