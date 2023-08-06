from django.contrib.auth.mixins import AccessMixin
from django.views import View


class AdminSiteViewMixin(AccessMixin):
    """
    A mixin that checks administrator rights or staff
    """

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or user.is_authenticated and (not user.is_staff or not user.is_superuser):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdminSiteView(AdminSiteViewMixin, View):
    """
    A simple base view for admin site views
    """

    pass
