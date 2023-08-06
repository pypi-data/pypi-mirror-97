"""
"""
from pentaquark.constants import SEPARATOR, RELATIONSHIP_OBJECT_KEY, MANAGER_ATTRIBUTE_NAME
from pentaquark.lookups import LOOKUPS
from pentaquark.models.managers import Manager
from pentaquark.properties import Property
from pentaquark.exceptions import PentaQuarkConfigurationError

RESERVED_KEYWORDS = LOOKUPS + [
    SEPARATOR,
    RELATIONSHIP_OBJECT_KEY,
    MANAGER_ATTRIBUTE_NAME,
]


class MetaModelOptions:
    def __init__(
            self,
            label=None,
            **kwargs
    ):
        self.label = label


class PropertyModelBase(type):

    def __init__(cls, name, bases, attrs):
        """Metaclass for Models

        - Create dict of properties
            - Check property name is not a reserved keyword
        - Parse Meta options

        :param args:
        :param kwargs:
        """
        from pentaquark.properties.relationships import RelationshipProperty
        # deal with properties and relationships
        properties = {}
        for attr_name, attr in attrs.items():
            if attr_name in RESERVED_KEYWORDS:
                raise PentaQuarkConfigurationError(f"'{attr_name}' is a reserved keyword")
            if isinstance(attr, Property) and not isinstance(attr, RelationshipProperty):
                if SEPARATOR in attr_name:
                    raise PentaQuarkConfigurationError(f"'{attr_name}' contains {SEPARATOR}")
                properties[attr_name] = attr
                continue
        # manage inheritance
        for b in bases:
            if hasattr(b, "_properties"):
                properties.update(b._properties)  # noqa
        cls._properties = properties

        # meta class
        label = None
        manager_class = Manager
        if 'Meta' in attrs:
            Meta = attrs.get('Meta')  # noqa
            if hasattr(Meta, 'label'):
                label = Meta.label

        cls._meta = MetaModelOptions(label=label or cls.__name__, )
        cls.q = manager_class(cls)

        type.__init__(cls, name, bases, attrs)
