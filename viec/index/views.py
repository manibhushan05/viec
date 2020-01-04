from rest_framework import viewsets, status, permissions
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response


class IndexViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer)

    def get(self, request, *args, **kwargs):
        return Response(data={}, status=status.HTTP_200_OK, template_name='leads/register-lead.html')
