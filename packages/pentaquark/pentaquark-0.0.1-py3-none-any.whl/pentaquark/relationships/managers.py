# import warnings
import logging
import collections.abc

from pentaquark.constants import START_NODE_ALIAS, SEPARATOR, RELATIONSHIP_OBJECT_KEY
from pentaquark.db import connection
from pentaquark.exceptions import PentaquarkInvalidOperationError, PentaQuarkObjectDoesNotExistError
from .enums import RelationshipCardinality
from ..mixins import IteratorMixin
from ..query_builders.param_store import ParameterStore

logger = logging.getLogger(__name__)


class RelationshipSet:
    def __init__(self, relationships=None):
        self.relationships = relationships or []

    def __eq__(self, other):
        return self.relationships == other.relationships

    def __bool__(self):
        return len(self.relationships) > 0

    def __str__(self):
        return f"<RelationshipSet {str(self.relationships)}>"

    def __repr__(self):
        return f"<RelationshipSet {str(self.relationships)}>"

    def add(self, rel):
        if isinstance(rel, collections.abc.Iterable):
            self.relationships.extend(rel)
        else:
            self.relationships.append(rel)

    def items(self):
        for r in self.relationships:
            yield r.end_node, r

    def nodes(self):
        return [r.end_node for r in self.relationships]

    # TODO: is this method needed
    def __iter__(self):
        return iter(self.relationships)

    def __next__(self):
        yield from self.relationships

    def __getitem__(self, item):
        try:
            return self.relationships[item]
        except IndexError as e:
            raise PentaQuarkObjectDoesNotExistError(e)


class RelationshipManager(IteratorMixin):
    base_iterator = dict

    def __init__(self, instance, rel_property):
        super().__init__()
        self.instance = instance
        self.rel_property = rel_property
        self.is_sync = False

    def items(self):
        for r in self.related_objects:
            yield r.end_node, r

    def __iter__(self):
        # TODO: manage cases where there are multiple relationships between the same two nodes
        for item in self.related_objects:
            yield item.end_node

    def __next__(self):
        for item in self:
            yield item

    def _get_cached_or_fetch(self, /, one=False, ret_params=None):
        ret_params = ret_params or []
        if not self.related_objects:  # TODO: reduce the number of queries when there is no related object!
            related_objects = RelationshipSet()
            # fetch data
            data = self._fetch_data(*ret_params, raw=True, )
            if not data:
                return None if one else RelationshipSet()
            for d in data:
                related_objects.add(
                    self.hydrate(**d)
                )
            # res = [self.hydrate(**d) for d in data]
            self.related_objects = related_objects
        if one:
            return self.related_objects[0]
        return self.related_objects

    def _fetch_data(self, *ret_params, raw=False, ):
        """

        :param ret_params: return parameters
        :return:
        """
        returns = [
            *ret_params
            # f"{self.rel_property.name}{SEPARATOR}{p}" for p in ret_params
        ] if ret_params else [self.rel_property.name]
        data = self.instance.__class__.q.match(
            **self.instance.get_id_dict()
        ).returns(*returns)
        if raw:
            data = data.raw().one()
            related_data = data[START_NODE_ALIAS][self.rel_property.name]
            return related_data
        data = data.all()
        # related_data = data[START_NODE_ALIAS][self.rel_property.name]
        return [getattr(d, self.rel_property.name) for d in data]

    def one(self, *ret_params):
        r = self._get_cached_or_fetch(one=True, ret_params=ret_params)
        if r:
            return r.end_node

    def _get_filter_condition(self, key, value, obj):
        """

        :param key: parameter name  (+lookup if any)
        :param value: filter value
        :param obj: objects to be filtered
        :return:
        """
        if SEPARATOR in key:
            field, lookup = key.rsplit(SEPARATOR, 1)
        else:
            field = key
            lookup = "eq"
        if field not in obj._properties:
            raise ValueError(f"'{field}' is not a valid property for {obj.__class__.__name__}")
        if lookup != "eq":
            raise NotImplementedError(f"Lookup {lookup} is not (yet) implemented in the filter method. "
                                      f"You have to filter yourself.")
        return getattr(obj, field) == value

    def filter(self, *ret_params, **kwargs):
        data = self._get_cached_or_fetch(one=False, ret_params=ret_params)
        res = []
        for d in data.nodes():
            if all(
                self._get_filter_condition(k, v, d) for k, v in kwargs.items()
            ):
                res.append(d)
        return res

    def all(self, *ret_params):
        c = self._get_cached_or_fetch(ret_params=ret_params)
        return c.nodes()

    def get(self,  *ret_params):
        if self.rel_property.cardinality == RelationshipCardinality.UNIQUE_STRICT:
            return self.one(*ret_params)
        return self.all(*ret_params)

    @property
    def related_objects(self):
        cached_properties = self.instance.cached_properties
        if self.rel_property.name in cached_properties:
            return cached_properties[self.rel_property.name]
        return RelationshipSet()

    @related_objects.setter
    def related_objects(self, value):
        self.instance.cached_properties[self.rel_property.name] = value

    def _add_single(self, ins, **kwargs):
        from .models import Relationship
        self._check_other_is_valid(ins)
        related_objects = self.related_objects
        related_objects = RelationshipSet([related_objects]) \
            if not isinstance(related_objects, collections.abc.Iterable) else related_objects
        model_class = self.rel_property.model or Relationship
        relationship = model_class(
            start_node=self.instance,
            end_node=ins,
            **kwargs
        )
        related_objects.add(relationship)
        self.related_objects = related_objects
        return related_objects

    def _check_other_is_valid(self, other):
        # check node label is consistent with relationship definition
        other_label = other.get_label()
        if other_label != self.rel_property.target_node_labels:
            raise Exception(f"{other_label} not a valid target for {self.rel_property.name} "
                            f"(accepting: {self.rel_property.target_node_labels})")
        # check the relationship cardinality
        # FIXME: first if should not be commented
        # if other in self.related_objects:
        #     raise PentaQuarkCardinalityError(
        #         f"There is already a relationship of type {self.rel_property.rel_type} "
        #         f"between {self.rel_property.instance} and {other}"
        #     )
        # elif (
        #         self.cardinality == RelationshipCardinality.UNIQUE_LABEL
        #         and any(o.get_label() == other.get_label() for o in self._others)
        # ):
        #     raise AtomicUniquenessViolationError(
        #         f"There is already a relationship of type {self.rel_type} between {self.source} "
        #         f"and a node with label {other.get_label()}"
        #     )

    def add(self, ins, **kwargs):
        if kwargs and not self.rel_property.model:
            raise TypeError("Can not provide kwargs for relationships without model")
        if not ins:
            raise ValueError("cannot add empty or None objects")
        if isinstance(ins, RelationshipSet):
            self.related_objects = ins
            # for i in ins:
            #     if not i:
            #         continue
            #     related_objects.add(self._add_single(i.end_node, **kwargs))
            return self.related_objects
        return self._add_single(ins, **kwargs)

    def hydrate(self, **kwargs):
        from .models import Relationship
        target_node_class = self.get_target_model()
        target_instance = target_node_class.hydrate(**kwargs)
        rel_model_class = self.rel_property.model or Relationship
        rel_data = kwargs.get(RELATIONSHIP_OBJECT_KEY)
        if rel_data:
            rel_data = rel_data[0]
        else:
            rel_data = {}
        return rel_model_class(
            start_node=self.instance,
            end_node=target_instance,
            **rel_data
        )

    def connect(self, other, **kwargs):
        if not self.instance._is_in_neo:
            raise ValueError(f"You must first save the source object before connecting to another node ({self})")
        if not other._is_in_neo:
            raise ValueError(f"You must first save the target object before connecting to another node ({other})")
        self.add(other, **kwargs)
        self._save(other, **kwargs)

    def get_target_model(self):
        return self.rel_property.get_target_node_class()

    def _save(self, other, **kwargs):
        ps = ParameterStore()
        source = self.instance
        source_data = source.get_id_dict()
        source_node_cypher = source.to_cypher_match(alias=START_NODE_ALIAS, param_store=ps, data=source_data)
        target_data = other.get_id_dict()
        target = self.get_target_model()
        target_node_cypher = target.to_cypher_match(alias="target", param_store=ps, data=target_data)
        rel_pattern = self.rel_property.rel_pattern(alias="rel", param_store=ps, data=kwargs)
        q = f"""MATCH {source_node_cypher.repr()}
        MATCH {target_node_cypher.repr()}
        CREATE ({source_node_cypher.alias}) {rel_pattern.repr()} ({target_node_cypher.alias})
        """
        params = ps.params
        connection.cypher(q, params)

    # NB: method not used (yet?)
    def next(self, item):
        if item == RELATIONSHIP_OBJECT_KEY:
            return self.rel_property.model
        if item == self.rel_property.target_node_labels:
            return self.rel_property.get_target_node_class()
        raise PentaquarkInvalidOperationError(f"{item} is not a valid lookup for "
                                              f"{self.rel_property.__class__.__name__}")

    # def match(self, **kwargs):
    #     # data = self.instance.__class__.q.match(
    #     #     **self.instance.get_id_dict()
    #     # ).returns(self.rel_property.name).raw().one()
    #     prefix = START_NODE_ALIAS + SEPARATOR + self.rel_property.name
    #     qb = MatchQueryBuilder(
    #         model=self.instance.__class__,
    #         prefix=prefix,
    #     )
    #     return qb.match(**kwargs)
