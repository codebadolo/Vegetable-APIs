from django.contrib.admin import AdminSite
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        
        # Add dynamic sidebar based on the user's group
        if request.user.is_superuser:
            context["sidebar_navigation"] = [
                {
                    "title": _("Admin Management"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("Products"),
                            "icon": "inventory",
                            "link": reverse_lazy("admin:product_product_changelist"),
                        },
                        {
                            "title": _("Categories"),
                            "icon": "category",
                            "link": reverse_lazy("admin:product_category_changelist"),
                        },
                        {
                            "title": _("Orders"),
                            "icon": "shopping_cart",
                            "link": reverse_lazy("admin:orders_order_changelist"),
                        },
                        {
                            "title": _("Customers"),
                            "icon": "person",
                            "link": reverse_lazy("admin:orders_customer_changelist"),
                        },
                        {
                            "title": _("Cards"),
                            "icon": "credit_card",
                            "link": reverse_lazy("admin:orders_card_changelist"),
                        },
                        {
                            "title": _("Vendors"),
                            "icon": "store",
                            "link": reverse_lazy("admin:vendors_vendor_changelist"),
                        },
                    ],
                },
            ]
        elif request.user.groups.filter(name='Vendor').exists():
            context["sidebar_navigation"] = [
                {
                    "title": _("Vendor Management"),
                    "separator": True,
                    "collapsible": True,
                    "items": [
                        {
                            "title": _("Products"),
                            "icon": "inventory",
                            "link": reverse_lazy("admin:product_product_changelist"),
                        },
                        {
                            "title": _("Categories"),
                            "icon": "category",
                            "link": reverse_lazy("admin:product_category_changelist"),
                        },
                        {
                            "title": _("Orders"),
                            "icon": "shopping_cart",
                            "link": reverse_lazy("admin:orders_order_changelist"),
                        },
                    ],
                },
            ]
        else:
            context["sidebar_navigation"] = []  # Default empty sidebar for other users
        
        return context

# Use the CustomAdminSite instead of the default one
custom_admin_site = CustomAdminSite(name='custom_admin')
