from django.contrib import admin

from . import models


@admin.register(models.Amenity)
class AmenityAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_display = (
        "pk",
        "name",
        "price",
        "kind",
        "owner",
        "total_amenities",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "^price",
        "=owner__username",  # using username field
    )
