from .db import db


class Inventory(db.Model):
    __tablename__= 'inventories'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id", ondelete="CASCADE"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2000), nullable=False)

    #relationships
    item = db.relationship('Item',back_populates='inventory')


    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'quantity': self.quantity,
            'description': self.description
        }