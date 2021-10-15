from django.urls import path
from .views import home, user_login, user_logout, machines, parts, delete_machine, download_log, delete_part

urlpatterns = [
    # Define the endpoint for predictions
    path('', home, name = 'home'),
    path('login/', user_login, name = 'login'),
    path('logout/', user_logout, name = 'logout'),
    path('machines/', machines, name = 'machines'),
    path('deletemachine/<id>', delete_machine, name='deletemachine'),
    path('parts/', parts, name = 'parts'),
    path('download/<id>', download_log, name='download'),
    path('deletepart/<id>', delete_part, name='deletepart'),
]