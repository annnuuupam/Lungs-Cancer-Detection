from django.urls import path
from online_test import views
app_name='user'
urlpatterns = [
    path("",views.welcome,name='welcome'),
    path("signup",views.signup,name='signup'),
    path("store_user",views.store_user,name='store_user'),
    path("login",views.login,name='login'),
    path("homepage",views.homepage,name='homepage'),
    path("profile",views.profile,name='profile'),
    path("profile_save",views.profile_save,name='profile_save'),
    path("logout",views.logout,name='logout'),
    path("aboutUs",views.aboutUs,name='aboutUs'),
    path("view_profile",views.view_profile,name='view_profile'),
    path("pay",views.pay,name='pay'),
    path("success",views.success,name='success'),

    path('heart', views.heart, name="heart"),
    path('ChatBot', views.ChatBot, name="ChatBot"),

    path('xray', views.index, name='index'),
    path('import_data/', views.import_data, name='import_data'),
    path('train_model/', views.train_model, name='train_model'),
    path('predict_model/', views.predict_model, name='predict_model'),
]