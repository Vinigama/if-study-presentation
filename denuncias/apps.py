from django.apps import AppConfig
import pickle
from django.conf import settings

class DenunciasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'denuncias'

    tagger = pickle.load(open(settings.MEDIA_DATA + 'POS_tagger_brill.pkl', 'rb'))
    model  = pickle.load(open(settings.MEDIA_DATA + 'model.sav', 'rb'))