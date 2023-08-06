class ItemLockedException(Exception):
    def __init__(self, message, item_name):
        self._item_name = item_name
        super().__init__(message)

    @property
    def item_name(self):
        return self._item_name
