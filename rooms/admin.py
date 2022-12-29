from django.contrib import admin

from . import models


@admin.register(models.Amenity)
class AmenityAdmin(admin.ModelAdmin):

    list_display = ("name", "description", "created_at", "updated_at")
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass
