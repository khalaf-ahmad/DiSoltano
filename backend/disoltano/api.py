from flask_restful import Api
from backend.disoltano.resources.user import (
        Registration, Users, UserLogin, TokenRefresh
    )
from backend.disoltano.resources.category import Category, CategoryList
from backend.disoltano.resources.product import Product, ProductList

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