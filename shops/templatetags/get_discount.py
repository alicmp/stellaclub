from shops.models import Shop, Discount
from django.utils import timezone
from django.template.defaulttags import register

@register.simple_tag
def get_discount(shop):
  try:
    return Discount.objects.get(
      shop=shop,
      is_expire=False,
			expiration_date__gte=timezone.now(),
    ).percentage
  except Discount.DoesNotExist:
    return None