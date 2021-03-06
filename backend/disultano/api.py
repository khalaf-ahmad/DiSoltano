from flask_restful import Api
from disultano.resources.user import (
  Registration, Users, UserLogin, TokenRefresh
)
from disultano.resources.category import Category, CategoryList
from disultano.resources.product import Product, ProductList
from disultano.resources.order import Order, OrderList, OrderDetail, PrintOrder

# create api variable to make restful api's and endpoints
api = Api()

# adding resources

# user resources
api.add_resource(Registration, '/user')
api.add_resource(Users, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/token/refresh')

#category resources
api.add_resource(Category, '/category')
api.add_resource(CategoryList, '/categories')

#product resources
api.add_resource(Product, '/product')
api.add_resource(ProductList, '/products')

#order resources
api.add_resource(Order, '/order')
api.add_resource(OrderList, '/orders')
api.add_resource(PrintOrder, '/print_order')

#order detail resources
api.add_resource(OrderDetail, '/order_detail')