from djangoldp.filters import LocalObjectFilterBackend
from coopstarter_data.models import Resource
from coopstarter_data.filters import PendingResourceFilterBackend, ValidatedResourcesByStepFilterBackend
from coopstarter_data.permissions import PendingResourcePermissions
from djangoldp_i18n.views import I18nLDPViewSet


class ValidatedResourcesByStepViewSet(I18nLDPViewSet):
    model = Resource
    filter_backends = [ValidatedResourcesByStepFilterBackend, LocalObjectFilterBackend]


class PendingResourcesViewSet(I18nLDPViewSet):
    model = Resource
    filter_backends = [PendingResourceFilterBackend, LocalObjectFilterBackend]
    permission_classes = [PendingResourcePermissions]
