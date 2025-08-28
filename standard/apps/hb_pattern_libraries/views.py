from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class PatternLibraryOverView(TemplateView):
    template_name = "pattern_library/getting_started/overview.html"


class PatternLibraryCSS(TemplateView):
    template_name = "pattern_library/customize/css.html"


class PatternLibraryColors(TemplateView):
    template_name = "pattern_library/customize/colors.html"


class PatternLibraryTemplates(TemplateView):
    template_name = "pattern_library/customize/templates.html"


class PatternLibraryAlert(TemplateView):
    template_name = "pattern_library/components/alert/alerts.html"


class PatternLibraryAvatar(TemplateView):
    template_name = "pattern_library/components/avatar/avatar.html"


class PatternLibraryBadge(TemplateView):
    template_name = "pattern_library/components/badge/badge.html"


class PatternLibraryBtn(TemplateView):
    template_name = "pattern_library/components/button/buttons.html"


class PatternLibraryDatepicker(TemplateView):
    template_name = "pattern_library/components/datepicker/datepicker.html"


class PatternLibraryListGroupItem(TemplateView):
    template_name = "pattern_library/components/list_group_item/list_group_item.html"


class PatternLibraryTable(TemplateView):
    template_name = "pattern_library/components/table/table.html"


class PatternLibraryLink(TemplateView):
    template_name = "pattern_library/components/link/link.html"
