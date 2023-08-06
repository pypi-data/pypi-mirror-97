from cryptomodel.operations import OPERATIONS

MEMORY_HANDLED_ATTRIBUTE_NAME = "memory_handled"


class Repository:

    def __init__(self):
        self.memories = {}

    def commit(self):
        for key, mem in self.memories.items():

            self.remove_handled_items(mem.items)
            for item in mem.items:
                if not getattr(item, MEMORY_HANDLED_ATTRIBUTE_NAME):
                    if item.operation == OPERATIONS.ADDED.name:
                        trans = mem.on_add(item)
                        if trans is not None:
                            item.id = trans.id
                            setattr(item, MEMORY_HANDLED_ATTRIBUTE_NAME, True)
                    elif item.operation == OPERATIONS.MODIFIED.name:
                        trans = mem.on_edit(item)
                        if trans is not None:
                            item.id = trans.id
                            setattr(item, MEMORY_HANDLED_ATTRIBUTE_NAME, True)
                    elif item.operation == OPERATIONS.REMOVED.name:
                        mem.on_remove(item, False)
                        setattr(item,MEMORY_HANDLED_ATTRIBUTE_NAME, True)


    def remove_handled_items(self, source_list):
       for item in list(source_list):
           if not hasattr(item, MEMORY_HANDLED_ATTRIBUTE_NAME):
               setattr(item, MEMORY_HANDLED_ATTRIBUTE_NAME, False)
           if getattr(item, MEMORY_HANDLED_ATTRIBUTE_NAME):
                source_list.remove(item)

    """
    Assumes item has two attributes named as follows  
    operation  values : ADDED, REMOVED , MODIFIED 
    """

    def mark_deleted(self, memory_key, on_select, id_value, id_name):
        item = next((x for x in self.memories[memory_key].items if getattr(x, id_name) == id_value), None)
        if item is None:
            try:
                if len(on_select(id_value)) == 0:
                    return
                trans = on_select(id_value)[:1]
            except:
                trans = None  # log ?
            if trans is None:
                return
            else:
                trans.operation = OPERATIONS.REMOVED.name
                self.memories[memory_key].items.append(trans)
        else:
            item.operation = OPERATIONS.REMOVED.name
            setattr(item, MEMORY_HANDLED_ATTRIBUTE_NAME,
                    False)  # add, commit, remove sequence should set back to handled = false to allow deletion

