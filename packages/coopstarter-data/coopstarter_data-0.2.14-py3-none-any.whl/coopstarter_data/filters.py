from rest_framework.filters import BaseFilterBackend


class ValidatedResourcesByStepFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(steps__urlid__icontains=view.kwargs['id'], review__status='validated')


class PendingResourceFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(review__status='pending').exclude(submitter__urlid=request.user.urlid)
