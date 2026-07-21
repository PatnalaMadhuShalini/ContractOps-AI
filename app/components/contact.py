import reflex as rx
from app.states.crm_state import CrmState


TEAM_SIZES: list[str] = ["1-10", "10-50", "50-200", "200-1000", "1000+"]


def _label(text: str) -> rx.Component:
    return rx.el.label(
        text,
        class_name="text-[12px] font-semibold text-gray-700 mb-1.5",
    )


def _input(
    name: str,
    placeholder: str,
    type_: str = "text",
    required: bool = True,
) -> rx.Component:
    return rx.el.input(
        name=name,
        type=type_,
        placeholder=placeholder,
        required=required,
        class_name="h-10 px-3 rounded-md border border-gray-200 bg-white text-[13.5px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
    )


def _select(name: str) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.el.option("Select team size", value=""),
            *[rx.el.option(s, value=s) for s in TEAM_SIZES],
            name=name,
            default_value="",
            class_name="h-10 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13.5px] text-gray-800 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full",
        ),
        rx.icon(
            "chevron-down",
            class_name="h-3.5 w-3.5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none",
        ),
        class_name="relative",
    )


def _textarea(name: str, placeholder: str, rows: int = 3) -> rx.Component:
    return rx.el.textarea(
        name=name,
        placeholder=placeholder,
        rows=rows,
        class_name="p-3 rounded-md border border-gray-200 bg-white text-[13.5px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full resize-none",
    )


def _field(label: str, control: rx.Component) -> rx.Component:
    return rx.el.div(_label(label), control, class_name="flex flex-col")


def _success_state(
    title: str, body: str, reset_event, reset_label: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("circle-check", class_name="h-5 w-5 text-emerald-600"),
            class_name="h-10 w-10 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center",
        ),
        rx.el.h4(
            title,
            class_name="mt-4 text-[16px] font-semibold text-gray-900",
        ),
        rx.el.p(
            body,
            class_name="mt-1.5 text-[13.5px] text-gray-600 leading-relaxed",
        ),
        rx.el.button(
            reset_label,
            on_click=reset_event,
            class_name="mt-5 inline-flex items-center h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
        ),
        class_name="flex flex-col items-start",
    )


def _contact_sales_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "message-square-text", class_name="h-4 w-4 text-blue-600"
                ),
                class_name="h-8 w-8 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.h3(
                    "Talk to sales",
                    class_name="text-[16px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Custom pricing, SOC 2 evidence, or procurement questions — we usually reply within a business day.",
                    class_name="mt-1 text-[13px] text-gray-600 leading-relaxed",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-start gap-3 mb-6",
        ),
        rx.cond(
            CrmState.contact_submitted,
            _success_state(
                "Message received",
                "Thanks for reaching out. Our sales team will be in touch within one business day. We've also queued a copy of your request in our CRM.",
                CrmState.reset_contact_form,
                "Send another message",
            ),
            rx.el.form(
                rx.el.div(
                    _field("Full name", _input("name", "Alex Keller")),
                    _field(
                        "Work email",
                        _input("email", "alex@company.com", "email"),
                    ),
                    _field("Company", _input("company", "Acme Legal")),
                    _field(
                        "Phone (optional)",
                        _input(
                            "phone", "+1 555 555 5555", "tel", required=False
                        ),
                    ),
                    _field("Team size", _select("team_size")),
                    _field(
                        "What can we help with?",
                        _textarea(
                            "message",
                            "Tell us about your contract workflow, team size, or procurement requirements.",
                            rows=4,
                        ),
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                ),
                rx.cond(
                    CrmState.contact_error != "",
                    rx.el.div(
                        rx.icon(
                            "circle-alert",
                            class_name="h-3.5 w-3.5 text-red-600 mt-0.5 shrink-0",
                        ),
                        rx.el.p(
                            CrmState.contact_error,
                            class_name="text-[12.5px] text-red-700 leading-snug",
                        ),
                        class_name="mt-4 flex items-start gap-1.5 p-2.5 rounded-md border border-red-100 bg-red-50/70",
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    "Contact sales",
                    rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                    type="submit",
                    class_name="mt-5 inline-flex items-center justify-center gap-1.5 h-10 px-4 rounded-md bg-blue-600 text-[13.5px] font-semibold text-white hover:bg-blue-700 transition-colors w-full sm:w-auto",
                ),
                on_submit=CrmState.submit_contact,
                reset_on_submit=True,
            ),
        ),
        class_name="p-6 rounded-xl border border-gray-200 bg-white",
    )


def _demo_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar-clock", class_name="h-4 w-4 text-blue-600"),
                class_name="h-8 w-8 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.h3(
                    "Book a live demo",
                    class_name="text-[16px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    "30 minutes with a product specialist — bring one of your contracts and we'll review it live against your playbook.",
                    class_name="mt-1 text-[13px] text-gray-600 leading-relaxed",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-start gap-3 mb-6",
        ),
        rx.cond(
            CrmState.demo_submitted,
            _success_state(
                "Demo requested",
                "We've received your demo request. A member of the team will reach out shortly with available time slots.",
                CrmState.reset_demo_form,
                "Book another demo",
            ),
            rx.el.form(
                rx.el.div(
                    _field("Full name", _input("name", "Alex Keller")),
                    _field(
                        "Work email",
                        _input("email", "alex@company.com", "email"),
                    ),
                    _field("Company", _input("company", "Acme Legal")),
                    _field(
                        "Phone (optional)",
                        _input(
                            "phone", "+1 555 555 5555", "tel", required=False
                        ),
                    ),
                    _field("Team size", _select("team_size")),
                    _field(
                        "Anything specific to see?",
                        _textarea(
                            "message",
                            "MSAs, DPAs, playbook automation, Salesforce sync — tell us what to focus on.",
                            rows=4,
                        ),
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                ),
                rx.cond(
                    CrmState.demo_error != "",
                    rx.el.div(
                        rx.icon(
                            "circle-alert",
                            class_name="h-3.5 w-3.5 text-red-600 mt-0.5 shrink-0",
                        ),
                        rx.el.p(
                            CrmState.demo_error,
                            class_name="text-[12.5px] text-red-700 leading-snug",
                        ),
                        class_name="mt-4 flex items-start gap-1.5 p-2.5 rounded-md border border-red-100 bg-red-50/70",
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    "Book my demo",
                    rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                    type="submit",
                    class_name="mt-5 inline-flex items-center justify-center gap-1.5 h-10 px-4 rounded-md bg-blue-600 text-[13.5px] font-semibold text-white hover:bg-blue-700 transition-colors w-full sm:w-auto",
                ),
                on_submit=CrmState.submit_demo,
                reset_on_submit=True,
            ),
        ),
        class_name="p-6 rounded-xl border border-gray-200 bg-white",
    )


def _trust_row() -> rx.Component:
    def item(icon: str, text: str) -> rx.Component:
        return rx.el.div(
            rx.icon(icon, class_name="h-3.5 w-3.5 text-emerald-600"),
            rx.el.span(
                text,
                class_name="text-[12.5px] font-medium text-gray-600",
            ),
            class_name="inline-flex items-center gap-1.5",
        )

    return rx.el.div(
        item("shield-check", "SOC 2 Type II"),
        item("lock", "Data never trains our models"),
        item("clock", "Reply within 1 business day"),
        item("globe", "US + EU regions"),
        class_name="mt-8 flex flex-wrap items-center justify-center gap-x-6 gap-y-2",
    )


def contact_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Contact",
                    class_name="text-[12px] font-semibold uppercase tracking-[0.14em] text-blue-600",
                ),
                rx.el.h2(
                    "Get in touch with our team.",
                    class_name="mt-2 text-3xl sm:text-4xl font-semibold tracking-tight text-gray-900",
                ),
                rx.el.p(
                    "Whether you want a live demo or a quick answer on pricing and security, we're here — real humans, no auto-responders.",
                    class_name="mt-3 text-[15px] text-gray-600 max-w-2xl mx-auto",
                ),
                class_name="text-center max-w-2xl mx-auto",
            ),
            rx.el.div(
                _demo_card(),
                _contact_sales_card(),
                class_name="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-4",
            ),
            _trust_row(),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20",
        ),
        class_name="bg-white border-b border-gray-200",
        id="contact-sales",
    )
