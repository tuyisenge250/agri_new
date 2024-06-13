from models import storage
from models.base_models import Base_model
from models.news_letter import News
import base64

print("-- Create a new Product --")
my_product = News()
my_product.title = 'hi'
my_product.content = 'hello'
my_product.image = 'ffhfhf'
my_product.status = 'ffjfjjfjf'
my_product.save()
