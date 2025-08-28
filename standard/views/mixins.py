"""standard.views.mixins - A variety of mixins for views.

### ProjectNameMixin - A mixin class to add the project name to a views context data.

"""

from django.conf import settings


class ProjectNameMixin:
    """
    A mixin class to add the project name to a views context data.

    Explanation:
    This mixin provides a method to update the context data by adding the project name
    from settings.PROJECT_NAME.

    Args:
    - self

    Returns:
    A dictionary containing the updated context data with the project name included.
    """

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["project_name"] = settings.PROJECT_NAME
        return kwargs
