def gen_str(cls):
    def __str__(self):
        class_name = type(self).__name__
        fields_texts = []
        for field in vars(self).items():
            field_name = str(field[0])
            field_value = str(field[1])
            field_text = field_name + '=' + field_value
            fields_texts.append(field_text)
        fields_texts_merged = ', '.join(fields_texts)
        return class_name + '{' + fields_texts_merged + '}'

    cls.__str__ = __str__
    return cls


def gen_repr(cls):
    def __repr__(self):
        return str(self)

    cls.__repr__ = __repr__
    return cls


def gen_str_repr(cls):
    def __str__(self):
        class_name = type(self).__name__
        fields_texts = []
        for field in vars(self).items():
            field_name = str(field[0])
            field_value = str(field[1])
            field_text = field_name + '=' + field_value
            fields_texts.append(field_text)
        fields_texts_merged = ', '.join(fields_texts)
        return class_name + '{' + fields_texts_merged + '}'

    def __repr__(self):
        return str(self)

    cls.__str__ = __str__
    cls.__repr__ = __repr__
    return cls
