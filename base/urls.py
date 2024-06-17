from django.urls import path
from .import views



urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.indexcard, name="index"),
    path('home', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('view-archive/', views.viewArchive, name="view-archive"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('borrow-room/<str:pk>/', views.BorrowRoom, name="borrow-room"),

    path('confirm-room/<str:pk>/', views.confirmresbtn, name="confirm-room"),
    path('update-user/', views.updateUser, name="update-user"),
    path('return-book/<str:pk>/', views.returnBook, name="return-book"),
    path('deny-book/<str:pk>/', views.denyBook, name="deny-book"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),

]
