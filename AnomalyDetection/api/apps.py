from django.apps import AppConfig
import pickle


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    # Init Model
    model = pickle.load(open('models/iso_forrest.model', 'rb'))