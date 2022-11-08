
from flask import Blueprint, jsonify, request
from app.models import User, db, Item
from flask_login import login_required, current_user



item_routes = Blueprint('items', __name__)

def augment_result(item):
    augmented_item = item.to_dict()

    # Add additional information that you'd like to pass
    # augmented_item["additional_info"] = item.additional_info
    return augmented_item
    


@item_routes.route('', methods=["GET"])
def get_items():
    """
    Get all items
    """
    items = Item.query.all()
    return {'items': [augment_result(item) for item in items]}


@item_routes.route('/category/<category>', methods=["GET"])
def get_items_by_category(category):
    """
    Get all items by drink category
    """
    items = Item.query.filter_by(category=category).all()
    return {'items': [augment_result(item) for item in items]}

@item_routes.route('/<int:item_id>', methods=["GET"])
def get_item_by_id(item_id):
    """
    Get item by id
    """
    item = Item.query.get(item_id)
    return {'item': augment_result(item)}