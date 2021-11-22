
from django.contrib import admin
from django.urls import path, include
from Argupedia import views as arg_views
from django.contrib.auth import views as a_views
from django.conf import settings
from django.conf.urls.static import static
# https://docs.djangoproject.com/en/3.2/topics/auth/default/
#https://docs.djangoproject.com/en/2.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development
urlpatterns = [
    # path to admin page
    path('admin/', admin.site.urls),
# path to signup page
    path('signup/',arg_views.signup, name='register'),
# path to login page
    path('signin/',a_views.LoginView.as_view(template_name='Argupedia/signin.html'), name='signin'),
# path to signout page
    path('signout/', a_views.LogoutView.as_view(template_name='Argupedia/signout.html'), name='signout'),
# path to profile page
    path('ArgupediaProfile/',arg_views.Argprofile, name='profile'),
    path('', include('Argupedia.urls')),
# path to reset password
    path('reset/', a_views.PasswordResetView.as_view(template_name='Argupedia/reset.html'), name='password_reset'),

# path to reset confirm
    path('resetconfirm/',a_views.PasswordResetDoneView.as_view(template_name='Argupedia/password_reset_confirmed.html'),name='password_reset_done'),
# path to reset password
    path('password-reset-confirm/<uidb64>/<token>/',
         a_views.PasswordResetConfirmView.as_view(
             template_name='Argupedia/resetbackend.html'),name='password_reset_confirm'),
# path to reset finalise the password
    path('resetFinalise/', a_views.PasswordResetCompleteView.as_view(template_name='Argupedia/resetFinalise.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#The user is then presented with a wide range of argument schemes to choose from allowing them to argue from a variety of positions
#next to each scheme is a modal and within each modal it details when to use each scheme, the fields each scheme contains and an example argument constructed with the scheme

#When the user clicks on an argument scheme name they are taken to a page in which the web application retrives the argument field names and presents them to the user
# which an example argument is displayed within each field