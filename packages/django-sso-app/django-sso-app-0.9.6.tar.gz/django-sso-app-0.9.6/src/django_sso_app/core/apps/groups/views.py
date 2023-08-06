from rest_framework import viewsets
from rest_framework import permissions

from .serializers import GroupSerializer
from .models import Group


class GroupApiViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = 'pk'
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        """
        List groups
        """
        return super(GroupApiViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Group detail
        """
        return super(GroupApiViewSet, self).retrieve(request, pk, *args, **kwargs)
