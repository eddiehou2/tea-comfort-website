from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import User, db, Order

order_routes = Blueprint('order', __name__)

def augment_result(order):
    augmented_order = order.to_dict()

    # Add additional information that you'd like to pass
    # augmented_order["additional_info"] = order.additional_info
    return augmented_order

@order_routes.route('/all', methods=["GET"])
@login_required
def get_all_orders():
    """
    Get all orders owned by this user
    """

    user_id = current_user.id
    orders = Order.query.filter_by(user_id=user_id).all()

    return {'orders': [augment_result(order) for order in orders]}

@order_routes.route('', methods=["GET","POST"])
@login_required
def get_current_order():
    """
    Get existing order for current user or create new order
    """
    user_id = current_user.id
    order = Order.query.filter_by(user_id=user_id, status='not placed').first()

    if not order:
        order = Order()
        order.user_id = user_id
        order.status = 'not placed'
        db.session.add(order)
        db.session.commit()
        return {'order': augment_result(order)}
    else:
        return {'order': augment_result(order)}

@order_routes.route('/<order_id>', methods=["POST"])
@login_required
def submit_order(order_id):
    """
    Submit order by order ID - change status to "placed"
    """
    user_id = current_user.id
    order = Order.query.get(order_id)

    if not order or order.user_id != user_id:
        return {'error': 'Cannot submit order.'}, 400
    elif order.status != 'not placed':
        return {'error': 'Order has already been submitted.'}, 400
    else:
        order.status = 'placed'
        db.session.commit()
        return {'order': augment_result(order)}

@order_routes.route('/<order_id>', methods=["DELETE"])
@login_required
def delete_order(order_id):
    """
    Delete order by order ID
    """
    user_id = current_user.id
    order = Order.query.get(order_id)

    if not order or order.user_id != user_id:
        return {'error': 'Cannot delete order.'}, 400
    else:
        db.session.delete(order)
        db.session.commit()
        return {"message": "Deleted successfuly"}