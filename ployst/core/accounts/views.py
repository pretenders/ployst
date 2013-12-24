from rest_framework.viewsets import ModelViewSet

from .models import Team

class TeamViewSet(ModelViewSet):
    model = Team
