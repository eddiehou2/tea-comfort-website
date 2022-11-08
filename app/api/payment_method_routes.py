
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import PaymentMethod
from app.forms import AddPaymentMethod


payment_method_routes = Blueprint('payment_methods', __name__)

def augment_result(payment_method):
    augmented_payment_method = payment_method.to_dict()

    # Add additional information that you'd like to pass
    # augmented_payment_method["additional_info"] = payment_method.additional_info
    return augmented_payment_method

@payment_method_routes.route('', methods=["GET"])
@login_required
def get_payment_methods():
    """
    Get all payment methods of current user
    """
    user_id = current_user.id
    payment_methods = PaymentMethod.query.filter_by(user_id=user_id).all()
    return {'payment_methods': [augment_result(payment_method) for payment_method in payment_methods]}

@payment_method_routes.route('', methods=["POST"])
@login_required
def add_payment_method():
    """
    Add a payment method for current user
    """
    user_id = current_user.id
    form = AddPaymentMethod()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        payment_method = PaymentMethod()
        form.populate_obj(payment_method)
        payment_method.user_id = user_id
        db.session.add(payment_method)
        db.session.commit()
        return {'payment_method': augment_result(payment_method)}
    else:
        return {'errors': form.errors}, 400

@payment_method_routes.route('/<payment_method_id>', methods=["PUT"])
@login_required
def update_payment_method(payment_method_id):
    """
    Update a payment method for current user w/ payment_method_id
    """
    user_id = current_user.id
    form = AddPaymentMethod()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():

        payment_method = PaymentMethod.query.get(payment_method_id)
        if not payment_method:
            return {'errors': 'Payment Method does not exist.'}, 400
        elif payment_method.user_id != user_id:
            return {'errors': 'Payment Method does not belong to current user.'}, 400
        form.populate_obj(payment_method)
        db.session.commit()
        return {'payment_method': augment_result(payment_method)}
    else:
        return {'errors': form.errors}, 400

@payment_method_routes.route('/<payment_method_id>', methods=["DELETE"])
@login_required
def delete_payment_method(payment_method_id):
    """
    Delete a payment method for current user w/ payment_method_id
    """
    user_id = current_user.id
    payment_method = PaymentMethod.query.get(payment_method_id)
    if payment_method:
        if payment_method.user_id != user_id:
            return {'errors': 'Review does not belong to current user.'}, 400
        db.session.delete(payment_method)
        db.session.commit()
        return {"message": "Deleted successfuly"}
    else:
        return {'errors': form.errors}, 400