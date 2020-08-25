from flask_restful import Resource, inputs, request, current_app
from backend.disoltano.utility import (
    create_request_parser,
    UserLevel,
    save_picture,
    delete_product_img
)
from backend.disoltano.models.product import ProductModel
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims
)
import os


_name_arg = {"name": "name", "type": str, "location": "form"}
_id_arg = {"name": "id", "type": int, "location": "form"}
_category_id_arg = {"name": "category_id", "type": int, "location": "form"}
_price_arg = {"name": "price", "type": float, "location": "form"}
_details_param = {"name": "details", "type": inputs.boolean, "location": "args"}

class Product(Resource):

    @jwt_required
    def get(self):
        data = create_request_parser([_name_arg, _details_param]).parse_args()
        product = ProductModel.find_by_name(data['name'])
        if not product:
            return {'message': 'product not found!'}, 404
        if not data['details']:
            return {
                "product": product.json()
            }
        return {
                "product": product.details_json()
            }

    @jwt_required
    def post(self):
        user_level = get_jwt_claims()['user_level']
        if user_level == UserLevel.GUEST:
            return {
                "message": "you don't have access rights to the content.",
                "error": "request_forbidden"
            }, 403
        data = create_request_parser([_name_arg,
            _price_arg, _category_id_arg])\
        .parse_args()
        image = request.files.get("image", None)
        product = ProductModel(data['name'],
            data['price'], data['category_id'], "")
        try:
            if image:
                file_name = save_picture(image)
                product.image_file = file_name
            product.save_to_db()
        except Exception as ex:
            return {"message": "internal server error!"}, 500
        
        return {
            "product": product.json()
        }, 201


    @jwt_required
    def put(self):
        user_level = get_jwt_claims()['user_level']
        if user_level == UserLevel.GUEST:
            return {
                "message": "you don't have access rights to the content.",
                "error": "request_forbidden"
            }, 403
        data = create_request_parser([_name_arg, _price_arg,
            _category_id_arg, _id_arg]).parse_args()
        product = ProductModel.find_by_id(data['id'])
        image = request.files.get("image", None)
        try:
            if product:
                product.name = data['name']
                product.price = data['price']
                product.category_id = data['category_id']
                if image:
                    delete_product_img(product.image_file)
            else:
                product = ProductModel(**data)
            if image:
                    file_name = save_picture(image)
                    product.image_file = file_name
            product.save_to_db()
        except Exception as ex:
            return {"message": "internal server error!"}, 500
        
        return {
            "product": product.json()
        }, 201

    @jwt_required
    def delete(self):
        user_level = get_jwt_claims()['user_level']
        if user_level == UserLevel.GUEST:
            return {
                "message": "you don't have access rights to the content.",
                "error": "request_forbidden"
            }, 403
        data = create_request_parser([{**_id_arg,
            "location": "json"}]).parse_args()
        product = ProductModel.find_by_id(data['id'])
        if not product:
            return {
                "message": "product not found."
            }, 404
        try:
            delete_product_img(product.image_file)
            product.delete_from_db()
        except Exception as ex:
            return {"message": "internal server error!"}, 500
        
        return {
            "message": "product deleted successfully"
        }




class ProductList(Resource):

    @jwt_required
    def get(self):
        details = create_request_parser([_details_param])\
        .parse_args().get('details')
        result = {"products": []}
        if details:
            result['products'] = [product.details_json()
            for product in ProductModel.get_all()]
        else:
            result['products'] = [product.json()
            for product in ProductModel.get_all()]
        return result
