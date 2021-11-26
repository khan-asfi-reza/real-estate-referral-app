from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import Recruiter, Recruit, Transaction, Referral
from .models.transaction import Commission, CommissionTransaction

admin.site.register(Recruiter)
admin.site.register(Recruit)


class ReferralAdmin(ModelAdmin):
    list_display = ["recruiter", "recruit", "time_stamp"]


admin.site.register(Referral, ReferralAdmin)


class TransactionAdmin(ModelAdmin):
    list_display = ["recruit", "amount", "time_stamp"]


admin.site.register(Transaction, TransactionAdmin)


class CommissionAdmin(ModelAdmin):
    list_display = ["recruit", "commission", "transaction", 'completed', "time_stamp"]

    def get_readonly_fields(self, request, obj: Commission = None):
        if obj and not obj.completed and not obj.commission_transaction:
            return []
        else:
            return ['completed', 'commission_transaction']


admin.site.register(Commission, CommissionAdmin)


class CommissionInline(admin.TabularInline):
    model = Commission

    def has_add_permission(self, request, obj):
        return False


class CommissionPaymentAdmin(ModelAdmin):
    list_display = ["recruiter", "id", "amount", "time_stamp"]
    inlines = [CommissionInline]


admin.site.register(CommissionTransaction, CommissionPaymentAdmin)
