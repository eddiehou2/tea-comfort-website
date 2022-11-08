from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Review
from app.forms import AddReview


review_routes = Blueprint('review', __name__)

def augment_result(review):
    augmented_review = order.to_dict()

    # Add additional information that you'd like to pass
    # augmented_review["additional_info"] = review.additional_info
    return augmented_review

@review_routes.route('/user', methods=["GET"])
@login_required
def get_user_reviews():
    """
    Get all reviews of current user
    """
    user_id = current_user.id
    reviews = Review.query.filter_by(user_id=user_id).all()
    return {'reviews': [augment_result(review) for review in reviews]}

@review_routes.route('/item/<item_id>', methods=["GET"])
def get_item_reviews(item_id):
    """
    Get all reviews of selected item
    """
    reviews = Review.query.filter_by(item_id=item_id).all()
    return {'reviews': [augment_result(review) for review in reviews]}

@review_routes.route('/item/<item_id>', methods=["POST"])
@login_required
def add_review(item_id):
    """
    Add a review for current user base on item_id
    """
    user_id = current_user.id
    form = AddReview()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        review = Review()
        review.user_id = current_user.id
        form.populate_obj(review)
        review.item_id = item_id
        review.user_id = user_id
        db.session.add(review)
        db.session.commit()
        return {'review': augment_result(review)}
    else:
        return {'errors': form.errors}, 400

@review_routes.route('/<review_id>', methods=["PUT"])
@login_required
def update_review(review_id):
    """
    Update a review for current user w/ review_id
    """
    user_id = current_user.id
    form = AddReview()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():

        review = Review.query.get(review_id)
        if not review:
            return {'errors': 'Review does not exist.'}, 400
        elif review.user_id != user_id:
            return {'errors': 'Review does not belong to current user.'}, 400
        form.populate_obj(review)
        db.session.commit()
        return {'review': augment_result(review)}
    else:
        return {'errors': form.errors}, 400

@review_routes.route('/<review_id>', methods=["DELETE"])
@login_required
def delete_review(review_id):
    """
    Delete a review for current user w/ review_id
    """
    user_id = current_user.id
    review = Review.query.get(review_id)
    if review:
        if review.user_id != user_id:
            return {'errors': 'Review does not belong to current user.'}, 400
        db.session.delete(review)
        db.session.commit()
        return {"message": "Deleted successfuly"}
    else:
        return {'errors': form.errors}, 400