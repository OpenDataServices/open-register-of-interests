from django.contrib import admin
import db.models as db


admin.site.register(db.Scrape)
admin.site.register(db.Body)
admin.site.register(db.Member)
admin.site.register(db.Declaration)
