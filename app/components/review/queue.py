import reflex as rx
from app.states.review_state import ReviewState, Contract


def _risk_pill(risk: str) -> rx.Component:
    return rx.match(
        risk,
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


def _type_pill(t: str) -> rx.Component:
    return rx.el.span(
        t,
        class_name="inline-flex items-center h-5 px-1.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-700",
    )


def _queue_row(c: Contract) -> rx.Component:
    active = ReviewState.selected_id == c["id"]
    return rx.el.button(
        rx.el.div(
            rx.icon("file-text", class_name="h-4 w-4 text-gray-500 shrink-0"),
            rx.el.div(
                rx.el.p(
                    c["title"],
                    class_name="text-[13px] font-medium text-gray-900 leading-tight truncate text-left",
                ),
                rx.el.p(
                    f"{c['counterparty']} · {c['updated']}",
                    class_name="text-[11.5px] text-gray-500 leading-tight truncate text-left",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-center gap-2.5 min-w-0 flex-1",
        ),
        rx.el.div(
            _type_pill(c["type"]),
            _risk_pill(c["priority"]),
            class_name="flex items-center gap-1.5 shrink-0",
        ),
        on_click=lambda: ReviewState.select_contract(c["id"]),
        class_name=rx.cond(
            active,
            "w-full flex items-center gap-2 px-3 py-2.5 border-l-2 border-blue-600 bg-blue-50/60 hover:bg-blue-50 transition-colors",
            "w-full flex items-center gap-2 px-3 py-2.5 border-l-2 border-transparent hover:bg-gray-50 transition-colors",
        ),
    )


def _upload_zone() -> rx.Component:
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud-upload", class_name="h-5 w-5 text-gray-400"),
                rx.el.p(
                    "Drop contracts or click to upload",
                    class_name="text-[12.5px] font-medium text-gray-700",
                ),
                rx.el.p(
                    "PDF, DOCX up to 25MB",
                    class_name="text-[11px] text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center gap-1 py-4",
            ),
            id="contract_upload",
            accept={
                "application/pdf": [".pdf"],
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
                    ".docx"
                ],
                "application/msword": [".doc"],
            },
            multiple=True,
            max_files=10,
            on_drop=ReviewState.handle_upload(
                rx.upload_files(upload_id="contract_upload")
            ),
            class_name="block w-full rounded-lg border border-dashed border-gray-300 bg-gray-50/50 hover:border-blue-400 hover:bg-blue-50/30 transition-colors cursor-pointer",
        ),
        rx.cond(
            ReviewState.upload_files.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Recently uploaded",
                        class_name="text-[10.5px] font-semibold uppercase tracking-wider text-gray-500",
                    ),
                    rx.el.button(
                        "Clear",
                        on_click=ReviewState.clear_uploads,
                        class_name="ml-auto text-[11px] font-medium text-gray-500 hover:text-gray-800",
                    ),
                    class_name="flex items-center px-1",
                ),
                rx.foreach(
                    ReviewState.upload_files,
                    lambda f: rx.el.div(
                        rx.icon(
                            "file-check-2",
                            class_name="h-3.5 w-3.5 text-emerald-600 shrink-0",
                        ),
                        rx.el.p(
                            f,
                            class_name="text-[12px] font-medium text-gray-700 truncate",
                        ),
                        rx.el.span(
                            "Queued",
                            class_name="ml-auto text-[10.5px] font-semibold text-blue-700 bg-blue-50 rounded px-1.5 h-4 inline-flex items-center",
                        ),
                        class_name="flex items-center gap-2 px-2 py-1.5 rounded-md border border-gray-200 bg-white",
                    ),
                ),
                class_name="mt-2 flex flex-col gap-1.5",
            ),
            rx.fragment(),
        ),
        class_name="p-3 border-b border-gray-200",
    )


def queue_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Queue",
                    class_name="text-[13px] font-semibold text-gray-900",
                ),
                rx.el.span(
                    ReviewState.filtered_contracts.length().to_string(),
                    class_name="ml-auto inline-flex items-center h-5 px-1.5 rounded bg-gray-100 text-[11px] font-semibold text-gray-600",
                ),
                class_name="flex items-center px-3 h-10 border-b border-gray-200",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="h-3.5 w-3.5 text-gray-400 absolute left-2.5 top-1/2 -translate-y-1/2",
                    ),
                    rx.el.input(
                        placeholder="Search contracts",
                        default_value=ReviewState.search_query,
                        on_change=ReviewState.set_search.debounce(300),
                        class_name="w-full h-8 pl-7 pr-2 rounded-md border border-gray-200 bg-white text-[12.5px] text-gray-800 placeholder-gray-400 focus:outline-hidden focus:border-blue-500 focus:ring-2 focus:ring-blue-100",
                    ),
                    class_name="relative",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                ReviewState.contract_types,
                                lambda t: rx.el.option(t, value=t),
                            ),
                            value=ReviewState.filter_type,
                            on_change=ReviewState.set_type_filter,
                            class_name="w-full h-8 pl-2 pr-7 rounded-md border border-gray-200 bg-white text-[12px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="h-3 w-3 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                        ),
                        class_name="relative flex-1",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                ReviewState.stage_options,
                                lambda t: rx.el.option(t, value=t),
                            ),
                            value=ReviewState.filter_stage,
                            on_change=ReviewState.set_stage_filter,
                            class_name="w-full h-8 pl-2 pr-7 rounded-md border border-gray-200 bg-white text-[12px] font-medium text-gray-700 appearance-none cursor-pointer focus:outline-hidden focus:border-blue-500",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="h-3 w-3 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                        ),
                        class_name="relative flex-1",
                    ),
                    class_name="mt-2 flex items-center gap-1.5",
                ),
                class_name="p-3 border-b border-gray-200",
            ),
            _upload_zone(),
            rx.el.div(
                rx.foreach(ReviewState.filtered_contracts, _queue_row),
                class_name="flex flex-col divide-y divide-gray-100",
            ),
            class_name="flex flex-col",
        ),
        class_name="border border-gray-200 rounded-xl bg-white overflow-hidden",
    )
