from django.views.generic import TemplateView

from ployst.core.providers import get_all_providers_meta


class HomeView(TemplateView):
    template_name = 'ui/main.html'

    def get_context_data(self, *args, **kwargs):
        """
        Add available providers to context.
        """
        data = super(HomeView, self).get_context_data(*args, **kwargs)
        providers = get_all_providers_meta()
        data.update({
            'providers': providers,
        })

        return data
