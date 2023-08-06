import random


class _RandomAttrMeta(type):
    def __getattr__(cls, name):
        scope = vars(cls.Voice if cls.type == 'Voice' else cls.Text)
        if name in scope:
            res = scope[name]
            if type(res) == str:
                return res
            elif type(res) in [tuple, list]:
                return res[random.randint(0, len(res) - 1)]
        elif name in vars(cls.Base):
            res = vars(cls.Base)[name]
            if type(res) == str:
                return res
            elif type(res) in [tuple, list]:
                return res[random.randint(0, len(res) - 1)]
        else:
            raise KeyError("Field {} not found in scopes (Text, Voice and {})".format(
                name, cls
            ))


class Dictionary(metaclass=_RandomAttrMeta):
    @classmethod
    def voice(cls):
        cls.type = 'Voice'
        return cls

    @classmethod
    def text(cls):
        cls.type = 'Text'
        return cls

    class Text: pass
    class Voice: pass
    class Base: pass
