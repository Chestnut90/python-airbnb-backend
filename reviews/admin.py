from django.contrib import admin

from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, queryset):
        word = self.value()
        if word:
            return queryset.filter(comment__contains=word)
        else:
            return queryset


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "comment",
    )

    list_filter = (
        WordFilter,
        "rating",
        "room__pet_friendly",
    )
