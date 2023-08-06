from django.urls import path
from . import views

urlpatterns = [
    path('error', views.cn_error_page, name='error'),

    # Cashnet Response Handlers
    path('response', views.cn_record_response, name='response'),
    path('tx/validation/<int:tx_id>', views.cn_validate_response, name='validation'),

    # Allow admin to update tx status after an error
    path('tx/update/<int:tx_id>/<status>', views.cn_admin_update_tx, name='admin_update'),

    # Catalog Views
    path('catalog', views.cn_catalog_index, name='catalog_index'),
    path('catalog/edit/<int:item_id>', views.cn_catalog_edit, name='catalog_edit'),
    path('catalog/save/<int:item_id>', views.cn_catalog_save, name='catalog_save'),

    # Transaction Views
    path('transaction', views.cn_transaction_index, name='transaction_index'),
    path('transaction/<int:tx_id>', views.cn_transaction_detail, name='transaction_detail'),
    path('transaction/<keyword>', views.cn_transaction_index, name='transaction_errors'),

    # Test Views
    path('test', views.test_transaction_form, name='test_form'),
    path('test/response', views.test_transaction_response, name='test_form_response'),
    path('test/cashnet/<int:tx_id>', views.cn_fake_site, name='fake_cashnet'),
    path('test/success', views.fake_success, name='fake_success'),
    path('test/failure', views.fake_failure, name='fake_failure'),
]
