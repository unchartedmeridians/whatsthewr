from django.contrib import admin
from records.models import Game, Record, Category
from records.forms import RecordAdminForm

class RecordAdmin(admin.ModelAdmin):
    form = RecordAdminForm
    fields = ('game', 'game_as_text', 'category', 'category_as_text', 'runner',
              'time', 'link', 'approved', 'date_submitted', 'date_approved',
              'submitted_by', 'submitted_by_ip', 'approved_by')
    readonly_fields = ('date_submitted', 'date_approved', 'submitted_by',
                      'submitted_by_ip', 'approved_by')


admin.site.register(Game)
admin.site.register(Record, RecordAdmin)
admin.site.register(Category)
