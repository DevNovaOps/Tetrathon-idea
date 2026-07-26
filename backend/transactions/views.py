from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Transaction
from .import_service import TransactionImportService
from .analytics_service import TransactionAnalyticsService


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transaction_list_view(request):
    """
    GET  — List transactions with optional filters (?category=food&is_income=false&limit=50).
    POST — Create a single transaction.
    """
    if request.method == 'POST':
        tx = TransactionImportService.create_transaction(request.user, request.data)
        return Response({
            "id": str(tx.id),
            "amount": float(tx.amount),
            "merchant": tx.merchant,
            "category": tx.category,
            "date": tx.date.isoformat(),
            "is_income": tx.is_income,
            "payment_method": tx.payment_method,
        }, status=201)

    # GET with filters
    qs = Transaction.objects.filter(user=request.user, is_deleted=False)

    category = request.GET.get('category')
    if category:
        qs = qs.filter(category=category)

    is_income = request.GET.get('is_income')
    if is_income is not None:
        qs = qs.filter(is_income=is_income.lower() == 'true')

    payment_method = request.GET.get('payment_method')
    if payment_method:
        qs = qs.filter(payment_method=payment_method)

    limit = int(request.GET.get('limit', 100))
    qs = qs[:limit]

    data = [{
        "id": str(tx.id),
        "amount": float(tx.amount),
        "merchant": tx.merchant,
        "category": tx.category,
        "date": tx.date.isoformat(),
        "is_income": tx.is_income,
        "payment_method": tx.payment_method,
        "location": tx.location,
        "description": tx.description,
        "source": tx.source,
    } for tx in qs]

    return Response({"transactions": data, "count": len(data)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_csv_view(request):
    """Import transactions from uploaded CSV file."""
    file = request.FILES.get('file')
    if not file:
        csv_text = request.data.get('csv_data', '')
        if not csv_text:
            return Response({"error": "No file or csv_data provided"}, status=400)
    else:
        csv_text = file.read().decode('utf-8')

    result = TransactionImportService.import_csv(request.user, csv_text)
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def demo_data_view(request):
    """Generate synthetic demo transaction data."""
    months = int(request.data.get('months', 6))
    result = TransactionImportService.generate_demo_data(request.user, months)
    return Response(result)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def correct_category_view(request, tx_id):
    """Manually correct a transaction's category."""
    new_category = request.data.get('category')
    if not new_category:
        return Response({"error": "category is required"}, status=400)
    tx = TransactionImportService.correct_category(request.user, tx_id, new_category)
    if not tx:
        return Response({"error": "Transaction not found"}, status=404)
    return Response({
        "id": str(tx.id),
        "category": tx.category,
        "original_category": tx.original_category,
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction_view(request, tx_id):
    """Soft-delete a transaction."""
    ok = TransactionImportService.delete_transaction(request.user, tx_id)
    if not ok:
        return Response({"error": "Transaction not found"}, status=404)
    return Response({"status": "deleted"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_view(request):
    """Full transaction analytics: spending summary, trends, patterns."""
    data = TransactionAnalyticsService.get_full_analytics(request.user)
    return Response(data)
