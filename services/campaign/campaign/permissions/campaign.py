from rest_framework.permissions import BasePermission


class IsCampaignOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.creator_id
