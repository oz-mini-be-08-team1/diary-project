from django.contrib import admin
from diary.models import Diary
# Register your models here.

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = (
        "title","mood","created_at","updated_at"
    )
    list_filter = ("mood","created_at")
    search_fields = ("title","tag","mood")
    readonly_fields = ("created_at","updated_at")
    fieldsets = (
        ("Diary Information",
         {"fields": ('title','detail','mood','tag')}
         ),
         ("Date",
          {"fields":("created_at","updated_at")},
          ),
    )
    add_fieldsets = (
        ("New Diary",
         {"classes":("wide"),
          "fields": ('title','mood','detail','tag')})
    )