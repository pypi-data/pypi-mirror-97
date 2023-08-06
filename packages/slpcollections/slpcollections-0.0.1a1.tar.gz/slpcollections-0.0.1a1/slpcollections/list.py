class List(list):
    """ A list that supports attribute  
    """
    def __init__(self):
        self.__dict__.update({"first": None, "second": None, "last": None})

    def append(self, item):
        super(List, self).append(item)

        if len(self) == 1:
            setattr(self, 'first', item)

        elif len(self) == 2:
            setattr(self, 'second', item)

        setattr(self, 'last', item)

    def pop(self):
        item = super().pop()
        if len(self) == 1:
            setattr(self, 'second', None)

        if len(self) == 0:
            setattr(self, 'first', None)
            setattr(self, 'last', None)
        else:
            setattr(self, 'last', self[-1])

        return item
