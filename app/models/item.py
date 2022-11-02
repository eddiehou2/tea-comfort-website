from .db import db


class Item(db.Model):
    __tablename__= 'items'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500),nullable=False)

    #relationships
    reviews = db.relationship('Review',back_populates='item')
    order_items = db.relationship('OrderItem',back_populates='item')
    inventory = db.relationship('Inventory',back_populates='item')


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            "category":self.category,
            'image_url':self.image_url,

        }