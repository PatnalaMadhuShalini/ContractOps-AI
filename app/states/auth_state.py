import reflex as rx
from typing import TypedDict


class AuthUser(TypedDict):
    id: str
    email: str
    password: str
    name: str
    initials: str
    role: str  # "platform_admin" | "owner" | "admin" | "member"
    company_id: str
    status: str  # "active" | "invited"
    created: str
    last_active: str


class Company(TypedDict):
    id: str
    name: str
    domain: str
    plan: str  # "Starter" | "Growth" | "Enterprise"
    contracts_reviewed: int
    created: str
    status: str  # "active" | "trialing" | "suspended"


class Invite(TypedDict):
    id: str
    email: str
    company_id: str
    role: str
    invited_by: str
    created: str


PLAN_LIMITS: dict[str, dict[str, int]] = {
    "Starter": {"contracts": 50, "seats": 5},
    "Growth": {"contracts": 500, "seats": 25},
    "Enterprise": {"contracts": 9999, "seats": 9999},
}

PLAN_ORDER: list[str] = ["Starter", "Growth", "Enterprise"]


def _seed_companies() -> list[Company]:
    return [
        {
            "id": "co-acme",
            "name": "Acme Legal",
            "domain": "acmelegal.com",
            "plan": "Growth",
            "contracts_reviewed": 142,
            "created": "Jan 12, 2025",
            "status": "active",
        },
        {
            "id": "co-northwind",
            "name": "Northwind Legal",
            "domain": "northwind.com",
            "plan": "Starter",
            "contracts_reviewed": 38,
            "created": "Feb 04, 2025",
            "status": "trialing",
        },
        {
            "id": "co-globex",
            "name": "Globex Systems",
            "domain": "globex.io",
            "plan": "Enterprise",
            "contracts_reviewed": 892,
            "created": "Nov 22, 2024",
            "status": "active",
        },
        {
            "id": "co-initech",
            "name": "Initech LLC",
            "domain": "initech.com",
            "plan": "Starter",
            "contracts_reviewed": 47,
            "created": "Mar 01, 2025",
            "status": "active",
        },
    ]


def _seed_users() -> list[AuthUser]:
    return [
        {
            "id": "u-platform",
            "email": "admin@contractops.ai",
            "password": "admin123",
            "name": "Platform Admin",
            "initials": "PA",
            "role": "platform_admin",
            "company_id": "",
            "status": "active",
            "created": "Jan 01, 2025",
            "last_active": "just now",
        },
        {
            "id": "u-alex",
            "email": "alex@acmelegal.com",
            "password": "demo123",
            "name": "Alex Keller",
            "initials": "AK",
            "role": "owner",
            "company_id": "co-acme",
            "status": "active",
            "created": "Jan 12, 2025",
            "last_active": "2 min ago",
        },
        {
            "id": "u-sarah",
            "email": "sarah@acmelegal.com",
            "password": "demo123",
            "name": "Sarah Reeves",
            "initials": "SR",
            "role": "admin",
            "company_id": "co-acme",
            "status": "active",
            "created": "Jan 14, 2025",
            "last_active": "18 min ago",
        },
        {
            "id": "u-priya",
            "email": "priya@acmelegal.com",
            "password": "demo123",
            "name": "Priya Shah",
            "initials": "PS",
            "role": "member",
            "company_id": "co-acme",
            "status": "active",
            "created": "Jan 20, 2025",
            "last_active": "1 hour ago",
        },
        {
            "id": "u-marcus",
            "email": "marcus@acmelegal.com",
            "password": "demo123",
            "name": "Marcus Lin",
            "initials": "ML",
            "role": "member",
            "company_id": "co-acme",
            "status": "active",
            "created": "Feb 02, 2025",
            "last_active": "Yesterday",
        },
        {
            "id": "u-nw-gc",
            "email": "gc@northwind.com",
            "password": "demo123",
            "name": "Jamie Reyes",
            "initials": "JR",
            "role": "owner",
            "company_id": "co-northwind",
            "status": "active",
            "created": "Feb 04, 2025",
            "last_active": "3 hours ago",
        },
        {
            "id": "u-gx-gc",
            "email": "legal@globex.io",
            "password": "demo123",
            "name": "Elena Vasquez",
            "initials": "EV",
            "role": "owner",
            "company_id": "co-globex",
            "status": "active",
            "created": "Nov 22, 2024",
            "last_active": "12 min ago",
        },
        {
            "id": "u-in-gc",
            "email": "counsel@initech.com",
            "password": "demo123",
            "name": "Peter Gibbons",
            "initials": "PG",
            "role": "owner",
            "company_id": "co-initech",
            "status": "active",
            "created": "Mar 01, 2025",
            "last_active": "2 days ago",
        },
    ]


def _seed_invites() -> list[Invite]:
    return [
        {
            "id": "inv-001",
            "email": "jordan@acmelegal.com",
            "company_id": "co-acme",
            "role": "member",
            "invited_by": "Alex Keller",
            "created": "2 days ago",
        }
    ]


def _initials(name: str) -> str:
    parts = [p for p in name.strip().split() if p]
    if not parts:
        return "U"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


class AuthState(rx.State):
    users: list[AuthUser] = _seed_users()
    companies: list[Company] = _seed_companies()
    invites: list[Invite] = _seed_invites()
    current_user_id: str = ""
    login_error: str = ""
    signup_error: str = ""
    invite_error: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_user_id != ""

    @rx.var
    def current_user(self) -> AuthUser:
        for u in self.users:
            if u["id"] == self.current_user_id:
                return u
        return {
            "id": "",
            "email": "",
            "password": "",
            "name": "Guest",
            "initials": "G",
            "role": "member",
            "company_id": "",
            "status": "active",
            "created": "",
            "last_active": "",
        }

    @rx.var
    def is_platform_admin(self) -> bool:
        return self.current_user["role"] == "platform_admin"

    @rx.var
    def can_manage_company(self) -> bool:
        return self.current_user["role"] in ("owner", "admin")

    @rx.var
    def current_company(self) -> Company:
        cid = self.current_user["company_id"]
        for c in self.companies:
            if c["id"] == cid:
                return c
        return {
            "id": "",
            "name": "—",
            "domain": "",
            "plan": "Starter",
            "contracts_reviewed": 0,
            "created": "",
            "status": "active",
        }

    @rx.var
    def contracts_limit(self) -> int:
        return PLAN_LIMITS.get(
            self.current_company["plan"], PLAN_LIMITS["Starter"]
        )["contracts"]

    @rx.var
    def seats_limit(self) -> int:
        return PLAN_LIMITS.get(
            self.current_company["plan"], PLAN_LIMITS["Starter"]
        )["seats"]

    @rx.var
    def usage_percent(self) -> int:
        limit = self.contracts_limit
        if limit <= 0:
            return 0
        pct = round(self.current_company["contracts_reviewed"] * 100 / limit)
        if pct > 100:
            return 100
        return pct

    @rx.var
    def contracts_remaining(self) -> int:
        remaining = (
            self.contracts_limit - self.current_company["contracts_reviewed"]
        )
        return remaining if remaining > 0 else 0

    @rx.var
    def company_users(self) -> list[AuthUser]:
        cid = self.current_user["company_id"]
        return [u for u in self.users if u["company_id"] == cid]

    @rx.var
    def company_invites(self) -> list[Invite]:
        cid = self.current_user["company_id"]
        return [i for i in self.invites if i["company_id"] == cid]

    @rx.var
    def seats_used(self) -> int:
        return len(self.company_users) + len(self.company_invites)

    @rx.var
    def seats_percent(self) -> int:
        limit = self.seats_limit
        if limit <= 0:
            return 0
        pct = round(self.seats_used * 100 / limit)
        if pct > 100:
            return 100
        return pct

    @rx.var
    def plan_options(self) -> list[str]:
        return PLAN_ORDER

    # Admin views
    @rx.var
    def admin_companies(self) -> list[dict[str, str | int]]:
        rows: list[dict[str, str | int]] = []
        for c in self.companies:
            user_count = sum(
                1 for u in self.users if u["company_id"] == c["id"]
            )
            limits = PLAN_LIMITS.get(c["plan"], PLAN_LIMITS["Starter"])
            rows.append(
                {
                    "id": c["id"],
                    "name": c["name"],
                    "domain": c["domain"],
                    "plan": c["plan"],
                    "status": c["status"],
                    "created": c["created"],
                    "contracts_reviewed": c["contracts_reviewed"],
                    "contracts_limit": limits["contracts"],
                    "seats_limit": limits["seats"],
                    "users": user_count,
                }
            )
        return rows

    @rx.var
    def admin_users(self) -> list[dict[str, str]]:
        by_co: dict[str, str] = {c["id"]: c["name"] for c in self.companies}
        rows: list[dict[str, str]] = []
        for u in self.users:
            rows.append(
                {
                    "id": u["id"],
                    "name": u["name"],
                    "email": u["email"],
                    "initials": u["initials"],
                    "role": u["role"],
                    "status": u["status"],
                    "company": by_co.get(u["company_id"], "—"),
                    "last_active": u["last_active"],
                }
            )
        return rows

    @rx.var
    def admin_stats(self) -> dict[str, int]:
        total_contracts = sum(c["contracts_reviewed"] for c in self.companies)
        return {
            "companies": len(self.companies),
            "users": len(self.users),
            "contracts": total_contracts,
            "invites": len(self.invites),
        }

    # ---- Events ----
    @rx.event
    def login(self, form_data: dict):
        email = (form_data.get("email") or "").strip().lower()
        password = form_data.get("password") or ""
        self.login_error = ""
        for u in self.users:
            if u["email"].lower() == email and u["password"] == password:
                if u["status"] != "active":
                    self.login_error = "Your account is not active yet."
                    return
                self.current_user_id = u["id"]
                if u["role"] == "platform_admin":
                    return rx.redirect("/admin")
                return rx.redirect("/workspace")
        self.login_error = (
            "Invalid email or password. Try alex@acmelegal.com / demo123."
        )

    @rx.event
    def signup(self, form_data: dict):
        name = (form_data.get("name") or "").strip()
        email = (form_data.get("email") or "").strip().lower()
        password = form_data.get("password") or ""
        company_name = (form_data.get("company") or "").strip()
        self.signup_error = ""
        if not name or not email or not password or not company_name:
            self.signup_error = "All fields are required."
            return
        if len(password) < 6:
            self.signup_error = "Password must be at least 6 characters."
            return
        if any(u["email"].lower() == email for u in self.users):
            self.signup_error = "An account with that email already exists."
            return
        # Check for invite acceptance
        pending = next(
            (i for i in self.invites if i["email"].lower() == email), None
        )
        if pending is not None:
            company_id = pending["company_id"]
            role = pending["role"]
            self.invites = [i for i in self.invites if i["id"] != pending["id"]]
        else:
            domain = email.split("@")[-1] if "@" in email else "example.com"
            company_id = f"co-{email.split('@')[0]}-{len(self.companies) + 1}"
            self.companies.append(
                {
                    "id": company_id,
                    "name": company_name,
                    "domain": domain,
                    "plan": "Starter",
                    "contracts_reviewed": 0,
                    "created": "just now",
                    "status": "trialing",
                }
            )
            role = "owner"
        user_id = f"u-{email.split('@')[0]}-{len(self.users) + 1}"
        self.users.append(
            {
                "id": user_id,
                "email": email,
                "password": password,
                "name": name,
                "initials": _initials(name),
                "role": role,
                "company_id": company_id,
                "status": "active",
                "created": "just now",
                "last_active": "just now",
            }
        )
        self.current_user_id = user_id
        return rx.redirect("/workspace")

    @rx.event
    def logout(self):
        self.current_user_id = ""
        self.login_error = ""
        return rx.redirect("/login")

    @rx.event
    def invite_user(self, form_data: dict):
        email = (form_data.get("email") or "").strip().lower()
        role = form_data.get("role") or "member"
        self.invite_error = ""
        if not email or "@" not in email:
            self.invite_error = "Enter a valid email address."
            return
        cid = self.current_user["company_id"]
        if any(
            u["email"].lower() == email and u["company_id"] == cid
            for u in self.users
        ):
            self.invite_error = "That user is already on your workspace."
            return
        if any(
            i["email"].lower() == email and i["company_id"] == cid
            for i in self.invites
        ):
            self.invite_error = "That email already has a pending invite."
            return
        if self.seats_used >= self.seats_limit:
            self.invite_error = (
                "Seat limit reached — upgrade your plan to invite more."
            )
            return
        self.invites.append(
            {
                "id": f"inv-{len(self.invites) + 1:03d}",
                "email": email,
                "company_id": cid,
                "role": role,
                "invited_by": self.current_user["name"],
                "created": "just now",
            }
        )
        return rx.toast.success(f"Invite sent to {email}")

    @rx.event
    def revoke_invite(self, invite_id: str):
        self.invites = [i for i in self.invites if i["id"] != invite_id]
        return rx.toast.info("Invite revoked")

    @rx.event
    def resend_invite(self, invite_id: str):
        return rx.toast.success("Invite resent")

    @rx.event
    def remove_user(self, user_id: str):
        target = next((u for u in self.users if u["id"] == user_id), None)
        if target is None:
            return
        if target["id"] == self.current_user_id:
            return rx.toast.error("You cannot remove yourself.")
        if target["role"] == "owner":
            return rx.toast.error("Owners cannot be removed.")
        self.users = [u for u in self.users if u["id"] != user_id]
        return rx.toast.info(f"Removed {target['name']}")

    @rx.event
    def change_user_role(self, user_id: str, role: str):
        for i, u in enumerate(self.users):
            if u["id"] == user_id:
                if u["role"] == "owner":
                    return rx.toast.error("Owner role cannot be changed.")
                self.users[i]["role"] = role
                return rx.toast.success(f"Updated role to {role}")

    @rx.event
    def change_plan(self, plan: str):
        if plan not in PLAN_LIMITS:
            return
        cid = self.current_user["company_id"]
        for i, c in enumerate(self.companies):
            if c["id"] == cid:
                self.companies[i]["plan"] = plan
                return rx.toast.success(f"Plan changed to {plan}")

    @rx.event
    def admin_change_plan(self, company_id: str, plan: str):
        if plan not in PLAN_LIMITS:
            return
        for i, c in enumerate(self.companies):
            if c["id"] == company_id:
                self.companies[i]["plan"] = plan
                return rx.toast.success(f"{c['name']} → {plan}")

    @rx.event
    def admin_toggle_status(self, company_id: str):
        for i, c in enumerate(self.companies):
            if c["id"] == company_id:
                self.companies[i]["status"] = (
                    "suspended" if c["status"] != "suspended" else "active"
                )
                return rx.toast.info(
                    f"{c['name']} is now {self.companies[i]['status']}"
                )

    @rx.event
    def increment_usage(self):
        """Simulate a contract review — bumps the counter, enforces plan limit."""
        cid = self.current_user["company_id"]
        for i, c in enumerate(self.companies):
            if c["id"] == cid:
                limit = PLAN_LIMITS.get(c["plan"], PLAN_LIMITS["Starter"])[
                    "contracts"
                ]
                if c["contracts_reviewed"] >= limit:
                    return rx.toast.error(
                        "Plan limit reached — upgrade to review more contracts."
                    )
                self.companies[i]["contracts_reviewed"] = (
                    c["contracts_reviewed"] + 1
                )
                return rx.toast.success("Contract review counted")

    @rx.event
    def require_auth(self):
        """on_load guard — redirect to /login if not authenticated."""
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    def require_platform_admin(self):
        if not self.is_authenticated:
            return rx.redirect("/login")
        if not self.is_platform_admin:
            return rx.redirect("/workspace")
