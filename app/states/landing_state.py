import reflex as rx


class LandingState(rx.State):
    mobile_nav_open: bool = False
    billing_annual: bool = True

    @rx.event
    def toggle_mobile_nav(self):
        self.mobile_nav_open = not self.mobile_nav_open

    @rx.event
    def set_annual(self, annual: bool):
        self.billing_annual = annual
