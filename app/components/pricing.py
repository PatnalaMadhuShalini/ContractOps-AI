import reflex as rx
from app.states.landing_state import LandingState


def _check_row(text: str) -> rx.Component:
    return rx.el.li(
        rx.icon(
            "check", class_name="h-3.5 w-3.5 text-blue-600 mt-0.5 shrink-0"
        ),
        rx.el.span(text, class_name="text-[13.5px] text-gray-700 leading-snug"),
        class_name="flex items-start gap-2",
    )


def _tier(
    name: str,
    tagline: str,
    monthly: str,
    annual: str,
    unit: str,
    cta: str,
    features_list: list[str],
    highlight: bool = False,
) -> rx.Component:
    price = rx.cond(LandingState.billing_annual, annual, monthly)
    header_cls = "text-[13px] font-semibold text-blue-600"
    if highlight:
        card_cls = "relative p-6 rounded-xl border-2 border-blue-600 bg-white"
        btn_cls = "mt-6 inline-flex items-center justify-center w-full h-10 rounded-md bg-blue-600 text-sm font-semibold text-white hover:bg-blue-700 transition-colors"
    else:
        card_cls = "relative p-6 rounded-xl border border-gray-200 bg-white"
        btn_cls = "mt-6 inline-flex items-center justify-center w-full h-10 rounded-md border border-gray-200 bg-white text-sm font-semibold text-gray-800 hover:bg-gray-50 transition-colors"
    return rx.el.div(
        rx.cond(
            highlight,
            rx.el.span(
                "Most popular",
                class_name="absolute -top-2.5 left-6 inline-flex items-center h-5 px-2 rounded-full bg-blue-600 text-[10.5px] font-semibold uppercase tracking-wider text-white",
            ),
            rx.fragment(),
        ),
        rx.el.p(name, class_name=header_cls),
        rx.el.p(tagline, class_name="mt-1 text-[13.5px] text-gray-600"),
        rx.el.div(
            rx.el.span(
                "$", class_name="text-lg font-semibold text-gray-900 align-top"
            ),
            rx.el.span(
                price,
                class_name="text-5xl font-semibold tracking-tight text-gray-900 leading-none",
            ),
            rx.el.span(unit, class_name="ml-1.5 text-[13px] text-gray-500"),
            class_name="mt-5 flex items-baseline",
        ),
        rx.el.a(
            cta,
            href="#contact-sales",
            class_name=btn_cls,
        ),
        rx.el.div(class_name="mt-6 h-px bg-gray-200"),
        rx.el.ul(
            *[_check_row(f) for f in features_list],
            class_name="mt-6 flex flex-col gap-2.5",
        ),
        class_name=card_cls,
    )


def _toggle() -> rx.Component:
    active = "h-8 px-3 rounded-md bg-white text-[12.5px] font-semibold text-gray-900 shadow-sm border border-gray-200"
    inactive = "h-8 px-3 rounded-md text-[12.5px] font-semibold text-gray-500 hover:text-gray-800"
    return rx.el.div(
        rx.el.button(
            "Monthly",
            on_click=lambda: LandingState.set_annual(False),
            class_name=rx.cond(LandingState.billing_annual, inactive, active),
        ),
        rx.el.button(
            "Annual",
            rx.el.span(
                "−20%",
                class_name="ml-1.5 inline-flex items-center h-4 px-1 rounded bg-blue-50 text-blue-700 text-[10px] font-semibold",
            ),
            on_click=lambda: LandingState.set_annual(True),
            class_name=rx.cond(LandingState.billing_annual, active, inactive),
        ),
        class_name="inline-flex items-center gap-1 p-1 rounded-lg bg-gray-100 border border-gray-200",
    )


def pricing() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Pricing",
                    class_name="text-[12px] font-semibold uppercase tracking-[0.14em] text-blue-600",
                ),
                rx.el.h2(
                    "Simple, usage-based pricing.",
                    class_name="mt-2 text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "Start free. Scale seat by seat. No per-contract fees, ever.",
                    class_name="mt-3 text-[15px] text-gray-600",
                ),
                _toggle(),
                class_name="flex flex-col items-center text-center gap-5",
            ),
            rx.el.div(
                _tier(
                    "Starter",
                    "For small legal teams getting off email.",
                    "49",
                    "39",
                    "/ user / mo",
                    "Start free trial",
                    [
                        "Up to 5 users",
                        "AI review on MSAs, NDAs, SOWs",
                        "50 contracts / month",
                        "Standard playbook templates",
                        "Email + Slack intake",
                    ],
                ),
                _tier(
                    "Growth",
                    "For scale-ups closing dozens of deals per week.",
                    "129",
                    "99",
                    "/ user / mo",
                    "Start free trial",
                    [
                        "Unlimited contracts",
                        "Custom playbooks & fallback library",
                        "Deviation-based approvals",
                        "Salesforce & Drive integrations",
                        "Obligation & renewal tracking",
                        "SSO / SAML",
                    ],
                    highlight=True,
                ),
                _tier(
                    "Enterprise",
                    "For legal orgs with security and scale needs.",
                    "—",
                    "—",
                    "custom",
                    "Talk to sales",
                    [
                        "Private VPC + dedicated region",
                        "Custom SLAs & 24/7 support",
                        "Advanced audit & DLP controls",
                        "Bring-your-own model & fine-tunes",
                        "Change management & training",
                        "SOC 2, ISO 27001, HIPAA-ready",
                    ],
                ),
                class_name="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
        ),
        class_name="border-b border-gray-200",
        id="pricing",
    )
