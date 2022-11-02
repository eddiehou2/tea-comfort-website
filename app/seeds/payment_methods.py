from app.models import db,PaymentMethod



def seed_payment_methods():
    card1 = PaymentMethod(user_id = 1, credit_number='1234567890123456',expiry_date='03/23',security_number='123')
    card2 = PaymentMethod(user_id = 2, credit_number='1234567890123457',expiry_date='03/23',security_number='123')
    card3 = PaymentMethod(user_id = 3, credit_number='1234567890123458',expiry_date='03/23',security_number='123')
    card4 = PaymentMethod(user_id = 4, credit_number='1234567890123459',expiry_date='03/23',security_number='123')
    card5 = PaymentMethod(user_id = 5, credit_number='1234567890123450',expiry_date='03/23',security_number='123')



    db.session.add(card1)
    db.session.add(card2)
    db.session.add(card3)
    db.session.add(card4)
    db.session.add(card5)



    db.session.commit()


# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_payment_methods():
    db.session.execute('TRUNCATE cards RESTART IDENTITY CASCADE;')
    db.session.commit()