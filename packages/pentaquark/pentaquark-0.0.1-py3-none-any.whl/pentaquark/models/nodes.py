import logging
from collections.abc import Iterable

from pentaquark.constants import SEPARATOR
from pentaquark.exceptions import PentaQuarkConfigurationError
from pentaquark.models.base import PropertyModelBase, RESERVED_KEYWORDS
from pentaquark.patterns import N
from pentaquark.properties import CypherProperty
from pentaquark.relationships.enums import RelationshipCardinality
from pentaquark.relationships.managers import RelationshipSet
from pentaquark.utils import unflatten_list

logger = logging.getLogger(__name__)


def cypher(return_type):
    def decorated(meth):
        """Just attach an attribute to the decorated method"""
        meth._is_cypher_property = True
        meth._return_type = return_type
        return meth
    return decorated


def graphql_property(graphql_type, name=None, requires=None):
    def decorated(meth):
        meth._is_graphql_property = True
        meth._graphql_type = graphql_type
        meth._graphql_name = name
        meth._requires = requires
        return meth
    return decorated


def graphql_query(name, graphql_return_type, graphql_input_type=None, graphql_input: str = None):
    def decorated(meth):
        meth._is_graphql_query = True
        meth._graphql_name = name
        meth._graphql_return_type = graphql_return_type
        meth._graphql_input_type = graphql_input_type
        meth._graphql_input = graphql_input
        return meth
    return decorated


class NodeMeta(PropertyModelBase):
    def __init__(cls, name, bases, attrs):
        from pentaquark.properties.relationships import RelationshipProperty
        from pentaquark.properties import CypherProperty
        relationships = {}
        graphql_properties = {}
        for attr_name, attr in attrs.items():
            if isinstance(attr, RelationshipProperty):
                if SEPARATOR in attr_name:
                    raise PentaQuarkConfigurationError(f"'{attr_name}' contains {SEPARATOR}")
                if attr_name in RESERVED_KEYWORDS:
                    raise PentaQuarkConfigurationError(f"'{attr_name}' is a reserved keyword")
                relationships[attr_name] = attr
                continue
            if getattr(attr, "_is_cypher_property", None):
                func = getattr(cls, attr_name)
                setattr(cls,
                        attr_name,
                        CypherProperty(cypher=func(), return_type=func._return_type)
                        )
            if getattr(attr, "_is_graphql_property", None):
                name = attr._graphql_name or attr_name
                graphql_properties[name] = attr
        # manage inheritance
        for b in bases:
            if hasattr(b, "relationships"):
                relationships.update(b._relationships)  # noqa
        cls._relationships = relationships
        cls._graphql_properties = graphql_properties
        PropertyModelBase.__init__(cls, name, bases, attrs)


class Node(metaclass=NodeMeta):
    id_property = "id"
    help_text = ""
    unique_together = ()

    def __init__(self, **kwargs):
        from pentaquark.relationships.models import Relationship
        self.cached_properties = {}
        self._is_in_neo = False
        self.is_sync = False
        # self.q.bind(self)

        properties_iter = self._properties
        for fn, prop in properties_iter.items():
            prop.bind(self, fn)
            val = kwargs.pop(fn, None)
            if val is None:
                # if prop.required:
                #     raise ValueError(f"Field {fn} is mandatory but no value provided")
                if hasattr(prop, "source"):
                    val = getattr(self, prop.source, None) or kwargs.get(prop.source, None)
                elif prop.default:
                    try:
                        val = prop.default()
                    except TypeError:  # not callable
                        val = prop.default
            setattr(self, fn, val)

        relationships_iter = self._relationships
        for rn, rel in relationships_iter.items():
            rel.bind(self, rn)
            rel_ins = kwargs.get(rn)
            rel_model_class = rel.model or Relationship
            if rel.required and rel_ins is None:
                raise ValueError(f"{rn} is a required relationship for {self.__class__.__name__}")
            if rel_ins is None:
                rel_ins = []
            elif not isinstance(rel_ins, Iterable):
                rel_ins = [rel_ins, ]
            rs = RelationshipSet()
            for ri in rel_ins:
                r = rel_model_class(
                    start_node=self,
                    end_node=ri,
                )
                rs.add(r)
            self.cached_properties[rn] = rs
            # CAN NOT SET A RELATIONSHIP (?)
            # rel_manager = getattr(self, rn)
            # rel_manager.is_sync = False
            # setattr(self, rn, kwargs.get(rn, []))

    def __str__(self):
        return f"{self.get_id_property_name()}: {self.get_id()}"

    def __repr__(self):
        return f"<{self._meta.label} {self.__str__()}>"

    # Node characteristics
    @classmethod
    def get_label(cls):
        return cls._meta.label

    @classmethod
    def get_id_property_name(cls):
        return cls.id_property

    @classmethod
    def get_property_graphql_type(cls, prop_name=None):
        if not prop_name:
            prop_name = cls.get_id_property_name()
        return cls._properties[prop_name].graphql_type

    def get_id(self):
        return getattr(self, self.get_id_property_name(), None)

    def get_id_dict(self):
        id_prop_name = self.get_id_property_name()
        id_prop = self._properties[id_prop_name]
        return {
            id_prop_name: id_prop.to_cypher(self.get_id()),
        }

    @classmethod
    def get_id_property_graphql_type(cls):
        id_property_name = cls.get_id_property_name()
        id_property = cls._properties.get(id_property_name)
        return id_property.get_graphql_type()

    @classmethod
    def get_graphql_type(cls):
        return cls.get_label()

    def _get_property_kwargs(self):
        properties = {}
        for pn, prop in self._properties.items():
            if (x := getattr(self, pn, None)) is not None:
                properties[pn] = x
            elif prop.has_default:
                properties[pn] = prop.default_value()
        return properties

    def _get_relationship_names_list(self) -> list[str]:
        return list(self._relationships.keys())

    def check_required_properties(self, kwargs=None):
        """Check that all required properties are set
        (before save for instance)
        """
        for pn, prop in self._properties.items():
            if kwargs:
                v = kwargs.get(pn, None)
            else:
                v = getattr(self, pn, None)
            if prop.required and v is None:
                raise ValueError(f"Field {pn} is mandatory but no value provided")

    # Node uniqueness
    def __eq__(self, other):
        if self.is_sync:
            if self_id := getattr(self, self.get_id_property_name()):
                if other_id := getattr(other, other.get_id_property_name()):
                    return self_id == other_id
            return False
        else:
            return True
        # else, compare unique elements

    # Hydrate from DB
    @classmethod
    def hydrate(cls, **kwargs):
        kls = cls()
        for pn, prop in kls._properties.items():
            setattr(kls, pn, prop.from_cypher(kwargs.get(pn)))
        for rn, _ in kls._relationships.items():
            if kw := kwargs.get(rn):
                cls.hydrate_related_object(kls, rn, kw)
        kls.is_sync = True
        kls._is_in_neo = True
        return kls

    @classmethod
    def hydrate_related_object(cls, kls, rn, rn_kwargs):
        if not rn_kwargs:
            return
        rel = getattr(kls, rn, None)
        rel_instances = RelationshipSet([
            rel.hydrate(**k) for k in rn_kwargs
        ])
        if rel_instances:
            rel_manager = getattr(kls, rn)
            rel_manager.add(rel_instances)

    # DB operations
    def save(self):
        # self._check_required_properties()
        if self.exists():
            return self.merge()
        ins = self.q.create(ins=self)
        if ins:
            ins.is_sync = True
            ins._is_in_neo = True
        return ins

    def exists(self):
        return self.q.exists(ins=self)

    def merge(self):
        ins = self.q.merge(ins=self)
        if ins:
            ins.is_sync = True
            ins._is_in_neo = True
        return ins

    def post_create(self):
        pass

    def detach_delete(self):
        return self.q.detach_delete(**self.get_id_dict())

    def delete(self):
        return self.q.delete(**self.get_id_dict())

    @classmethod
    def to_cypher_match(cls, alias="", data=None,
                        variables=None, param_store=None,
                        include_alias=True, include_label=True):
        # logger.debug("NODE.to_cypher_match include_alias=%s, include_label=%s", include_alias, include_label)
        kwargs = data or {}
        for k, v in kwargs.items():
            if k not in cls._properties or isinstance(k, CypherProperty):
                raise AttributeError(f"'{k}' is not a valid property for model {cls.__name__}")
        # if alias in variables and include_alias:
        #     return N(alias=alias)
        return N(
            label=cls._meta.label if include_label else None,
            alias=alias if include_alias else "",
            data=kwargs,
            param_store=param_store,
        )

    @classmethod
    def to_cypher_return(cls, *args):
        pass

    @classmethod
    def traverse_cypher(
            cls, relationship, alias, variables,
            include_alias=True, include_label=True, param_store=None, data=None) -> str:
        # logger.debug("NODE.TRAVERSE rel=%s, alias=%s, data=%s", relationship, alias, data)
        relationship_manager = getattr(cls, relationship, None)
        if relationship_manager is None:
            raise AttributeError(f"'{relationship}' is not a valid relationship for model {cls.__name__}")
        return relationship_manager.rel_property.to_cypher_match(
            alias, variables=variables,
            include_alias=include_alias, include_label=include_label,
            param_store=param_store, data=data)

    def to_graphql_return(self, ret_values: list[str]) -> dict:
        result = {}
        values = unflatten_list(*ret_values)
        for v in values:
            if isinstance(v, dict):  # relationship or graphql property
                rel_key, rel_values = next(iter(v.items()))
                if rel_key in self._relationships:
                    rel = self._relationships[rel_key]
                    related_instances = getattr(self, rel_key)
                    res = []
                    for ri in related_instances.all():
                        res.append(ri.to_graphql_return(rel_values))
                    if rel.cardinality == RelationshipCardinality.NONE:
                        result[rel_key] = res
                    else:
                        result[rel_key] = res[0]
                elif rel_key in self._graphql_properties:
                    result[rel_key] = getattr(self, rel_key)(rel_values)
                else:
                    raise ValueError(f"'{v}' unrecognized")
            elif v in self._properties:
                if x := getattr(self, v):
                    result[v] = self._properties[v].to_graphql(x)
            elif v in self._graphql_properties:
                result[v] = getattr(self, v)()
            else:
                raise ValueError(f"'{v}' unrecognized")
        return result

    @graphql_property("String", name="__typename")
    def typename(self):
        return self.get_label()

    def get_existance_query(self):
        filters = {}
        for u in self.unique_together:
            if value := getattr(self, u):
                filters[u] = value
        return filters
        # for f in fields:
        #     try:
        #         selection = f.selection_set.selections
        #     except AttributeError:
        #         selection = None
        #     print(f)
        #     if selection:
        #         print(f.name.value, selection)
        #         if f.name.value in self._relationships:
        #             rel = self._relationships[f.name.value]
        #             related_instances = getattr(self, f.name.value)
        #             res = []
        #             for ri in related_instances:
        #                 res.append(ri.to_graphql_return(selection))
        #             if rel.cardinality == RelationshipCardinality.NONE:
        #                 result[f] = res
        #             else:
        #                 result[f] = res[0]
        #         else:
        #             raise TypeError("Unmanaged case")
        #     else:
        #         result[f.name.value] = getattr(self, f.name.value)
        # return result
