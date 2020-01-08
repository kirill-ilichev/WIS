from rest_framework.permissions import BasePermission, SAFE_METHODS

from customers_app.models import Customer


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if request.method == 'PUT' or request.method == 'DELETE':
            if request.user.is_staff:
                return True

            is_owner = Customer.objects.get(pk=view.kwargs['pk']) == request.user.customer
            return bool(is_owner)
