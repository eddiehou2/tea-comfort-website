from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import User, db, Item,Inventory
from app.forms import ChangeInventory



inventory_routes = Blueprint('inventory', __name__)


def augment_result(inventory):
    augmented_inventory = inventory.to_dict()

    # Add additional information that you'd like to pass
    # augmented_inventory["additional_info"] = inventory.additional_info
    augmented_inventory["image_url"] = inventory.item.image_url
    augmented_inventory["name"] = inventory.item.name
    augmented_inventory["price"] = inventory.item.price

    return augmented_inventory

@inventory_routes.route('/<inventory_id>', methods=["GET"])
@login_required
def get_inventory_by_id(inventory_id):
    """
    Get inventory from inventory ID
    """
    # user_id = current_user.id
    inventory = Inventory.query.get(inventory_id)

    if not inventory:
        return {'error': 'Inventory does not exist.'}, 400
    else:
        return {'inventory': augment_result(inventory)}

@inventory_routes.route('/item/<item_id>', methods=["GET"])
@login_required
def get_inventory(item_id):
    """
    Get inventory for item with item_id
    """
    user_id = current_user.id
    inventory = Inventory.query.filter_by(item_id=item_id).first()
    # frontend used fields: name (of item), image_url, quantity, price,
    # additional fields: item_id, customized_item_id, id

    if not inventory:
        return {'error': 'Inventory does not exist.'}, 400
    else:
        return {'inventory': augment_result(inventory)}

@inventory_routes.route('/item/<item_id>', methods=["POST"])
@login_required
def change_inventory(item_id):
    """
    Change inventory for item
    """
    user_id = current_user.id

    form = ChangeInventory()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        inventory = Inventory.query.filter_by(item_id=item_id).first()

        if not inventory:
            return {'error': 'Inventory does not exist.'}, 400
        else:
            inventory.quantity += form.data['change_in_quantity']
        db.session.commit()
        return {'inventory': augment_result(inventory)}
    else:
        return {'errors': form.errors}, 400

@inventory_routes.route('/<inventory_id>', methods=["PUT"])
@login_required
def edit_inventory(inventory_id):
    """
    Update inventory by ID
    """
    user_id = current_user.id
    form = ChangeInventory()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        inventory = Inventory.query.get(inventory_id)
        if not inventory:
            return {'errors': 'Inventory does not exist.'}, 400
        else:
            inventory.quantity = form.data['absolute_quantity']
            db.session.commit()

            return {'inventory': augment_result(inventory)}
    else:
        return {'errors': form.errors}, 400