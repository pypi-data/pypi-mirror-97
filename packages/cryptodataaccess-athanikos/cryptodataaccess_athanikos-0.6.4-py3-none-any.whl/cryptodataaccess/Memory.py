"""
Represents an item list contained within Repository
keeps the set of methods executed for add/edit/delete
"""
TRANSACTIONS_MEMORY_KEY = "transactions"
USER_NOTIFICATIONS_MEMORY_KEY = "notifications"
USER_CHANNELS_MEMORY_KEY = "channels"
USER_SETTINGS_MEMORY_KEY = "settings"
CALCULATOR_MEMORY_KEY = "calculator"
NOTIFICATIONS_MEMORY_KEY = "notifications"


class Memory:

    def __init__(self, on_add, on_edit, on_remove, items):
        self.on_add = on_add
        self.on_remove = on_remove
        self.on_edit = on_edit
        self.items = items
        self.handled_items = []
