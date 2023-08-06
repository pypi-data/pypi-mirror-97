from django.db.models import Manager
from dynamicfield_serializer import DynamicFieldSerializer
from rest_framework.serializers import ListSerializer, LIST_SERIALIZER_KWARGS

from .utils import replacer, calculate, get_operations

__all__ = (
    'CalculationDynamicFieldSerializer',
    'GeneratorSerializer',
    'GeneratorListSerializer',
)


class GeneratorListSerializer(ListSerializer):
    def to_representation(self, data, to_list=True):
        iterable = data.iterator() if isinstance(data, Manager) else data
        if to_list:
            return [self.child.to_representation(item) for item in iterable]
        for item in iterable:
            yield self.child.to_representation(item)

    @property
    def data(self):
        return self.to_representation(self.instance, to_list=True)

    @property
    def generator(self):
        return self.to_representation(self.instance, to_list=False)


class GeneratorSerializer(DynamicFieldSerializer):
    """if many=True, have property generator - to return generator serializable values"""

    @classmethod
    def many_init(cls, *args, **kwargs):
        allow_empty = kwargs.pop('allow_empty', None)
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {
            'child': child_serializer,
        }
        if allow_empty is not None:
            list_kwargs['allow_empty'] = allow_empty
        list_kwargs.update(
            {
                key: value
                for key, value in kwargs.items()
                if key in LIST_SERIALIZER_KWARGS
            }
        )
        return GeneratorListSerializer(*args, **list_kwargs)


class CalculationDynamicFieldSerializer(GeneratorSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        calc = self.context.get("calculation")
        if calc:
            calc = get_operations(calc)
            for name, calc_value in calc.items():
                if name in ret:
                    data = replacer(calc_value, name, ret[name])
                    ret[name] = calculate(data)

        return ret
