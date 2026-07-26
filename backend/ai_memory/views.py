from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .memory_service import MemoryService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def memory_list_view(request):
    """List AI memories, optionally filtered by type."""
    memory_type = request.GET.get('type')
    limit = int(request.GET.get('limit', 50))
    memories = MemoryService.get_memories(request.user, memory_type, limit)
    for m in memories:
        m['id'] = str(m['id'])
        m['created_at'] = m['created_at'].isoformat()
    return Response({"memories": memories, "count": len(memories)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def memory_context_view(request):
    """Aggregated memory context for Explainable AI."""
    context = MemoryService.get_memory_context(request.user)
    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def improvement_trends_view(request):
    """Natural-language improvement insights from memory data."""
    trends = MemoryService.get_improvement_trends(request.user)
    return Response({"trends": trends})
