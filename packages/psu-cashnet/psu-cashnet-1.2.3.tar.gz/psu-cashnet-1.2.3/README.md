# WDT Django Cashnet Plugin

This plugin integrates a PSU Django app with Cashnet's checkout interface

## Setup
*This plugin requires the [psu-base plugin](https://github.com/PSU-OIT-ARC/django-psu-base) to be installed*  

* Add to project requirements: 
```
psu-base>=1.1.9
psu-cashnet>=1.0.1
```
* Add to installed apps
```
INSTALLED_APPS = [
    ...
    'django_cas_ng',
    'crequest',
    'sass_processor',
    'psu_base',
    'psu_cashnet',
]
```
* Configure URLs
```
path('cashnet/', include(('psu_cashnet.urls', 'psu_cashnet'), namespace='cashnet')),
```
* Install requirements and run migrations
```
$ pip install -r requirements.txt
$ python manage.py migrate
```
* Add required and optional settings in settings.py
```
# Merchant code is required, and must be configured on Cashnet Admin interface
# If your app has multiple merchant codes, provide the correct one during transaction creation
CASHNET_MERCHANT_CODE = 'pdxtestmerchant'

# During development, you can use a simulated Cashnet site to complete transactions 
# without a credit card. *** Do this in local_settings.py ***
CASHNET_SIMULATE_TRANSACTION = False
```

## How to use

### Security Roles
Access to edit items, view transactions, and use the nonprod test form are all granted via the "cashnet" role.
Users with oit-es-manager will get the same access, and in non-production, developers get full access to everything.

### Defining Catalog Items
Follow the "Cashnet Items" link in the admin menu. 
Links to create a new item exist at the top and bottom of the page.
Existing items can be edited by clicking the pencil-square icon or the ID number link.   
There is currently no way to delete an item. If a future delete function is created, it should not actually delete 
any item that has been purchased in the past, as that would affect previous transaction history displays.

### Viewing Past Transactions
Follow the "Cashnet Transactions" link in the admin menu.
Newest transactions appear first by default, but can be sorted by clicking on column headings.  
**Transaction Statuses:**
* New - customer was never sent to Cashnet
* Initiated - customer was sent to Cashnet, but has not returned back to the app
* Processing - customer was returned to the app, and response data is being validated.  
*If this status lasts more than a fraction of a second, it likely indicates an unhandled exception occurred.*
* Error - There was an error validating the response from Cashnet.  
The transaction may or may not have been successful, and needs to be reviewed in Banner.
* Recorded - Response parameters from Cashnet were recorded, but customer authentication was not verified
* Failure - The customer did not complete payment on Cashnet's site.
* Success - Customer completed payment on Cashnet's site

### Creating a transaction
Use cashnet_service to create a new transaction:
```
    tx = cashnet_service.create_transaction(
        requested_items=requested_items,  # A list of CatalogItem or CatalogItem IDs
                                          # - To indicate quantity, include a tuple (item, quantity) in the list
        success_url=success_url,          # URL or Named URL to redirect successful payment to
        failure_url=failure_url,          # - Can also be a tuple ('named_url', arg) or ('named_url', arg1, arg2, ...)
        merchant_code=merchant_code,      # Merchant code as defined in Cashnet
        reference_class=reference_class,  # If payment is for an object represented by a class/model
        reference_id=reference_id,        # ID of given model (if applicable)
        secret_key=secret_key,            # Not used since Cashnet does not support their "secret key" feature
        term_code=term_code,              # Optional term code associated with transaction
    )
```

### Sending customer to Cashnet site
cashnet_service.cashnet_redirect(tx) will send the customer to the appropriate instance of Cashnet
(production, training, or the "fake cashnet site")
```
def whatever_view(request):

    # tx is the transaction created by cashnet_service
    return cashnet_service.cashnet_redirect(tx)
```

### Handling Cashnet's response
Configure Cashnet to return the customer to `<your app's URL>/cashnet/response`

* Successful transactions will be redirected to the URL defined when the transaction was created
* Unsuccessful transactions will be redirected to the URL defined when the transaction was created
* Transactions that encounter an error while validating will be directed to an error page

### Response validation errors
Any error that occurs during response validation will be logged in the log file, as well as in the AWS 
database, accessible via the Admin menu -> Error Log.  The customer will be directed to a generic error page.
The error page can be overridden by creating a page in your app's directory: `<app>/templates/cn_error.html`
If the Cashnet parameters indicate the payment was successful, and an error occurs, an email will be sent to 
any users with the cashnet role.  The IA team will be included as BCC

### Post-payment processing
Any post-payment processing should be done from the `success_url` defined in the transaction.  

**IMPORTANT**  
Post-payment processing steps (success *and* failure) should should account for the possibility
of an administrator marking a transaction as Success or Failure and kicking off auto-processing.
Processing should be done on the account of the `.customer` property of the transaction record, 
or on the `proxied_user` identity when an admin is proxying.

The status of the post-processing should be set in the transaction record's `post_processing_status` field 
(30-character limit).
```
cashnet_service.set_post_payment_processing_status(tx, "COMPLETE")

# OR, equivalently:

tx.post_processing_status = "COMPLETE"
tx.save()
```