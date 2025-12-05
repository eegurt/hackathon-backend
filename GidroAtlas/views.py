from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework.decorators import api_view
from rest_framework.response import Response


@extend_schema(responses={200: OpenApiTypes.OBJECT})
@api_view(["GET"])
def health_check(request):
    """Simple endpoint to verify the service is online."""
    return Response(
        {
            "status": "ok",
            "service": "GidroAtlas",
        }
    )
