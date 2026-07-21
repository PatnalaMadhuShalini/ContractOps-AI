import reflex as rx
from typing import TypedDict


class Integration(TypedDict):
    name: str
    description: str
    icon: str
    connected: bool


class ApiKey(TypedDict):
    name: str
    prefix: str
    created: str
    last_used: str


class SettingsState(rx.State):
    active_section: str = "profile"

    # Profile
    full_name: str = "Alex Keller"
    email: str = "alex@acmelegal.com"
    role: str = "Contract Manager"
    timezone: str = "America/New_York"

    # Company
    company_name: str = "Acme Legal"
    company_domain: str = "acmelegal.com"
    default_playbook: str = "Enterprise SaaS"
    default_governing_law: str = "Delaware"
    fiscal_year_start: str = "January"

    # Notifications
    notify_pending_approvals: bool = True
    notify_high_risk: bool = True
    notify_renewals: bool = True
    notify_weekly_digest: bool = False
    notify_slack_mentions: bool = True
    email_frequency: str = "Immediate"

    # Security
    require_2fa: bool = True
    session_timeout: str = "8 hours"
    ip_allowlist_enabled: bool = False

    # Integrations
    integrations: list[Integration] = [
        {
            "name": "Salesforce",
            "description": "Sync contracts with opportunities",
            "icon": "cloud",
            "connected": True,
        },
        {
            "name": "Google Drive",
            "description": "Ingest contracts from shared folders",
            "icon": "hard-drive",
            "connected": True,
        },
        {
            "name": "DocuSign",
            "description": "Native e-signature workflows",
            "icon": "pen-tool",
            "connected": True,
        },
        {
            "name": "Slack",
            "description": "Contract intake and approval requests",
            "icon": "message-square",
            "connected": True,
        },
        {
            "name": "Microsoft 365",
            "description": "Ingest contracts from Outlook and OneDrive",
            "icon": "mail",
            "connected": False,
        },
        {
            "name": "Ironclad",
            "description": "Two-way sync of contract records",
            "icon": "shield",
            "connected": False,
        },
        {
            "name": "Workday",
            "description": "Sync counterparty data with vendor master",
            "icon": "briefcase",
            "connected": False,
        },
        {
            "name": "Zapier",
            "description": "Connect to 5,000+ apps via webhook",
            "icon": "zap",
            "connected": False,
        },
    ]

    # API keys
    api_keys: list[ApiKey] = [
        {
            "name": "Production",
            "prefix": "co_live_9a2f…",
            "created": "3 months ago",
            "last_used": "12 min ago",
        },
        {
            "name": "Staging",
            "prefix": "co_test_1b4c…",
            "created": "1 month ago",
            "last_used": "Yesterday",
        },
    ]

    saved_flash: str = ""

    @rx.var
    def sections(self) -> list[dict[str, str]]:
        return [
            {"key": "profile", "label": "Profile", "icon": "user"},
            {"key": "company", "label": "Company", "icon": "building-2"},
            {"key": "notifications", "label": "Notifications", "icon": "bell"},
            {"key": "integrations", "label": "Integrations", "icon": "plug"},
            {"key": "security", "label": "Security", "icon": "shield-check"},
            {"key": "api", "label": "API keys", "icon": "key-round"},
        ]

    @rx.event
    def set_section(self, key: str):
        self.active_section = key
        self.saved_flash = ""

    @rx.event
    def save_profile(self, form_data: dict):
        self.full_name = form_data.get("full_name", self.full_name)
        self.email = form_data.get("email", self.email)
        self.role = form_data.get("role", self.role)
        self.timezone = form_data.get("timezone", self.timezone)
        self.saved_flash = "profile"
        return rx.toast.success("Profile saved")

    @rx.event
    def save_company(self, form_data: dict):
        self.company_name = form_data.get("company_name", self.company_name)
        self.company_domain = form_data.get(
            "company_domain", self.company_domain
        )
        self.default_playbook = form_data.get(
            "default_playbook", self.default_playbook
        )
        self.default_governing_law = form_data.get(
            "default_governing_law", self.default_governing_law
        )
        self.fiscal_year_start = form_data.get(
            "fiscal_year_start", self.fiscal_year_start
        )
        self.saved_flash = "company"
        return rx.toast.success("Company preferences saved")

    @rx.event
    def toggle_notification(self, key: str):
        if key == "pending":
            self.notify_pending_approvals = not self.notify_pending_approvals
        elif key == "risk":
            self.notify_high_risk = not self.notify_high_risk
        elif key == "renewals":
            self.notify_renewals = not self.notify_renewals
        elif key == "digest":
            self.notify_weekly_digest = not self.notify_weekly_digest
        elif key == "slack":
            self.notify_slack_mentions = not self.notify_slack_mentions

    @rx.event
    def set_email_frequency(self, value: str):
        self.email_frequency = value

    @rx.event
    def save_notifications(self):
        self.saved_flash = "notifications"
        return rx.toast.success("Notification preferences saved")

    @rx.event
    def toggle_integration(self, name: str):
        for i, ig in enumerate(self.integrations):
            if ig["name"] == name:
                self.integrations[i]["connected"] = not ig["connected"]
                verb = "Disconnected" if ig["connected"] else "Connected"
                return rx.toast.success(f"{verb} {name}")

    @rx.event
    def toggle_2fa(self):
        self.require_2fa = not self.require_2fa

    @rx.event
    def toggle_ip_allowlist(self):
        self.ip_allowlist_enabled = not self.ip_allowlist_enabled

    @rx.event
    def set_session_timeout(self, value: str):
        self.session_timeout = value

    @rx.event
    def save_security(self):
        self.saved_flash = "security"
        return rx.toast.success("Security settings saved")

    @rx.event
    def create_api_key(self, form_data: dict):
        name = form_data.get("key_name", "").strip() or "New key"
        import secrets

        prefix = f"co_live_{secrets.token_hex(3)}…"
        self.api_keys.append(
            {
                "name": name,
                "prefix": prefix,
                "created": "just now",
                "last_used": "—",
            }
        )
        return rx.toast.success(f"API key '{name}' created")

    @rx.event
    def revoke_api_key(self, prefix: str):
        self.api_keys = [k for k in self.api_keys if k["prefix"] != prefix]
        return rx.toast.info("API key revoked")
