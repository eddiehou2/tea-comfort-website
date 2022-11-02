from flask.cli import AppGroup
from .users import seed_users, undo_users
from .items import seed_items,undo_items
from .reviews import seed_reviews,undo_reviews
from .orders import seed_orders,undo_orders
from .payment_methods import seed_payment_methods,undo_payment_methods
from .order_items import seed_order_items,undo_order_items
from .inventories import seed_inventories,undo_inventories

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    seed_users()
    seed_items()
    seed_reviews()
    seed_orders()
    seed_payment_methods()
    seed_order_items()
    seed_inventories()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    # Add other undo functions here
