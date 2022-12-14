from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import User, db, Order,OrderItem
from app.forms import AddOrderItem



order_item_routes = Blueprint('order_item', __name__)


def augment_result(order_item):
    augmented_order_item = order_item.to_dict()

    # Add additional information that you'd like to pass
    # augmented_order_item["additional_info"] = order_item.additional_info
    augmented_order_item["image_url"] = order_item.item.image_url
    augmented_order_item["name"] = order_item.item.name
    augmented_order_item["price"] = order_item.item.price

    return augmented_order_item

@order_item_routes.route('/<order_item_id>', methods=["GET"])
@login_required
def get_order_items_by_id(order_item_id):
    """
    Get order item from order item ID
    """
    # user_id = current_user.id
    order_item = OrderItem.query.get(order_item_id)

    if not order_item:
        return {'error': 'Order item does not exist.'}, 400
    else:
        return {'order_item': augment_result(order_item)}

@order_item_routes.route('/order/<order_id>', methods=["GET"])
@login_required
def get_order_items(order_id):
    """
    Get all order items from order ID
    """
    user_id = current_user.id
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    # frontend used fields: name (of item), image_url, quantity, price,
    # additional fields: item_id, customized_item_id, id

    if not order_items:
        return {'order_items': []}
    else:
        return {'order_items': [augment_result(order_item) for order_item in order_items]}

@order_item_routes.route('/order/<order_id>', methods=["POST"])
@login_required
def add_order_item(order_id):
    """
    Add order item to order
    """
    user_id = current_user.id

    form = AddOrderItem()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        order_item = None
        if not form.data['item_id'] and not form.data['customized_item_id']:
            return {'errors': 'Item not specified.'}, 400
        elif form.data['item_id'] and form.data['customized_item_id']:
            return {'errors': 'Both item ID and customized item ID specified. Should only have one.'}, 400

        if form.data['item_id']:
            order_item = OrderItem.query.filter_by(order_id=order_id, item_id=form.data['item_id']).first()
        elif form.data['customized_item_id']:
            order_item = OrderItem.query.filter_by(order_id=order_id, customized_item_id=form.data['customized_item_id']).first()

        if not order_item:
            order_item = OrderItem()
            form.populate_obj(order_item)
            order_item.order_id = order_id
            db.session.add(order_item)
        else:
            order_item.quantity += form.data['quantity']
        db.session.commit()
        return {'order_item': augment_result(order_item)}
    else:
        return {'errors': form.errors}, 400

@order_item_routes.route('/<order_item_id>', methods=["DELETE"])
@login_required
def delete_order_item(order_item_id):
    """
    Delete order item by ID
    """
    user_id = current_user.id
    order_item = OrderItem.query.get(order_item_id)
    if not order_item:
        return {'errors': 'Order item does not exist.'}, 400
    else:
        db.session.delete(order_item)
        db.session.commit()
        return {"message": "Deleted successfuly"}

@order_item_routes.route('/<order_item_id>', methods=["PUT"])
@login_required
def edit_order_item(order_item_id):
    """
    Update order item by ID
    """
    user_id = current_user.id
    form = AddOrderItem()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        order_item = OrderItem.query.get(order_item_id)
        if not order_item:
            return {'errors': 'Order item does not exist.'}, 400
        else:
            if form.data['quantity'] > 0:
                order_item.quantity = form.data['quantity']
                db.session.commit()

                return {'order_item': augment_result(order_item)}
            else:
                db.session.delete(order_item)
                db.session.commit()
                return {"message": "Deleted successfuly"}
    else:
        return {'errors': form.errors}, 400