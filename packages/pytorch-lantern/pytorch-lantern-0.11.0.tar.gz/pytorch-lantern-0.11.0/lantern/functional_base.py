from pydantic import BaseModel, Extra


class FunctionalBase(BaseModel):
    class Config:
        allow_mutation = False
        extra = Extra.forbid

    def map(self, fn, *args, **kwargs):
        return fn(self, *args, **kwargs)

    def replace(self, **kwargs):
        new_dict = self.dict()
        new_dict.update(**kwargs)
        return type(self)(**new_dict)

    @classmethod
    def setattr(cls, name, value):
        if hasattr(cls, name):
            raise ValueError(f"Attribute {name} already exists")
        setattr(cls, name, value)
        return value

    @classmethod
    def method(cls, fn):
        return cls.setattr(fn.__name__, fn)

    @classmethod
    def property(cls, fn):
        return cls.setattr(fn.__name__, property(fn))

    @classmethod
    def staticmethod(cls, fn):
        return cls.setattr(fn.__name__, staticmethod(fn))

    @classmethod
    def classmethod(cls, fn):
        return cls.setattr(fn.__name__, classmethod(fn))
