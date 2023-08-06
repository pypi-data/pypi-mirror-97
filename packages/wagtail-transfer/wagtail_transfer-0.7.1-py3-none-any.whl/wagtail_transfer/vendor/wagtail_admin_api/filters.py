from rest_framework.filters import BaseFilterBackend
from wagtail.core import hooks

from ..wagtail_api_v2.utils import BadRequestError, parse_boolean


class HasChildrenFilter(BaseFilterBackend):
    """
    Filters the queryset by checking if the pages have children or not.
    This is useful when you want to get just the branches or just the leaves.
    """
    def filter_queryset(self, request, queryset, view):
        if 'has_children' in request.GET:
            try:
                has_children_filter = parse_boolean(request.GET['has_children'])
            except ValueError:
                raise BadRequestError("has_children must be 'true' or 'false'")

            if has_children_filter is True:
                return queryset.filter(numchild__gt=0)
            else:
                return queryset.filter(numchild=0)

        return queryset


class ForExplorerFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if not hasattr(queryset, '_filtered_by_child_of'):
            raise BadRequestError("filtering without child_of is not supported")

        parent_page = queryset._filtered_by_child_of
        for hook in hooks.get_hooks('construct_explorer_page_queryset'):
            queryset = hook(parent_page, queryset, request)

        return queryset
