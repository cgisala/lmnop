from django.contrib import admin

# Register your models here, for them to be displayed in the admin view

from .models import Venue, Artist, Note, Show, Profile, Rating

admin.site.register(Venue)
admin.site.register(Artist)
admin.site.register(Note)
admin.site.register(Show)
admin.site.register(Profile)
admin.site.register(Rating)