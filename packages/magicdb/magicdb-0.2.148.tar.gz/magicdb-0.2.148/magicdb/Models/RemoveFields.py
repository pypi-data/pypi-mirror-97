from magicdb.Models.MagicModel import QueryAndBaseMetaClasses


class RemoveFieldsMeta(QueryAndBaseMetaClasses, type):
    @staticmethod
    def remove_fields(cls):
        if "fields_to_remove" not in cls.__fields__:
            return
        for field in cls.__fields__["fields_to_remove"].default:
            if field in cls.__fields__:
                del cls.__fields__[field]
        del cls.__fields__["fields_to_remove"]

    def __new__(mcs, *args, **kwargs):
        x = super().__new__(mcs, *args, **kwargs)
        mcs.remove_fields(x)
        return x
