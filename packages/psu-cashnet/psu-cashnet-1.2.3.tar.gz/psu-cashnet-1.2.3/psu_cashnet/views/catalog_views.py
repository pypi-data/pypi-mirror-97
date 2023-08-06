from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.conf import settings
from psu_base.classes.ConvenientDate import ConvenientDate
from psu_base.classes.Log import Log
from psu_base.services import utility_service, error_service, auth_service, message_service
from psu_base.decorators import require_authority
from psu_cashnet.models.catalog import CatalogItem
from decimal import Decimal

log = Log()


@require_authority(['cashnet', 'oit-es-manager'])
def cn_catalog_index(request):
    """
    Browse the item catalog
    """
    log.trace()

    items = CatalogItem.objects.all()

    return render(
        request, 'catalog/cn_catalog_index.html',
        {'items': items}
    )


@require_authority(['cashnet', 'oit-es-manager'])
def cn_catalog_edit(request, item_id):
    """
    Edit an item
    """
    log.trace()

    if int(item_id) == 0:
        item = {'id': 0}
    else:
        item = get_object_or_404(CatalogItem, pk=item_id)

    return render(
        request, 'catalog/cn_catalog_edit.html',
        {'item': item}
    )


@require_authority(['cashnet', 'oit-es-manager'])
def cn_catalog_save(request, item_id):
    """
    Save changes to an item
    """
    log.trace()

    if int(item_id) == 0:
        item = CatalogItem()
        item.app_code = utility_service.get_app_code()
    else:
        item = get_object_or_404(CatalogItem, pk=item_id)

    # Only developers can update the item_code (referenced in Django code)
    if auth_service.has_authority(['developer', '~SuperUser']):
        item.item_code = request.POST.get('item_code')
    # Also allow for new items
    elif int(item_id) == 0:
        item.item_code = request.POST.get('item_code')
    # If it was changed, but cannot be saved, post a warning
    elif item.item_code != request.POST.get('item_code'):
        message_service.post_warning("Only developers can change the 'item code' referenced in the Django project")

    # Plain-text values
    item.cashnet_code = request.POST.get('cashnet_code')
    item.description = request.POST.get('description')
    item.gl = request.POST.get('gl')

    # Amounts and dates
    error_flag = False
    try:
        amount = request.POST.get('amount')
        sale_amount = request.POST.get('sale_amount')
        sale_start = request.POST.get('sale_start_date')
        sale_end = request.POST.get('sale_end_date')

        decimal_amount = Decimal(amount) if amount else item.amount
        decimal_sale_amount = Decimal(sale_amount) if sale_amount else None

        if sale_start or sale_end:
            sale_start_date = ConvenientDate(sale_start).datetime_instance
            sale_end_date = ConvenientDate(sale_end).datetime_instance
            item.sale_start_date = sale_start_date
            item.sale_end_date = sale_end_date

        item.amount = decimal_amount
        item.sale_amount = decimal_sale_amount

    except Exception as ee:
        error_flag = True
        error_service.unexpected_error(
            "Unable to save dollar amounts or sale dates. Please verify your input values.",
            ee
        )
    # Save changes
    # This is below the exception so that plain-text changes will save even if sale/amounts failed
    item.save()

    if error_flag:
        return redirect('cashnet:catalog_edit', item.id)
    else:
        message_service.post_success(f"""Item #{item.id}: "{item.description}" has been saved""")
        return redirect('cashnet:catalog_index')
