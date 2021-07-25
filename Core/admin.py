from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import Recruiter, Recruit, Transaction, Referral
from .models.transaction import Commission, CommissionPayment

admin.site.register(Recruiter)
admin.site.register(Recruit)


class ReferralAdmin(ModelAdmin):
    list_display = ["recruiter", "recruit", "time_stamp"]


admin.site.register(Referral, ReferralAdmin)


class TransactionAdmin(ModelAdmin):
    list_display = ["recruit", "amount", "time_stamp"]


admin.site.register(Transaction, TransactionAdmin)


class CommissionPaymentTabularInline(TabularInline):
    model = CommissionPayment
    extra = 1

    def has_add_permission(self, request, obj):
        return not obj.completed


class CommissionAdmin(ModelAdmin):
    list_display = ["recruit", "commission", "transaction", "time_stamp"]
    inlines = [CommissionPaymentTabularInline]


admin.site.register(Commission, CommissionAdmin)
