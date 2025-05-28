
from django.contrib import admin
from django.utils.text import Truncator  #1

from content.models import SeekingAd

@admin.register(SeekingAd)  #2
class SeekingAdAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "owner", "seeking", "show_ad")  #3

    def show_ad(self, obj):
        return Truncator(obj.content).words(5, truncate=' ...')  #4
    
    show_ad.short_description = "Ad"  #5
