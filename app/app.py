import reflex as rx

from app.components.navbar import navbar
from app.components.sidebar import sidebar
from app.components.hero import hero
from app.components.logos import logos
from app.components.metrics import metrics
from app.components.workflow import workflow
from app.components.features import features
from app.components.pricing import pricing
from app.components.cta import cta
from app.components.contact import contact_section
from app.components.footer import footer
from app.pages.review import review_page
from app.pages.approvals import approvals_page
from app.pages.clauses import clauses_page
from app.pages.analytics import analytics_page
from app.pages.settings import settings_page
from app.pages.login import login_page
from app.pages.signup import signup_page
from app.pages.workspace import workspace_page
from app.pages.admin import admin_page
from app.pages.leads import leads_page
from app.pages.billing import billing_page
from app.pages.admin_billing import admin_billing_page
from app.states.auth_state import AuthState


def index() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.el.div(
            sidebar(active="home"),
            rx.el.div(
                hero(),
                logos(),
                metrics(),
                workflow(),
                features(),
                pricing(),
                cta(),
                contact_section(),
                footer(),
                class_name="flex-1 min-w-0 bg-gray-50",
            ),
            class_name="flex items-start",
        ),
        class_name="font-['Inter'] bg-gray-50 text-gray-900 antialiased min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(review_page, route="/review")
app.add_page(approvals_page, route="/approvals")
app.add_page(clauses_page, route="/clauses")
app.add_page(analytics_page, route="/analytics")
app.add_page(settings_page, route="/settings")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(workspace_page, route="/workspace", on_load=AuthState.require_auth)
app.add_page(
    admin_page, route="/admin", on_load=AuthState.require_platform_admin
)
app.add_page(
    leads_page, route="/leads", on_load=AuthState.require_platform_admin
)
app.add_page(billing_page, route="/billing", on_load=AuthState.require_auth)
app.add_page(
    admin_billing_page,
    route="/admin/billing",
    on_load=AuthState.require_platform_admin,
)
