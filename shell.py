import os
import django
from apps.product.models import ProductCharacteristic, CharacteristicImage
from django.core.management import call_command


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


# Ensure that you have a valid product_characteristic_id
product_characteristic_id = 16

try:
    # Try to convert the ID to an integer and find the object
    characteristic = ProductCharacteristic.objects.get(id=int(product_characteristic_id))
except ProductCharacteristic.DoesNotExist:
    # Handle the case where the object with the given ID doesn't exist
    print(f"ProductCharacteristic with ID {product_characteristic_id} does not exist.")
else:
    # Get all images for the found ProductCharacteristic
    images = characteristic.images.all()

    # Print the URL of each image
    for image in images:
        print(image.image.url)
