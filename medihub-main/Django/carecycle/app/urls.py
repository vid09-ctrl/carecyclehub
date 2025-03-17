from django.urls import path
from . import views  # Ensure views is properly imported

urlpatterns = [
    path('', views.index, name='index'),  # Index page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('signin/', views.signin, name='signin'),  # Signin page
    path('userlogout/', views.userlogout, name='userlogout'),
    path('order/',views.order, name='order'),
    path('forgotpass/',views.forgotpass,name="forgotpass"),
    path('resetpassword/<str:uname>/',views.resetpassword,name="resetpassword"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('searchmedicine/',views.searchmedicine,name="searchmedicine"),
    path("showcarts/", views.showcarts, name="showcarts"),
    path("addtocart/<int:medicineid>/", views.addtocart, name="addtocart"),
    path('removecart/<int:medicineid>/', views.removecart, name='removecart'),
    path("update-qty/<int:qv>/<int:medicineid>/", views.updateqty, name="updateqty"),
    path("add-address/", views.addaddress, name="addaddress"),
    path("show-address/", views.showaddress, name="showaddress"),

]
