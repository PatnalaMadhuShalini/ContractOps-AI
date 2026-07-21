import reflex as rx
from app.states.review_state import ReviewState, STAGES


def _status_tracker() -> rx.Component:
    def _node(index: int, name: str) -> rx.Component:
        is_done = index < ReviewState.stage_index
        is_current = index == ReviewState.stage_index
        return rx.el.div(
            rx.el.div(
                rx.cond(
                    is_done,
                    rx.icon("check", class_name="h-3 w-3 text-white"),
                    rx.cond(
                        is_current,
                        rx.el.div(class_name="h-2 w-2 rounded-full bg-white"),
                        rx.el.div(
                            class_name="h-1.5 w-1.5 rounded-full bg-gray-300"
                        ),
                    ),
                ),
                class_name=rx.cond(
                    is_done,
                    "h-5 w-5 rounded-full bg-blue-600 flex items-center justify-center shrink-0",
                    rx.cond(
                        is_current,
                        "h-5 w-5 rounded-full bg-blue-600 flex items-center justify-center shrink-0 ring-4 ring-blue-100",
                        "h-5 w-5 rounded-full bg-white border border-gray-200 flex items-center justify-center shrink-0",
                    ),
                ),
            ),
            rx.el.p(
                name,
                class_name=rx.cond(
                    is_current,
                    "ml-2 text-[12.5px] font-semibold text-gray-900",
                    rx.cond(
                        is_done,
                        "ml-2 text-[12.5px] font-medium text-gray-700",
                        "ml-2 text-[12.5px] font-medium text-gray-400",
                    ),
                ),
            ),
            class_name="flex items-center shrink-0",
        )

    def _connector(index: int) -> rx.Component:
        return rx.el.div(
            class_name=rx.cond(
                index < ReviewState.stage_index,
                "flex-1 h-px bg-blue-600 mx-3",
                "flex-1 h-px bg-gray-200 mx-3",
            ),
        )

    return rx.el.div(
        _node(0, STAGES[0]),
        _connector(0),
        _node(1, STAGES[1]),
        _connector(1),
        _node(2, STAGES[2]),
        _connector(2),
        _node(3, STAGES[3]),
        class_name="flex items-center w-full",
    )


def _header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    "Contracts",
                    href="#",
                    class_name="text-[12px] font-medium text-gray-500 hover:text-gray-800",
                ),
                rx.icon("chevron-right", class_name="h-3 w-3 text-gray-400"),
                rx.el.span(
                    ReviewState.selected["type"],
                    class_name="text-[12px] font-medium text-gray-500",
                ),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.div(
                rx.el.h1(
                    ReviewState.selected["title"],
                    class_name="text-xl sm:text-2xl font-semibold tracking-tight text-gray-900",
                ),
                rx.el.span(
                    rx.icon("sparkles", class_name="h-3 w-3"),
                    "AI reviewed",
                    class_name="inline-flex items-center gap-1 h-6 px-2 rounded-md bg-blue-50 text-blue-700 text-[11px] font-semibold",
                ),
                class_name="mt-1 flex items-center gap-2 flex-wrap",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "building-2", class_name="h-3.5 w-3.5 text-gray-400"
                    ),
                    rx.el.span(
                        ReviewState.selected["counterparty"],
                        class_name="text-[12.5px] font-medium text-gray-700",
                    ),
                    class_name="inline-flex items-center gap-1.5",
                ),
                rx.el.div(
                    rx.icon(
                        "book-open", class_name="h-3.5 w-3.5 text-gray-400"
                    ),
                    rx.el.span(
                        ReviewState.selected["playbook"],
                        class_name="text-[12.5px] font-medium text-gray-700",
                    ),
                    class_name="inline-flex items-center gap-1.5",
                ),
                rx.el.div(
                    rx.icon(
                        "file-text", class_name="h-3.5 w-3.5 text-gray-400"
                    ),
                    rx.el.span(
                        ReviewState.selected["pages"].to_string() + " pages",
                        class_name="text-[12.5px] font-medium text-gray-700",
                    ),
                    class_name="inline-flex items-center gap-1.5",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            ReviewState.selected["owner_initials"],
                            class_name="text-[10px] font-semibold text-blue-700",
                        ),
                        class_name="h-5 w-5 rounded-full bg-blue-100 flex items-center justify-center",
                    ),
                    rx.el.span(
                        ReviewState.selected["owner"],
                        class_name="text-[12.5px] font-medium text-gray-700",
                    ),
                    class_name="inline-flex items-center gap-1.5",
                ),
                class_name="mt-3 flex flex-wrap items-center gap-x-5 gap-y-1.5",
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("download", class_name="h-3.5 w-3.5"),
                "Export",
                class_name="inline-flex items-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-[12.5px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
            ),
            rx.el.button(
                rx.icon("git-pull-request", class_name="h-3.5 w-3.5"),
                "Request changes",
                on_click=ReviewState.request_changes,
                class_name="inline-flex items-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-[12.5px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
            ),
            rx.el.button(
                rx.icon("send", class_name="h-3.5 w-3.5"),
                "Send for signature",
                on_click=ReviewState.send_for_signature,
                class_name="inline-flex items-center gap-1.5 h-8 px-3 rounded-md bg-blue-600 text-[12.5px] font-semibold text-white hover:bg-blue-700 transition-colors",
            ),
            class_name="flex items-center gap-2 flex-wrap",
        ),
        class_name="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4",
    )


def _summary_cards() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Risk score",
                    class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.div(
                    rx.el.p(
                        ReviewState.selected["risk_score"].to_string(),
                        class_name="text-3xl font-semibold tracking-tight text-gray-900 leading-none",
                    ),
                    rx.el.span(
                        "/ 100", class_name="text-[11.5px] text-gray-500"
                    ),
                    class_name="mt-2 flex items-baseline gap-1",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.div(
                    class_name=rx.cond(
                        ReviewState.selected["risk_score"] < 100,
                        "h-full bg-blue-600 rounded-full",
                        "h-full bg-emerald-500 rounded-full",
                    ),
                    style={
                        "width": ReviewState.selected["risk_score"].to_string()
                        + "%"
                    },
                ),
                class_name="mt-4 h-1.5 w-full rounded-full bg-gray-100 overflow-hidden",
            ),
            class_name="p-4 rounded-xl border border-gray-200 bg-white",
        ),
        rx.el.div(
            rx.el.p(
                "Playbook match",
                class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.div(
                rx.el.p(
                    ReviewState.playbook_match_pct.to_string() + "%",
                    class_name="text-3xl font-semibold tracking-tight text-gray-900 leading-none",
                ),
                class_name="mt-2",
            ),
            rx.el.p(
                ReviewState.selected["playbook"],
                class_name="mt-2 text-[12px] text-gray-600",
            ),
            class_name="p-4 rounded-xl border border-gray-200 bg-white",
        ),
        rx.el.div(
            rx.el.p(
                "Findings",
                class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.div(
                rx.el.p(
                    ReviewState.total_clauses.to_string(),
                    class_name="text-3xl font-semibold tracking-tight text-gray-900 leading-none",
                ),
                class_name="mt-2",
            ),
            rx.el.div(
                rx.el.span(
                    ReviewState.clause_counts["High"].to_string() + " high",
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
                ),
                rx.el.span(
                    ReviewState.clause_counts["Medium"].to_string() + " med",
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
                ),
                rx.el.span(
                    ReviewState.clause_counts["Low"].to_string() + " low",
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
                ),
                class_name="mt-2 flex items-center gap-1.5 flex-wrap",
            ),
            class_name="p-4 rounded-xl border border-gray-200 bg-white",
        ),
        rx.el.div(
            rx.el.p(
                "Value",
                class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.div(
                rx.el.p(
                    ReviewState.selected["value"],
                    class_name="text-2xl font-semibold tracking-tight text-gray-900 leading-none",
                ),
                class_name="mt-2",
            ),
            rx.el.p(
                "Priority · " + ReviewState.selected["priority"],
                class_name="mt-2 text-[12px] text-gray-600",
            ),
            class_name="p-4 rounded-xl border border-gray-200 bg-white",
        ),
        class_name="grid grid-cols-2 lg:grid-cols-4 gap-3",
    )


def _tab_button(label: str, key: str, icon: str) -> rx.Component:
    active = ReviewState.active_tab == key
    return rx.el.button(
        rx.icon(icon, class_name="h-3.5 w-3.5"),
        label,
        on_click=lambda: ReviewState.set_tab(key),
        class_name=rx.cond(
            active,
            "inline-flex items-center gap-1.5 h-9 px-3 border-b-2 border-blue-600 text-[13px] font-semibold text-blue-700",
            "inline-flex items-center gap-1.5 h-9 px-3 border-b-2 border-transparent text-[13px] font-medium text-gray-500 hover:text-gray-800",
        ),
    )


def _key_terms_panel() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            ReviewState.selected["key_terms"],
            lambda kt: rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            kt["icon"], class_name="h-3.5 w-3.5 text-blue-600"
                        ),
                        class_name="h-7 w-7 rounded-md bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
                    ),
                    rx.el.div(
                        rx.el.p(
                            kt["label"],
                            class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
                        ),
                        rx.el.p(
                            kt["value"],
                            class_name="mt-0.5 text-[13.5px] font-medium text-gray-900 leading-snug",
                        ),
                        class_name="flex flex-col min-w-0",
                    ),
                    class_name="flex items-start gap-3 min-w-0 flex-1",
                ),
                rx.el.span(
                    kt["confidence"].to_string() + "%",
                    class_name="text-[10.5px] font-semibold text-gray-500 bg-gray-100 rounded px-1.5 h-4 inline-flex items-center shrink-0",
                ),
                class_name="flex items-center gap-2 p-3 rounded-lg border border-gray-200 bg-white",
            ),
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 gap-2.5",
    )


def _clause_card(clause: dict) -> rx.Component:
    risk = clause["risk"]
    status = clause["playbook_status"]
    accepted = ReviewState.accepted_clauses.contains(clause["id"])
    rejected = ReviewState.rejected_clauses.contains(clause["id"])
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    clause["title"],
                    class_name="text-[14px] font-semibold text-gray-900 leading-snug",
                ),
                rx.el.p(
                    clause["category"],
                    class_name="mt-0.5 text-[11.5px] font-medium text-gray-500",
                ),
                class_name="flex flex-col min-w-0",
            ),
            rx.el.div(
                rx.match(
                    risk,
                    (
                        "High",
                        rx.el.span(
                            "High risk",
                            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
                        ),
                    ),
                    (
                        "Medium",
                        rx.el.span(
                            "Medium risk",
                            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
                        ),
                    ),
                    rx.el.span(
                        "Low risk",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
                    ),
                ),
                rx.match(
                    status,
                    (
                        "Deviates",
                        rx.el.span(
                            "Deviates from playbook",
                            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-red-50 text-red-700",
                        ),
                    ),
                    (
                        "Review",
                        rx.el.span(
                            "Needs review",
                            class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-700",
                        ),
                    ),
                    rx.el.span(
                        "Matches playbook",
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-700",
                    ),
                ),
                class_name="flex items-center gap-1.5 shrink-0",
            ),
            class_name="flex items-start justify-between gap-3 flex-wrap",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Contract language",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    clause["excerpt"],
                    class_name="mt-1.5 text-[13px] text-gray-800 leading-relaxed italic",
                ),
                class_name="p-3 rounded-md border border-gray-200 bg-gray-50/60",
            ),
            rx.el.div(
                rx.el.p(
                    "Playbook standard",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-blue-700",
                ),
                rx.el.p(
                    clause["playbook_standard"],
                    class_name="mt-1.5 text-[13px] text-gray-800 leading-relaxed",
                ),
                class_name="p-3 rounded-md border border-blue-100 bg-blue-50/40",
            ),
            class_name="mt-3 grid grid-cols-1 md:grid-cols-2 gap-2.5",
        ),
        rx.cond(
            clause["suggested_redline"] != "",
            rx.el.div(
                rx.el.div(
                    rx.icon("sparkles", class_name="h-3.5 w-3.5 text-blue-600"),
                    rx.el.p(
                        "AI suggested redline",
                        class_name="text-[11.5px] font-semibold text-gray-900",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.p(
                    clause["suggested_redline"],
                    class_name="mt-1.5 text-[13px] text-gray-800 leading-relaxed",
                ),
                class_name="mt-3 p-3 rounded-md border border-blue-200 bg-white",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.icon(
                "info", class_name="h-3.5 w-3.5 text-gray-400 mt-0.5 shrink-0"
            ),
            rx.el.p(
                clause["rationale"],
                class_name="text-[12.5px] text-gray-600 leading-snug",
            ),
            class_name="mt-3 flex items-start gap-1.5",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("check", class_name="h-3.5 w-3.5"),
                "Accept",
                on_click=lambda: ReviewState.accept_clause(clause["id"]),
                class_name=rx.cond(
                    accepted,
                    "inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md bg-emerald-600 text-[12px] font-semibold text-white",
                    "inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-emerald-50 hover:border-emerald-200 hover:text-emerald-700 transition-colors",
                ),
            ),
            rx.el.button(
                rx.icon("x", class_name="h-3.5 w-3.5"),
                "Reject",
                on_click=lambda: ReviewState.reject_clause(clause["id"]),
                class_name=rx.cond(
                    rejected,
                    "inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md bg-red-600 text-[12px] font-semibold text-white",
                    "inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-red-50 hover:border-red-200 hover:text-red-700 transition-colors",
                ),
            ),
            rx.el.button(
                rx.icon("message-square", class_name="h-3.5 w-3.5"),
                "Comment",
                class_name="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
            ),
            rx.el.button(
                rx.icon("scroll-text", class_name="h-3.5 w-3.5"),
                "View in contract",
                class_name="ml-auto inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md border border-transparent text-[12px] font-semibold text-blue-700 hover:bg-blue-50 transition-colors",
            ),
            class_name="mt-4 pt-3 border-t border-gray-100 flex items-center gap-1.5 flex-wrap",
        ),
        class_name="p-4 rounded-xl border border-gray-200 bg-white",
    )


def _clauses_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                ReviewState.total_clauses.to_string()
                + " clauses reviewed against "
                + ReviewState.selected["playbook"],
                class_name="text-[12.5px] text-gray-600",
            ),
            rx.el.button(
                rx.icon("check-check", class_name="h-3.5 w-3.5"),
                "Accept all suggestions",
                on_click=ReviewState.approve_all,
                class_name="ml-auto inline-flex items-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-[12.5px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
            ),
            class_name="flex items-center gap-2 flex-wrap mb-3",
        ),
        rx.el.div(
            rx.foreach(ReviewState.selected["clauses"], _clause_card),
            class_name="flex flex-col gap-3",
        ),
    )


def _playbook_row(clause: dict) -> rx.Component:
    status = clause["playbook_status"]
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                clause["title"],
                class_name="text-[13px] font-semibold text-gray-900",
            ),
            rx.el.p(
                clause["category"], class_name="text-[11.5px] text-gray-500"
            ),
            class_name="flex flex-col min-w-0 w-40 shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                "Contract",
                class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.p(
                clause["excerpt"],
                class_name="mt-1 text-[12.5px] text-gray-700 leading-snug line-clamp-3",
            ),
            class_name="flex-1 min-w-0 p-3 rounded-md bg-gray-50/70 border border-gray-100",
        ),
        rx.el.div(
            rx.el.p(
                "Playbook",
                class_name="text-[10.5px] font-semibold uppercase tracking-wider text-blue-700",
            ),
            rx.el.p(
                clause["playbook_standard"],
                class_name="mt-1 text-[12.5px] text-gray-700 leading-snug line-clamp-3",
            ),
            class_name="flex-1 min-w-0 p-3 rounded-md bg-blue-50/40 border border-blue-100",
        ),
        rx.el.div(
            rx.match(
                status,
                (
                    "Deviates",
                    rx.el.span(
                        "Deviates",
                        class_name="inline-flex items-center h-6 px-2 rounded text-[11px] font-semibold bg-red-50 text-red-700",
                    ),
                ),
                (
                    "Review",
                    rx.el.span(
                        "Review",
                        class_name="inline-flex items-center h-6 px-2 rounded text-[11px] font-semibold bg-amber-50 text-amber-700",
                    ),
                ),
                rx.el.span(
                    "Match",
                    class_name="inline-flex items-center h-6 px-2 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-700",
                ),
            ),
            class_name="w-24 shrink-0 flex items-center justify-end",
        ),
        class_name="flex items-stretch gap-3 p-3 border border-gray-200 rounded-xl bg-white",
    )


def _playbook_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Playbook: " + ReviewState.selected["playbook"],
                    class_name="text-[13px] font-semibold text-gray-900",
                ),
                rx.el.p(
                    ReviewState.playbook_match_pct.to_string()
                    + "% of clauses match your standard playbook",
                    class_name="mt-0.5 text-[12px] text-gray-600",
                ),
                class_name="flex flex-col",
            ),
            rx.el.a(
                rx.icon("external-link", class_name="h-3.5 w-3.5"),
                "Open playbook",
                href="#",
                class_name="ml-auto inline-flex items-center gap-1.5 h-8 px-3 rounded-md border border-gray-200 bg-white text-[12.5px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
            ),
            class_name="flex items-center gap-2 mb-3",
        ),
        rx.el.div(
            rx.foreach(ReviewState.selected["clauses"], _playbook_row),
            class_name="flex flex-col gap-2",
        ),
    )


def _activity_panel() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            ReviewState.selected["activity"],
            lambda a: rx.el.div(
                rx.el.div(
                    rx.icon(a["icon"], class_name="h-3.5 w-3.5 text-blue-600"),
                    class_name="h-7 w-7 rounded-full bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        a["action"],
                        class_name="text-[13px] font-medium text-gray-900 leading-snug",
                    ),
                    rx.el.p(
                        a["actor"] + " · " + a["when"],
                        class_name="text-[11.5px] text-gray-500",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-start gap-3 p-3 rounded-lg border border-gray-200 bg-white",
            ),
        ),
        class_name="flex flex-col gap-2",
    )


def _tabs() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            _tab_button("Key terms", "terms", "tags"),
            _tab_button("Clause review", "clauses", "scan-search"),
            _tab_button("Playbook", "playbook", "book-open"),
            _tab_button("Activity", "activity", "activity"),
            class_name="flex items-center gap-1 border-b border-gray-200 overflow-x-auto",
        ),
        rx.el.div(
            rx.match(
                ReviewState.active_tab,
                ("terms", _key_terms_panel()),
                ("clauses", _clauses_panel()),
                ("playbook", _playbook_panel()),
                ("activity", _activity_panel()),
                _key_terms_panel(),
            ),
            class_name="pt-5",
        ),
        class_name="mt-6",
    )


def _stage_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                "Status",
                class_name="text-[11.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.button(
                rx.icon("arrow-right", class_name="h-3.5 w-3.5"),
                "Advance stage",
                on_click=ReviewState.advance_stage,
                class_name="ml-auto inline-flex items-center gap-1.5 h-7 px-2.5 rounded-md border border-gray-200 bg-white text-[12px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
            ),
            class_name="flex items-center mb-4",
        ),
        _status_tracker(),
        class_name="p-4 rounded-xl border border-gray-200 bg-white",
    )


def detail_panel() -> rx.Component:
    return rx.el.div(
        _header(),
        rx.el.div(
            _summary_cards(),
            class_name="mt-6",
        ),
        rx.el.div(
            _stage_bar(),
            class_name="mt-4",
        ),
        _tabs(),
        class_name="flex flex-col",
    )
