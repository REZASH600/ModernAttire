from django.shortcuts import redirect


class RedirectIfAuthenticatedMixin:
    """
    A mixin that redirects authenticated users to a specified URL
    if they try to access a view meant for unauthenticated users.
    """

    redirect_url = "/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
