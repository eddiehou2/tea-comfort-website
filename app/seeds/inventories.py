from app.models import db, Inventory



def seed_inventories():
    inventories = []
    NUM_OF_ITEMS = 60

    for i in range(NUM_OF_ITEMS):
        inventories.append(Inventory(item_id = i + 1, quantity = 100, description="original stock inventory on 11/1/22"))

    for inventory in inventories:
        db.session.add(inventory)

    db.session.commit()


# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_inventories():
    db.session.execute('TRUNCATE orders RESTART IDENTITY CASCADE;')
    db.session.commit()