from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Recruiter, Recruit, Transaction, Referral

admin.site.register(Recruiter)
admin.site.register(Recruit)


class ReferralAdmin(ModelAdmin):
    list_display = ["recruiter", "recruit", "commission", "time_stamp"]


admin.site.register(Referral, ReferralAdmin)


class TransactionAdmin(ModelAdmin):
    list_display = ["recruit", "amount", "time_stamp"]


admin.site.register(Transaction, TransactionAdmin)
