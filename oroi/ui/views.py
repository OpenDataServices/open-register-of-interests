from django.views.generic.base import TemplateView
from django.db.models import Count
import db.models as db

# Create your views here.
class StatsView(TemplateView):
    template_name = "stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = db.Member.objects.annotate(num_decs=Count('declaration')).order_by("-num_decs")
        return context