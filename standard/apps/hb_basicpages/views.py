from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, TemplateView

from project_apps.chats.forms import ConversationItemForm, ConversationThreadForm
from project_apps.chats.models import ConversationThread
from standard.views.mixins import ProjectNameMixin


class HomePageView(ProjectNameMixin, LoginRequiredMixin, ListView):
    model = ConversationThread
    context_object_name = "conversation_threads"
    template_name = "home/homepagecontent.html"

    def get_queryset(self):
        return ConversationThread.objects.filter(
            created_by=self.request.user, chat_type="web"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["api_chats"] = ConversationThread.objects.filter(
            created_by=self.request.user, chat_type="api"
        )
        context["noa_chats"] = ConversationThread.objects.filter(
            created_by=self.request.user, chat_type="noa"
        )
        context["latest_conversation"] = (
            ConversationThread.objects.filter(created_by=self.request.user)
            .order_by("-modified_at")
            .first()
        )
        # Add the ConversationItemForm to the context
        context["form"] = ConversationItemForm()
        context["new_chat_form"] = ConversationThreadForm()
        return context


class AboutPageView(ProjectNameMixin, LoginRequiredMixin, TemplateView):
    template_name = "about.html"


class TnCsPageView(ProjectNameMixin, LoginRequiredMixin, TemplateView):
    template_name = "tncs.html"
