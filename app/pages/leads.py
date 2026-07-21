import reflex as rx
from app.components.page_shell import page_shell, page_header, stat_card
from app.states.crm_state import CrmState, Lead, EmailDraft, LEAD_STAGES
from app.states.auth_state import AuthState


# ---------- Small helpers ----------
def _stage_pill(stage: str) -> rx.Component:
    return rx.match(
        stage,
        (
            "New",
            rx.el.span(
                "New",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
            ),
        ),
        (
            "Contacted",
            rx.el.span(
                "Contacted",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-violet-50 text-violet-700",
            ),
        ),
        (
            "Qualified",
            rx.el.span(
                "Qualified",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-indigo-50 text-indigo-700",
            ),
        ),
        (
            "Demo scheduled",
            rx.el.span(
                "Demo",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-cyan-50 text-cyan-700",
            ),
        ),
        (
            "Proposal",
            rx.el.span(
                "Proposal",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
            ),
        ),
        (
            "Won",
            rx.el.span(
                rx.icon("check", class_name="h-3 w-3"),
                "Won",
                class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
            ),
        ),
        rx.el.span(
            rx.icon("x", class_name="h-3 w-3"),
            "Lost",
            class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
        ),
    )


def _priority_pill(p: str) -> rx.Component:
    return rx.match(
        p,
        (
            "High",
            rx.el.span(
                "High",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
            ),
        ),
        (
            "Medium",
            rx.el.span(
                "Medium",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
            ),
        ),
        rx.el.span(
            "Low",
            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
        ),
    )


def _interest_pill(i: str) -> rx.Component:
    return rx.match(
        i,
        (
            "demo",
            rx.el.span(
                "Demo",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
            ),
        ),
        (
            "trial",
            rx.el.span(
                "Trial",
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
            ),
        ),
        rx.el.span(
            "Sales",
            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-violet-50 text-violet-700",
        ),
    )


def _tab_button(key: str, label: str, icon: str, badge) -> rx.Component:
    active = CrmState.active_tab == key
    return rx.el.button(
        rx.icon(icon, class_name="h-3.5 w-3.5"),
        label,
        rx.el.span(
            badge,
            class_name=rx.cond(
                active,
                "ml-1.5 inline-flex items-center h-4 px-1 rounded bg-blue-100 text-blue-700 text-[10.5px] font-semibold",
                "ml-1.5 inline-flex items-center h-4 px-1 rounded bg-gray-100 text-gray-600 text-[10.5px] font-semibold",
            ),
        ),
        on_click=lambda: CrmState.set_tab(key),
        class_name=rx.cond(
            active,
            "inline-flex items-center gap-1.5 h-9 px-3 border-b-2 border-blue-600 text-[13px] font-semibold text-blue-700",
            "inline-flex items-center gap-1.5 h-9 px-3 border-b-2 border-transparent text-[13px] font-medium text-gray-500 hover:text-gray-800",
        ),
    )


# ---------- Filters bar ----------
def _select_filter(value, options, on_change) -> rx.Component:
    return rx.el.div(
        rx.el.select(
            rx.foreach(options, lambda o: rx.el.option(o, value=o)),
            default_value=value,
            key=value,
            on_change=on_change,
            class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[13px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500",
        ),
        rx.icon(
            "chevron-down",
            class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
        ),
        class_name="relative",
    )


def _filters_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="h-3.5 w-3.5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
            ),
            rx.el.input(
                placeholder="Search by name, company, or email…",
                default_value=CrmState.search_query,
                on_change=CrmState.set_search.debounce(300),
                class_name="w-full h-9 pl-9 pr-3 rounded-md border border-gray-200 bg-white text-[13px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100",
            ),
            class_name="relative flex-1 min-w-[220px]",
        ),
        _select_filter(
            CrmState.stage_filter,
            CrmState.stage_options,
            CrmState.set_stage_filter,
        ),
        _select_filter(
            CrmState.status_filter,
            CrmState.status_options,
            CrmState.set_status_filter,
        ),
        _select_filter(
            CrmState.interest_filter,
            CrmState.interest_options,
            CrmState.set_interest_filter,
        ),
        rx.el.button(
            rx.icon("rotate-ccw", class_name="h-3.5 w-3.5"),
            "Reset",
            on_click=CrmState.reset_filters,
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-medium text-gray-700 hover:bg-gray-50 transition-colors",
        ),
        class_name="flex flex-wrap items-center gap-2.5 mb-4",
    )


# ---------- Pipeline strip ----------
def _pipeline_strip() -> rx.Component:
    def col(stage: str) -> rx.Component:
        return rx.el.button(
            rx.el.p(
                stage,
                class_name="text-[11px] font-semibold uppercase tracking-wider text-gray-500 truncate",
            ),
            rx.el.p(
                CrmState.pipeline_counts[stage].to_string(),
                class_name="mt-1 text-2xl font-semibold tracking-tight text-gray-900 leading-none",
            ),
            on_click=lambda: CrmState.set_stage_filter(stage),
            class_name="text-left p-3 rounded-lg border border-gray-200 bg-white hover:border-blue-300 hover:bg-blue-50/30 transition-colors min-w-0",
        )

    return rx.el.div(
        *[col(s) for s in LEAD_STAGES],
        class_name="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 mb-4",
    )


# ---------- Leads table ----------
def _lead_row(L: Lead) -> rx.Component:
    active = CrmState.selected_lead_id == L["id"]
    return rx.el.tr(
        rx.el.td(
            rx.el.button(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            L["initials"],
                            class_name="text-[10.5px] font-semibold text-blue-700",
                        ),
                        class_name="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center shrink-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            L["name"],
                            class_name="text-[13px] font-semibold text-gray-900 leading-tight text-left",
                        ),
                        rx.el.p(
                            L["email"],
                            class_name="text-[11.5px] text-gray-500 leading-tight text-left",
                        ),
                        class_name="flex flex-col min-w-0",
                    ),
                    class_name="flex items-center gap-3 min-w-0",
                ),
                on_click=lambda: CrmState.select_lead(L["id"]),
                class_name="w-full",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    L["company"],
                    class_name="text-[13px] font-medium text-gray-900",
                ),
                rx.el.p(
                    L["team_size"],
                    class_name="text-[11.5px] text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            _interest_pill(L["interest"]), class_name="px-4 py-3 align-middle"
        ),
        rx.el.td(_stage_pill(L["stage"]), class_name="px-4 py-3 align-middle"),
        rx.el.td(
            _priority_pill(L["priority"]), class_name="px-4 py-3 align-middle"
        ),
        rx.el.td(
            rx.el.p(
                L["owner"],
                class_name="text-[12.5px] font-medium text-gray-700",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                L["created"],
                class_name="text-[11.5px] text-gray-500",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("panel-right-open", class_name="h-3.5 w-3.5"),
                    on_click=lambda: CrmState.select_lead(L["id"]),
                    class_name="inline-flex items-center h-7 w-7 justify-center rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 transition-colors",
                    title="Open details",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                    on_click=lambda: CrmState.delete_lead(L["id"]),
                    class_name="inline-flex items-center h-7 w-7 justify-center rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                    title="Delete lead",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        class_name=rx.cond(
            active,
            "border-t border-gray-100 bg-blue-50/60 hover:bg-blue-50 transition-colors cursor-pointer",
            "border-t border-gray-100 hover:bg-gray-50/60 transition-colors cursor-pointer",
        ),
    )


def _leads_table() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Leads",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                CrmState.filtered_leads.length().to_string()
                + " of "
                + CrmState.leads.length().to_string()
                + " · captured from marketing site",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-14 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Lead", class_name=header_cls),
                        rx.el.th("Company", class_name=header_cls),
                        rx.el.th("Interest", class_name=header_cls),
                        rx.el.th("Stage", class_name=header_cls),
                        rx.el.th("Priority", class_name=header_cls),
                        rx.el.th("Owner", class_name=header_cls),
                        rx.el.th("Created", class_name=header_cls),
                        rx.el.th("Actions", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(rx.foreach(CrmState.filtered_leads, _lead_row)),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.cond(
            CrmState.filtered_leads.length() == 0,
            rx.el.div(
                rx.icon("inbox", class_name="h-6 w-6 text-gray-300"),
                rx.el.p(
                    "No leads match your filters",
                    class_name="mt-2 text-[13px] font-medium text-gray-700",
                ),
                rx.el.p(
                    "Reset filters or wait for new website submissions.",
                    class_name="text-[12px] text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center py-12 text-center",
            ),
            rx.fragment(),
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


# ---------- Lead detail side panel ----------
def _lead_detail() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        CrmState.selected_lead["initials"],
                        class_name="text-[12px] font-semibold text-blue-700",
                    ),
                    class_name="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        CrmState.selected_lead["name"],
                        class_name="text-[15px] font-semibold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        CrmState.selected_lead["email"],
                        class_name="text-[12px] text-gray-500 leading-tight",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-3 min-w-0",
            ),
            rx.el.div(
                _stage_pill(CrmState.selected_lead["stage"]),
                _priority_pill(CrmState.selected_lead["priority"]),
                class_name="flex items-center gap-1.5 mt-3 flex-wrap",
            ),
            class_name="pb-4 border-b border-gray-100",
        ),
        # Field grid
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Company",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    CrmState.selected_lead["company"],
                    class_name="mt-0.5 text-[13px] font-medium text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Team size",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    CrmState.selected_lead["team_size"],
                    class_name="mt-0.5 text-[13px] font-medium text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Phone",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    rx.cond(
                        CrmState.selected_lead["phone"] != "",
                        CrmState.selected_lead["phone"],
                        "—",
                    ),
                    class_name="mt-0.5 text-[13px] font-medium text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Source",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    CrmState.selected_lead["source"],
                    class_name="mt-0.5 text-[13px] font-medium text-gray-900",
                ),
            ),
            class_name="mt-4 grid grid-cols-2 gap-3",
        ),
        # Message
        rx.el.div(
            rx.el.p(
                "Message",
                class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.p(
                rx.cond(
                    CrmState.selected_lead["message"] != "",
                    CrmState.selected_lead["message"],
                    "(no message provided)",
                ),
                class_name="mt-1.5 text-[13px] text-gray-700 leading-relaxed",
            ),
            class_name="mt-4 p-3 rounded-md border border-gray-200 bg-gray-50/60",
        ),
        # Stage + status + owner controls
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Stage",
                    class_name="text-[11px] font-semibold text-gray-700 mb-1",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            CrmState.stage_choices,
                            lambda s: rx.el.option(s, value=s),
                        ),
                        default_value=CrmState.selected_lead["stage"],
                        key=CrmState.selected_lead["stage"],
                        on_change=lambda v: CrmState.update_stage(
                            CrmState.selected_lead_id, v
                        ),
                        class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[12.5px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 w-full",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.label(
                    "Owner",
                    class_name="text-[11px] font-semibold text-gray-700 mb-1",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            CrmState.owner_choices,
                            lambda o: rx.el.option(o, value=o),
                        ),
                        default_value=CrmState.selected_lead["owner"],
                        key=CrmState.selected_lead["owner"],
                        on_change=lambda v: CrmState.assign_owner(
                            CrmState.selected_lead_id, v
                        ),
                        class_name="h-9 pl-3 pr-8 rounded-md border border-gray-200 bg-white text-[12.5px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500 w-full",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="h-3 w-3 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="flex flex-col",
            ),
            class_name="mt-4 grid grid-cols-2 gap-3",
        ),
        # Won / Lost quick actions
        rx.el.div(
            rx.el.button(
                rx.icon("check", class_name="h-3.5 w-3.5"),
                "Mark won",
                on_click=lambda: CrmState.update_status(
                    CrmState.selected_lead_id, "won"
                ),
                class_name="inline-flex items-center justify-center gap-1.5 h-8 px-3 rounded-md bg-emerald-600 text-[12px] font-semibold text-white hover:bg-emerald-700 transition-colors flex-1",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-3.5 w-3.5"),
                "Mark lost",
                on_click=lambda: CrmState.update_status(
                    CrmState.selected_lead_id, "lost"
                ),
                class_name="inline-flex items-center justify-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors flex-1",
            ),
            rx.el.button(
                rx.icon("rotate-ccw", class_name="h-3.5 w-3.5"),
                on_click=lambda: CrmState.update_status(
                    CrmState.selected_lead_id, "open"
                ),
                class_name="inline-flex items-center justify-center h-8 w-8 rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 transition-colors",
                title="Reopen",
            ),
            class_name="mt-3 flex items-center gap-1.5",
        ),
        # Notes
        rx.el.div(
            rx.el.p(
                "Activity",
                class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 mb-2",
            ),
            rx.cond(
                CrmState.selected_lead["notes"].length() > 0,
                rx.el.div(
                    rx.foreach(
                        CrmState.selected_lead["notes"],
                        lambda n: rx.el.div(
                            rx.icon(
                                "message-circle",
                                class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    n["body"],
                                    class_name="text-[12.5px] text-gray-800 leading-snug",
                                ),
                                rx.el.p(
                                    n["author"] + " · " + n["when"],
                                    class_name="mt-0.5 text-[11px] text-gray-500",
                                ),
                                class_name="flex flex-col min-w-0",
                            ),
                            class_name="flex items-start gap-2 p-2.5 rounded-md border border-gray-200 bg-white",
                        ),
                    ),
                    class_name="flex flex-col gap-1.5",
                ),
                rx.el.p(
                    "No activity yet.",
                    class_name="text-[12px] text-gray-500",
                ),
            ),
            rx.el.form(
                rx.el.textarea(
                    name="note",
                    placeholder="Add a note or activity update…",
                    rows=2,
                    class_name="p-2.5 rounded-md border border-gray-200 bg-white text-[12.5px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100 w-full resize-none",
                ),
                rx.el.button(
                    rx.icon("send", class_name="h-3.5 w-3.5"),
                    "Add note",
                    type="submit",
                    class_name="mt-2 inline-flex items-center gap-1.5 h-8 px-3 rounded-md bg-blue-600 text-[12px] font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
                on_submit=CrmState.add_note,
                reset_on_submit=True,
                class_name="mt-3",
            ),
            class_name="mt-5 pt-4 border-t border-gray-100",
        ),
        class_name="p-5 rounded-xl border border-gray-200 bg-white sticky top-20",
    )


# ---------- Leads tab body ----------
def _leads_body() -> rx.Component:
    return rx.el.div(
        _pipeline_strip(),
        _filters_bar(),
        rx.el.div(
            rx.el.div(_leads_table(), class_name="lg:col-span-8"),
            rx.el.div(_lead_detail(), class_name="lg:col-span-4"),
            class_name="grid grid-cols-1 lg:grid-cols-12 gap-4",
        ),
    )


# ---------- Customers tab ----------
def _customer_row(u: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        u["initials"],
                        class_name="text-[10.5px] font-semibold text-blue-700",
                    ),
                    class_name="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        u["name"],
                        class_name="text-[13px] font-semibold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        u["email"],
                        class_name="text-[11.5px] text-gray-500 leading-tight",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-3 min-w-0",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                u["company"],
                class_name="text-[12.5px] font-medium text-gray-800",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.match(
                u["role"],
                (
                    "platform_admin",
                    rx.el.span(
                        "Platform admin",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
                    ),
                ),
                (
                    "owner",
                    rx.el.span(
                        "Owner",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
                    ),
                ),
                (
                    "admin",
                    rx.el.span(
                        "Admin",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-violet-50 text-violet-700",
                    ),
                ),
                rx.el.span(
                    "Member",
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-gray-100 text-gray-700",
                ),
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                u["last_active"],
                class_name="text-[12px] text-gray-600",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50/60 transition-colors",
    )


def _customers_body() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Customer directory",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Every user across every paying workspace — inspect and cross-reference against leads.",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-14 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("User", class_name=header_cls),
                        rx.el.th("Workspace", class_name=header_cls),
                        rx.el.th("Role", class_name=header_cls),
                        rx.el.th("Last active", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(rx.foreach(AuthState.admin_users, _customer_row)),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


# ---------- Workspaces tab ----------
def _workspace_row(c: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon("building-2", class_name="h-4 w-4 text-blue-600"),
                    class_name="h-8 w-8 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        c["name"],
                        class_name="text-[13px] font-semibold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        f"{c['domain']} · {c['created']}",
                        class_name="text-[11.5px] text-gray-500 leading-tight",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-3 min-w-0",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.span(
                c["plan"],
                class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.match(
                c["status"],
                (
                    "active",
                    rx.el.span(
                        rx.el.span(
                            class_name="h-1.5 w-1.5 rounded-full bg-emerald-500"
                        ),
                        "Active",
                        class_name="inline-flex items-center gap-1.5 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
                    ),
                ),
                (
                    "trialing",
                    rx.el.span(
                        "Trial",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
                    ),
                ),
                rx.el.span(
                    "Suspended",
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
                ),
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                c["users"].to_string() + " / " + c["seats_limit"].to_string(),
                class_name="text-[12.5px] font-semibold text-gray-900",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.p(
                c["contracts_reviewed"].to_string()
                + " / "
                + c["contracts_limit"].to_string(),
                class_name="text-[12.5px] font-semibold text-gray-900",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        rx.el.td(
            rx.el.a(
                "Open",
                rx.icon("arrow-up-right", class_name="h-3.5 w-3.5"),
                href="/admin",
                class_name="inline-flex items-center gap-1 h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
            ),
            class_name="px-4 py-3 align-middle",
        ),
        class_name="border-t border-gray-100 hover:bg-gray-50/60 transition-colors",
    )


def _workspaces_body() -> rx.Component:
    header_cls = "px-4 py-2.5 text-left text-[10.5px] font-semibold uppercase tracking-wider text-gray-500 bg-gray-50/70 border-b border-gray-200"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Customer workspaces",
                class_name="text-[13.5px] font-semibold text-gray-900",
            ),
            rx.el.p(
                "Inspect any workspace's plan, seats, and usage. Manage plan changes in Platform admin.",
                class_name="text-[12px] text-gray-500 mt-0.5",
            ),
            class_name="px-4 h-14 flex flex-col justify-center border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Workspace", class_name=header_cls),
                        rx.el.th("Plan", class_name=header_cls),
                        rx.el.th("Status", class_name=header_cls),
                        rx.el.th("Seats", class_name=header_cls),
                        rx.el.th("Usage", class_name=header_cls),
                        rx.el.th("", class_name=header_cls),
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(AuthState.admin_companies, _workspace_row)
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


# ---------- Email drafts tab ----------
def _draft_card(d: EmailDraft) -> rx.Component:
    is_sent = d["status"] == "sent"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        rx.cond(
                            d["kind"] == "internal",
                            "shield-alert",
                            "mail",
                        ),
                        class_name=rx.cond(
                            d["kind"] == "internal",
                            "h-4 w-4 text-amber-600",
                            "h-4 w-4 text-blue-600",
                        ),
                    ),
                    class_name=rx.cond(
                        d["kind"] == "internal",
                        "h-8 w-8 rounded-md bg-amber-50 border border-amber-100 flex items-center justify-center shrink-0",
                        "h-8 w-8 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        d["subject"],
                        class_name="text-[13.5px] font-semibold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        "To: " + d["to_name"] + " <" + d["to_email"] + ">",
                        class_name="text-[11.5px] text-gray-500 leading-tight mt-0.5",
                    ),
                    rx.el.p(
                        "From: "
                        + d["from_name"]
                        + " <"
                        + d["from_email"]
                        + ">",
                        class_name="text-[11px] text-gray-500 leading-tight",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-start gap-3 min-w-0 flex-1",
            ),
            rx.el.div(
                rx.el.span(
                    d["template"],
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-gray-100 text-gray-700",
                ),
                rx.cond(
                    is_sent,
                    rx.el.span(
                        rx.icon("check", class_name="h-3 w-3"),
                        "Sent",
                        class_name="inline-flex items-center gap-1 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
                    ),
                    rx.el.span(
                        rx.el.span(
                            class_name="h-1.5 w-1.5 rounded-full bg-blue-500"
                        ),
                        "Draft",
                        class_name="inline-flex items-center gap-1.5 h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
                    ),
                ),
                class_name="flex items-center gap-1.5 shrink-0",
            ),
            class_name="flex items-start justify-between gap-3 flex-wrap",
        ),
        rx.el.div(
            rx.el.p(
                d["body"],
                class_name="text-[12.5px] text-gray-700 leading-relaxed whitespace-pre-line",
            ),
            class_name="mt-3 p-3 rounded-md border border-gray-200 bg-gray-50/60 max-h-40 overflow-auto",
        ),
        rx.el.div(
            rx.el.p(
                "Lead: " + d["lead_id"] + " · " + d["created"],
                class_name="text-[11px] text-gray-500 mr-auto",
            ),
            rx.el.button(
                rx.icon("copy", class_name="h-3.5 w-3.5"),
                "Copy",
                on_click=lambda: CrmState.copy_email(d["id"]),
                class_name="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
            ),
            rx.cond(
                is_sent,
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="h-3.5 w-3.5"),
                    "Revert to draft",
                    on_click=lambda: CrmState.mark_email_draft(d["id"]),
                    class_name="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
                ),
                rx.el.button(
                    rx.icon("send", class_name="h-3.5 w-3.5"),
                    "Mark sent",
                    on_click=lambda: CrmState.mark_email_sent(d["id"]),
                    class_name="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md bg-blue-600 text-[12px] font-semibold text-white hover:bg-blue-700 transition-colors",
                ),
            ),
            rx.el.button(
                rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                on_click=lambda: CrmState.delete_email(d["id"]),
                class_name="inline-flex items-center justify-center h-7 w-7 rounded-md border border-gray-200 bg-white text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                title="Delete draft",
            ),
            class_name="mt-3 flex items-center gap-1.5 flex-wrap pt-3 border-t border-gray-100",
        ),
        class_name="p-4 rounded-xl border border-gray-200 bg-white",
    )


def _email_filter_button(key: str, label: str) -> rx.Component:
    active = CrmState.lead_email_filter == key
    return rx.el.button(
        label,
        on_click=lambda: CrmState.set_email_filter(key),
        class_name=rx.cond(
            active,
            "h-8 px-3 rounded-md bg-white text-[12.5px] font-semibold text-gray-900 shadow-sm border border-gray-200",
            "h-8 px-3 rounded-md text-[12.5px] font-semibold text-gray-500 hover:text-gray-800",
        ),
    )


def _emails_body() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Prepared notifications",
                    class_name="text-[13.5px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Every website submission auto-generates a customer acknowledgement and an internal alert. Copy, send manually, or wire to a provider later.",
                    class_name="text-[12px] text-gray-500 mt-0.5 max-w-2xl",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                _email_filter_button("All", "All"),
                _email_filter_button("draft", "Drafts"),
                _email_filter_button("sent", "Sent"),
                class_name="ml-auto inline-flex items-center gap-1 p-1 rounded-lg bg-gray-100 border border-gray-200",
            ),
            class_name="flex items-start justify-between gap-3 flex-wrap mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "info",
                    class_name="h-3.5 w-3.5 text-blue-600 mt-0.5 shrink-0",
                ),
                rx.el.p(
                    "No email provider is connected yet — drafts are stored locally. When you plug in a provider (Postmark, Resend, SES), each draft can be sent with one click.",
                    class_name="text-[12.5px] text-gray-700 leading-relaxed",
                ),
                class_name="flex items-start gap-2",
            ),
            class_name="mb-4 p-3 rounded-md border border-blue-100 bg-blue-50/40",
        ),
        rx.el.div(
            rx.foreach(CrmState.filtered_drafts, _draft_card),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-3",
        ),
        rx.cond(
            CrmState.filtered_drafts.length() == 0,
            rx.el.div(
                rx.icon("mail-x", class_name="h-6 w-6 text-gray-300"),
                rx.el.p(
                    "No email notifications yet",
                    class_name="mt-2 text-[13px] font-medium text-gray-700",
                ),
                rx.el.p(
                    "Drafts will appear here as leads come in.",
                    class_name="text-[12px] text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center py-12 text-center",
            ),
            rx.fragment(),
        ),
    )


# ---------- Header actions + KPIs ----------
def _kpis() -> rx.Component:
    return rx.el.div(
        stat_card(
            "Total leads",
            CrmState.stats["total"].to_string(),
            "Captured from the marketing site",
            "users",
        ),
        stat_card(
            "New this batch",
            CrmState.stats["new"].to_string(),
            "Awaiting first-touch outreach",
            "sparkles",
        ),
        stat_card(
            "Open pipeline",
            CrmState.stats["open"].to_string(),
            "Actively being worked",
            "trending-up",
        ),
        stat_card(
            "Closed won",
            CrmState.stats["won"].to_string(),
            "Converted to customers",
            "circle-check",
        ),
        class_name="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6",
    )


def _header_actions() -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.icon("external-link", class_name="h-3.5 w-3.5"),
            "View landing page",
            href="/#contact-sales",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
        ),
        rx.el.a(
            "Platform admin",
            rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
            href="/admin",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
        ),
        class_name="flex items-center gap-2 flex-wrap",
    )


def leads_page() -> rx.Component:
    return page_shell(
        "leads",
        rx.el.div(
            page_header(
                "Sales & customer CRM",
                "Every website inquiry lands here — track leads through your pipeline, inspect customer workspaces, and manage prepared email notifications.",
                _header_actions(),
            ),
            _kpis(),
            rx.el.div(
                rx.el.div(
                    _tab_button(
                        "leads",
                        "Leads",
                        "users",
                        CrmState.leads.length(),
                    ),
                    _tab_button(
                        "customers",
                        "Customers",
                        "user-check",
                        AuthState.admin_users.length(),
                    ),
                    _tab_button(
                        "workspaces",
                        "Workspaces",
                        "building-2",
                        AuthState.admin_companies.length(),
                    ),
                    _tab_button(
                        "emails",
                        "Email drafts",
                        "mail",
                        CrmState.email_drafts.length(),
                    ),
                    class_name="flex items-center gap-1 border-b border-gray-200 overflow-x-auto",
                ),
                rx.el.div(
                    rx.match(
                        CrmState.active_tab,
                        ("leads", _leads_body()),
                        ("customers", _customers_body()),
                        ("workspaces", _workspaces_body()),
                        ("emails", _emails_body()),
                        _leads_body(),
                    ),
                    class_name="pt-5",
                ),
            ),
        ),
    )
