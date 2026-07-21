import reflex as rx
from app.components.page_shell import page_shell, page_header
from app.states.settings_state import SettingsState


def _sidebar_nav() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.p(
                "Settings",
                class_name="px-2.5 pt-3 pb-1.5 text-[11px] font-semibold uppercase tracking-wider text-gray-400",
            ),
            rx.foreach(
                SettingsState.sections,
                lambda s: rx.el.button(
                    rx.icon(s["icon"], class_name="h-4 w-4"),
                    rx.el.span(s["label"]),
                    on_click=lambda: SettingsState.set_section(s["key"]),
                    class_name=rx.cond(
                        SettingsState.active_section == s["key"],
                        "flex items-center gap-2.5 h-8 px-2.5 rounded-md text-[13px] font-medium bg-blue-50 text-blue-700 w-full",
                        "flex items-center gap-2.5 h-8 px-2.5 rounded-md text-[13px] font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 w-full",
                    ),
                ),
            ),
            class_name="flex flex-col gap-0.5 p-2",
        ),
        class_name="w-full lg:w-56 shrink-0 rounded-xl border border-gray-200 bg-white sticky top-20 self-start",
    )


def _label(text: str) -> rx.Component:
    return rx.el.label(
        text,
        class_name="text-[12px] font-semibold text-gray-700 mb-1.5",
    )


def _input(
    name: str, value, placeholder: str = "", type_: str = "text"
) -> rx.Component:
    return rx.el.input(
        name=name,
        default_value=value,
        key=value,
        placeholder=placeholder,
        type=type_,
        class_name="h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
    )


def _select(name: str, value, options: list[str]) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            *[rx.el.option(o, value=o) for o in options],
            name=name,
            default_value=value,
            key=value,
            class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
        ),
        rx.icon(
            "chevron-down",
            class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
        ),
        class_name="relative",
    )


def _field(label: str, control: rx.Component, hint: str = "") -> rx.Component:
    return rx.el.div(
        _label(label),
        control,
        rx.cond(
            hint != "",
            rx.el.p(hint, class_name="mt-1 text-[11.5px] text-gray-500"),
            rx.fragment(),
        ),
        class_name="flex flex-col",
    )


def _section_card(
    title: str, subtitle: str, body: rx.Component
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                title,
                class_name="text-[15px] font-semibold text-gray-900",
            ),
            rx.el.p(
                subtitle,
                class_name="mt-0.5 text-[12.5px] text-gray-600",
            ),
            class_name="mb-5 pb-4 border-b border-gray-100",
        ),
        body,
        class_name="p-6 rounded-xl border border-gray-200 bg-white",
    )


def _save_button(label: str = "Save changes") -> rx.Component:
    return rx.el.button(
        label,
        type="submit",
        class_name="inline-flex items-center h-9 px-4 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
    )


def _toggle(active, on_click) -> rx.Component:
    return rx.el.button(
        rx.el.span(
            class_name=rx.cond(
                active,
                "inline-block h-4 w-4 rounded-full bg-white shadow-sm translate-x-4 transition-transform",
                "inline-block h-4 w-4 rounded-full bg-white shadow-sm translate-x-0.5 transition-transform",
            ),
        ),
        on_click=on_click,
        type="button",
        class_name=rx.cond(
            active,
            "h-5 w-9 rounded-full bg-blue-600 flex items-center transition-colors",
            "h-5 w-9 rounded-full bg-gray-200 flex items-center transition-colors",
        ),
    )


def _toggle_row(title: str, description: str, active, on_click) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                title, class_name="text-[13px] font-semibold text-gray-900"
            ),
            rx.el.p(
                description,
                class_name="mt-0.5 text-[12px] text-gray-600 leading-relaxed",
            ),
            class_name="flex flex-col min-w-0 flex-1 pr-4",
        ),
        _toggle(active, on_click),
        class_name="flex items-start justify-between py-3.5 border-b border-gray-100 last:border-b-0",
    )


def _profile() -> rx.Component:
    return _section_card(
        "Your profile",
        "How you appear to your team across contracts and approvals.",
        rx.el.form(
            rx.el.div(
                _field(
                    "Full name", _input("full_name", SettingsState.full_name)
                ),
                _field(
                    "Email",
                    _input("email", SettingsState.email, type_="email"),
                    "Used for contract intake and notifications.",
                ),
                _field("Role", _input("role", SettingsState.role)),
                _field(
                    "Timezone",
                    _select(
                        "timezone",
                        SettingsState.timezone,
                        [
                            "America/New_York",
                            "America/Los_Angeles",
                            "America/Chicago",
                            "Europe/London",
                            "Europe/Berlin",
                            "Asia/Singapore",
                        ],
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
            ),
            rx.el.div(
                _save_button(),
                class_name="mt-6 flex justify-end",
            ),
            on_submit=SettingsState.save_profile,
        ),
    )


def _company() -> rx.Component:
    return _section_card(
        "Company preferences",
        "Defaults that apply to every new contract, playbook, and workflow.",
        rx.el.form(
            rx.el.div(
                _field(
                    "Company name",
                    _input("company_name", SettingsState.company_name),
                ),
                _field(
                    "Primary domain",
                    _input("company_domain", SettingsState.company_domain),
                    "Used to detect internal vs. external counterparties.",
                ),
                _field(
                    "Default playbook",
                    _select(
                        "default_playbook",
                        SettingsState.default_playbook,
                        [
                            "Enterprise SaaS",
                            "Standard NDA",
                            "GDPR Processor",
                            "Professional Services",
                            "Vendor Paper",
                        ],
                    ),
                ),
                _field(
                    "Default governing law",
                    _select(
                        "default_governing_law",
                        SettingsState.default_governing_law,
                        [
                            "Delaware",
                            "New York",
                            "California",
                            "England & Wales",
                        ],
                    ),
                ),
                _field(
                    "Fiscal year starts",
                    _select(
                        "fiscal_year_start",
                        SettingsState.fiscal_year_start,
                        [
                            "January",
                            "April",
                            "July",
                            "October",
                        ],
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
            ),
            rx.el.div(
                _save_button(),
                class_name="mt-6 flex justify-end",
            ),
            on_submit=SettingsState.save_company,
        ),
    )


def _notifications() -> rx.Component:
    return _section_card(
        "Notifications",
        "Choose what pings you, where, and how often.",
        rx.el.div(
            _toggle_row(
                "Pending approvals",
                "Get notified whenever a contract is routed to you for review.",
                SettingsState.notify_pending_approvals,
                lambda: SettingsState.toggle_notification("pending"),
            ),
            _toggle_row(
                "High-risk deviations",
                "Alert me the moment AI flags a high-risk clause deviation.",
                SettingsState.notify_high_risk,
                lambda: SettingsState.toggle_notification("risk"),
            ),
            _toggle_row(
                "Renewal reminders",
                "Reminder 60 days before any contract's renewal notice window.",
                SettingsState.notify_renewals,
                lambda: SettingsState.toggle_notification("renewals"),
            ),
            _toggle_row(
                "Weekly digest",
                "A Monday-morning summary of the week's contract activity.",
                SettingsState.notify_weekly_digest,
                lambda: SettingsState.toggle_notification("digest"),
            ),
            _toggle_row(
                "Slack mentions",
                "Ping me in Slack when I'm @-mentioned on a contract.",
                SettingsState.notify_slack_mentions,
                lambda: SettingsState.toggle_notification("slack"),
            ),
            rx.el.div(
                rx.el.p(
                    "Email frequency",
                    class_name="text-[13px] font-semibold text-gray-900 mb-2",
                ),
                rx.el.div(
                    _select(
                        "email_frequency",
                        SettingsState.email_frequency,
                        ["Immediate", "Hourly", "Daily digest", "Off"],
                    ),
                    class_name="max-w-xs",
                ),
                class_name="pt-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Save preferences",
                    on_click=SettingsState.save_notifications,
                    class_name="inline-flex items-center h-9 px-4 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                class_name="mt-6 flex justify-end",
            ),
        ),
    )


def _integrations() -> rx.Component:
    return _section_card(
        "Integrations",
        "Plug ContractOps AI into the tools your team already uses.",
        rx.el.div(
            rx.foreach(
                SettingsState.integrations,
                lambda ig: rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                ig["icon"],
                                class_name="h-4 w-4 text-blue-600",
                            ),
                            class_name="h-9 w-9 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                ig["name"],
                                class_name="text-[13.5px] font-semibold text-gray-900 leading-tight",
                            ),
                            rx.el.p(
                                ig["description"],
                                class_name="text-[12px] text-gray-600 leading-snug mt-0.5",
                            ),
                            class_name="flex flex-col min-w-0",
                        ),
                        class_name="flex items-start gap-3 min-w-0 flex-1",
                    ),
                    rx.el.div(
                        rx.cond(
                            ig["connected"],
                            rx.el.span(
                                rx.el.span(
                                    class_name="h-1.5 w-1.5 rounded-full bg-emerald-500"
                                ),
                                "Connected",
                                class_name="inline-flex items-center gap-1.5 h-6 px-2 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-700",
                            ),
                            rx.fragment(),
                        ),
                        rx.el.button(
                            rx.cond(ig["connected"], "Disconnect", "Connect"),
                            on_click=lambda: SettingsState.toggle_integration(
                                ig["name"]
                            ),
                            class_name=rx.cond(
                                ig["connected"],
                                "inline-flex items-center h-8 px-3 rounded-md border border-gray-200 bg-white text-[12.5px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                                "inline-flex items-center h-8 px-3 rounded-md bg-blue-600 text-[12.5px] font-semibold text-white hover:bg-blue-700 transition-colors",
                            ),
                        ),
                        class_name="flex items-center gap-2 shrink-0",
                    ),
                    class_name="flex items-center justify-between gap-3 p-4 rounded-xl border border-gray-200 bg-white",
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-3",
        ),
    )


def _security() -> rx.Component:
    return _section_card(
        "Security",
        "Access controls, session policy, and network safeguards.",
        rx.el.div(
            _toggle_row(
                "Require 2-factor authentication",
                "All members must verify with an authenticator app or hardware key.",
                SettingsState.require_2fa,
                SettingsState.toggle_2fa,
            ),
            _toggle_row(
                "IP allowlist",
                "Restrict access to a set of approved corporate IP ranges.",
                SettingsState.ip_allowlist_enabled,
                SettingsState.toggle_ip_allowlist,
            ),
            rx.el.div(
                rx.el.p(
                    "Session timeout",
                    class_name="text-[13px] font-semibold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Automatically sign out inactive sessions after this duration.",
                    class_name="text-[12px] text-gray-600 mb-2",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("1 hour", value="1 hour"),
                        rx.el.option("4 hours", value="4 hours"),
                        rx.el.option("8 hours", value="8 hours"),
                        rx.el.option("24 hours", value="24 hours"),
                        rx.el.option("7 days", value="7 days"),
                        value=SettingsState.session_timeout,
                        on_change=SettingsState.set_session_timeout,
                        class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative max-w-xs",
                ),
                class_name="pt-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Save security settings",
                    on_click=SettingsState.save_security,
                    class_name="inline-flex items-center h-9 px-4 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                class_name="mt-6 flex justify-end",
            ),
        ),
    )


def _api_keys() -> rx.Component:
    return _section_card(
        "API keys",
        "Programmatic access for scripts, webhooks, and internal tools.",
        rx.el.div(
            rx.el.form(
                rx.el.div(
                    rx.el.input(
                        name="key_name",
                        placeholder="Key name (e.g. Reporting service)",
                        class_name="flex-1 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="h-3.5 w-3.5"),
                        "Create key",
                        type="submit",
                        class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
                    ),
                    class_name="flex items-center gap-2",
                ),
                on_submit=SettingsState.create_api_key,
                reset_on_submit=True,
            ),
            rx.el.div(
                rx.foreach(
                    SettingsState.api_keys,
                    lambda k: rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "key-round",
                                class_name="h-4 w-4 text-gray-500 shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    k["name"],
                                    class_name="text-[13px] font-semibold text-gray-900",
                                ),
                                rx.el.p(
                                    k["prefix"]
                                    + " · created "
                                    + k["created"]
                                    + " · last used "
                                    + k["last_used"],
                                    class_name="text-[11.5px] text-gray-500 font-mono",
                                ),
                                class_name="flex flex-col min-w-0",
                            ),
                            class_name="flex items-center gap-2.5 min-w-0 flex-1",
                        ),
                        rx.el.button(
                            "Revoke",
                            on_click=lambda: SettingsState.revoke_api_key(
                                k["prefix"]
                            ),
                            class_name="inline-flex items-center h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors shrink-0",
                        ),
                        class_name="flex items-center justify-between gap-2 p-3 rounded-md border border-gray-200 bg-white",
                    ),
                ),
                class_name="mt-4 flex flex-col gap-2",
            ),
            rx.el.div(
                rx.icon("info", class_name="h-3.5 w-3.5 text-gray-400 mt-0.5"),
                rx.el.p(
                    "API keys grant access to your ContractOps workspace. Rotate them regularly and never share them in client-side code.",
                    class_name="text-[12px] text-gray-600 leading-relaxed",
                ),
                class_name="mt-4 flex items-start gap-1.5",
            ),
        ),
    )


def settings_page() -> rx.Component:
    return page_shell(
        "settings",
        rx.el.div(
            page_header(
                "Settings",
                "Manage your profile, company defaults, notifications, integrations, and security.",
            ),
            rx.el.div(
                rx.el.div(_sidebar_nav(), class_name="lg:col-span-3"),
                rx.el.div(
                    rx.match(
                        SettingsState.active_section,
                        ("profile", _profile()),
                        ("company", _company()),
                        ("notifications", _notifications()),
                        ("integrations", _integrations()),
                        ("security", _security()),
                        ("api", _api_keys()),
                        _profile(),
                    ),
                    class_name="lg:col-span-9",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-12 gap-5",
            ),
        ),
    )
