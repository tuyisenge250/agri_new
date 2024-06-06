from models import storage
from models.base_models import Base_model
from models.product import Product
import base64

print("-- Create a new Product --")
my_product = Product()
my_product.name = "apple"
my_product.price = 0.6
my_product.type = "vegetables"

# Read the image file
with open("./web_flask/agri apple.png", "rb") as f:
    image_data = f.read()

# Encode the image data to base64
encoded_image = base64.b64encode(image_data)

# Store the base64 encoded image in the Product object
my_product.image = encoded_image

my_product.save()
print(my_product)
