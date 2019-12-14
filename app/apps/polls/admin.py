from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from .models import *


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Poll)
class PollAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
