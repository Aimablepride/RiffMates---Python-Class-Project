from typing import Any
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User 
from django.utils.html import format_html
from band.models import Musician, Band, UserProfile, Venue, Room
from datetime import datetime, date

class DecadeListFilter(admin.SimpleListFilter):
    title = 'decade of birth'
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        result = []
        this_year = datetime.now().year
        for i in range(1900, this_year, 10):
            result.append((i, f'{i}-{i+9}'))
        return result  

    def queryset(self, request, queryset):
        start = self.value()
        if start is None:
            return queryset
        start = int(start)
        return queryset.filter(birth__gte=date(start, 1, 1), birth__lte=date(start+9, 12, 31))

@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'show_weekday', 'show_bands')
    search_fields = ('first_name__startswith', 'last_name__startswith')
    list_filter = (DecadeListFilter,)

    def show_weekday(self, obj):
        return obj.birth.strftime('%A')
    show_weekday.short_description = 'Weekday of birth'

    def show_bands(self, obj):
        bands = obj.band_set.all()
        if len(bands) == 0:
            return format_html('<i>no bands</i>')

        plural = 's' if len(bands) > 1 else ''
        param = '?id__in=' + ','.join(str(band.id) for band in bands)
        url = reverse('admin:band_band_changelist') + param
        return format_html('<a href="{}">{} band{}</a>', url, len(bands), plural)
    show_bands.short_description = 'Bands'

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name__startswith',)

class UserProfileInline(admin.StackedInline): 
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin): 
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
admin.site.unregister(User) 
admin.site.register(User, UserAdmin)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "show_rooms")
    search_fields = ("name",)

    def show_rooms(self, obj):
        rooms = obj.room_set.all()
        if len(rooms) == 0:
            return format_html("<i>None</i>")
        plural = "s" if len(rooms) > 1 else ""
        param = "?venue__id__exact=" + str(obj.id)
        url = reverse("admin:band_room_changelist") + param
        return format_html('<a href="{}">{} room{}</a>', url, len(rooms), plural)
    show_rooms.short_description = "Rooms"

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "venue")
    search_fields = ("name", "venue__name")