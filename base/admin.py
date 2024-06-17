from django.contrib import admin
# Register your models here.


from .models import Room, Topic, User, Reservation, Reservation2, Reservation3, Reservation4
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Reservation2)
admin.site.register(Reservation3)
admin.site.register(Reservation4)

admin.site.register(Topic)



