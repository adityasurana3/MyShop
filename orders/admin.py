from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.http import HttpResponse

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''
order_payment.short_description = 'Stripe Payment'

def download_csv(modeladmin, request, queryset):
    import csv
    opts = queryset.model._meta
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            data_row.append(value)
        writer.writerow(data_row)
    return response



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display =  ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', order_payment, 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [download_csv]

