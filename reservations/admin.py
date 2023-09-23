from django.contrib import admin
from reservations.models import *


class ReservationInline(admin.StackedInline):
    model = Reservation
    extra = 0
    show_change_link = True
    
class PayInline(admin.StackedInline):
    model = Pay
    extra = 0
    show_change_link = True
admin.site.register(Pay)

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    show_change_link = True
admin.site.register(Review)


class ClientAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, ReservationInline]
admin.site.register(Client, ClientAdmin)


class UnitInline(admin.StackedInline):
    model = Unit
    extra = 0
    show_change_link = True
    
    
class UnitAdmin(admin.ModelAdmin):
    inlines = [ReservationInline,]
admin.site.register(Unit, UnitAdmin)

class PlaceAdmin(admin.ModelAdmin):
    inlines = [UnitInline,]
admin.site.register(Place, PlaceAdmin)


class ReservationAdmin(admin.ModelAdmin):
    inlines = [PayInline,]
admin.site.register(Reservation, ReservationAdmin)
