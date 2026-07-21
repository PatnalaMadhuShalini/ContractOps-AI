import reflex as rx
from app.components.page_shell import page_shell, page_header, stat_card
from app.states.clauses_state import ClausesState, ClauseTemplate


def _risk_pill(r: str) -> rx.Component:
    return rx.match(
        r,
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
    )


def _category_button(name: str) -> rx.Component:
    active = ClausesState.category_filter == name
    return rx.el.button(
        name,
        rx.el.span(
            ClausesState.category_counts.get(name, 0).to_string(),
            class_name=rx.cond(
                active,
                "ml-1.5 inline-flex items-center h-4 px-1 rounded bg-white/20 text-[10.5px] font-semibold text-white",
                "ml-1.5 inline-flex items-center h-4 px-1 rounded bg-gray-100 text-[10.5px] font-semibold text-gray-600",
            ),
        ),
        on_click=lambda: ClausesState.set_category(name),
        class_name=rx.cond(
            active,
            "inline-flex items-center h-8 px-3 rounded-md bg-blue-600 text-[12.5px] font-semibold text-white transition-colors",
            "inline-flex items-center h-8 px-3 rounded-md border border-gray-200 bg-white text-[12.5px] font-medium text-gray-700 hover:bg-gray-50 transition-colors",
        ),
    )


def _template_card(t: ClauseTemplate) -> rx.Component:
    selected = ClausesState.selected_id == t["id"]
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    t["category"],
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
                ),
                _risk_pill(t["risk_level"]),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.p(
                t["title"],
                class_name="mt-3 text-[14px] font-semibold text-gray-900 leading-snug text-left",
            ),
            rx.el.p(
                t["description"],
                class_name="mt-1.5 text-[12.5px] text-gray-600 leading-relaxed text-left line-clamp-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("users", class_name="h-3 w-3 text-gray-400"),
                    rx.el.span(
                        t["usage_count"].to_string() + " uses",
                        class_name="text-[11px] font-medium text-gray-600",
                    ),
                    class_name="inline-flex items-center gap-1",
                ),
                rx.el.div(
                    rx.icon("clock", class_name="h-3 w-3 text-gray-400"),
                    rx.el.span(
                        t["last_updated"],
                        class_name="text-[11px] font-medium text-gray-600",
                    ),
                    class_name="inline-flex items-center gap-1",
                ),
                class_name="mt-4 flex items-center gap-3",
            ),
            class_name="flex flex-col",
        ),
        on_click=lambda: ClausesState.select(t["id"]),
        class_name=rx.cond(
            selected,
            "text-left p-4 rounded-xl border-2 border-blue-600 bg-blue-50/30 transition-colors",
            "text-left p-4 rounded-xl border border-gray-200 bg-white hover:border-blue-300 hover:shadow-[0_1px_2px_rgba(0,0,0,0.04)] transition-all",
        ),
    )


def _grid() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
            ),
            rx.el.input(
                placeholder="Search clauses by title, tag, or content…",
                default_value=ClausesState.search_query,
                on_change=ClausesState.set_search.debounce(300),
                class_name="w-full h-10 pl-10 pr-3 rounded-md border border-gray-200 bg-white text-[13.5px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100",
            ),
            class_name="relative mb-4",
        ),
        rx.el.div(
            rx.foreach(ClausesState.categories, _category_button),
            class_name="flex flex-wrap items-center gap-1.5 mb-5",
        ),
        rx.el.div(
            rx.foreach(ClausesState.filtered, _template_card),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-3",
        ),
        rx.cond(
            ClausesState.filtered.length() == 0,
            rx.el.div(
                rx.icon("search-x", class_name="h-6 w-6 text-gray-300"),
                rx.el.p(
                    "No clauses match your filters",
                    class_name="mt-2 text-[13px] font-medium text-gray-700",
                ),
                class_name="flex flex-col items-center justify-center py-12 text-center",
            ),
            rx.fragment(),
        ),
    )


def _detail_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    ClausesState.selected["category"],
                    class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
                ),
                _risk_pill(ClausesState.selected["risk_level"]),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.h2(
                ClausesState.selected["title"],
                class_name="mt-3 text-[16px] font-semibold text-gray-900 leading-snug",
            ),
            rx.el.p(
                ClausesState.selected["description"],
                class_name="mt-1.5 text-[13px] text-gray-600 leading-relaxed",
            ),
            class_name="pb-4 border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.p(
                "Clause language",
                class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.p(
                ClausesState.selected["body"],
                class_name="mt-2 text-[13px] text-gray-800 leading-relaxed whitespace-pre-line",
            ),
            class_name="mt-4 p-3 rounded-md border border-gray-200 bg-gray-50/60",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Author",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    ClausesState.selected["author"],
                    class_name="mt-1 text-[13px] font-medium text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Last updated",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    ClausesState.selected["last_updated"],
                    class_name="mt-1 text-[13px] font-medium text-gray-900",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Uses",
                    class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                ),
                rx.el.p(
                    ClausesState.selected["usage_count"].to_string(),
                    class_name="mt-1 text-[13px] font-medium text-gray-900",
                ),
            ),
            class_name="mt-4 grid grid-cols-3 gap-2",
        ),
        rx.el.div(
            rx.el.p(
                "Tags",
                class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
            ),
            rx.el.div(
                rx.foreach(
                    ClausesState.selected["tags"],
                    lambda tag: rx.el.span(
                        tag,
                        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-medium bg-gray-100 text-gray-700",
                    ),
                ),
                class_name="mt-2 flex flex-wrap gap-1",
            ),
            class_name="mt-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("plus", class_name="h-3.5 w-3.5"),
                "Insert into contract",
                on_click=lambda: ClausesState.insert_clause(
                    ClausesState.selected_id
                ),
                class_name="inline-flex items-center justify-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors flex-1",
            ),
            rx.el.button(
                rx.cond(
                    ClausesState.copied_id == ClausesState.selected_id,
                    rx.icon("check", class_name="h-3.5 w-3.5"),
                    rx.icon("copy", class_name="h-3.5 w-3.5"),
                ),
                rx.cond(
                    ClausesState.copied_id == ClausesState.selected_id,
                    "Copied",
                    "Copy",
                ),
                on_click=lambda: ClausesState.copy_clause(
                    ClausesState.selected_id
                ),
                class_name="inline-flex items-center justify-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
            ),
            class_name="mt-5 flex items-center gap-2",
        ),
        class_name="p-5 rounded-xl border border-gray-200 bg-white sticky top-20",
    )


def _stats() -> rx.Component:
    return rx.el.div(
        stat_card(
            "Templates",
            ClausesState.templates.length().to_string(),
            "Approved clauses in your library",
            "library",
        ),
        stat_card(
            "Total uses",
            ClausesState.total_usage.to_string(),
            "Inserts across all contracts",
            "trending-up",
        ),
        stat_card(
            "Categories",
            (ClausesState.categories.length() - 1).to_string(),
            "Playbook areas covered",
            "layers",
        ),
        stat_card(
            "Contributors",
            "5",
            "Legal teammates authoring templates",
            "users",
        ),
        class_name="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6",
    )


def _header_actions() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("download", class_name="h-3.5 w-3.5"),
            "Export library",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md border border-gray-200 bg-white text-[13px] font-semibold text-gray-800 hover:bg-gray-50 transition-colors",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-3.5 w-3.5"),
            "New clause",
            class_name="inline-flex items-center gap-1.5 h-9 px-3 rounded-md bg-blue-600 text-[13px] font-semibold text-white hover:bg-blue-700 transition-colors",
        ),
        class_name="flex items-center gap-2",
    )


def clauses_page() -> rx.Component:
    return page_shell(
        "clauses",
        rx.el.div(
            page_header(
                "Clause library",
                "Reusable, pre-approved language your team can drop into any contract. Kept in sync with your playbook.",
                _header_actions(),
            ),
            _stats(),
            rx.el.div(
                rx.el.div(_grid(), class_name="lg:col-span-8"),
                rx.el.div(_detail_panel(), class_name="lg:col-span-4"),
                class_name="grid grid-cols-1 lg:grid-cols-12 gap-5",
            ),
        ),
    )
