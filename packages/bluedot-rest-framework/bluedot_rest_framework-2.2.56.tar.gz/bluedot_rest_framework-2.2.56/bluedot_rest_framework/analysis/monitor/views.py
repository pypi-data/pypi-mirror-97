from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import AnalysisMonitor
from .serializers import AnalysisMonitorSerializer


class AnalysisMonitorView(ModelViewSet):
    model_class = AnalysisMonitor
    serializer_class = AnalysisMonitorSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()
