from django.urls import path
from . import views


app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room_pk>/<int:year>-<int:month>-<int:date>", 
        views.createReservation, name="create"
    ),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path("<int:pk>/<str:verb>/", views.edit_reservation, name="edit"),
    #path("<int:pk>/delete/", views.DeleteReservationView.as_view(), name="delete"),
]
