import logging

from pentaquark.relationships.managers import RelationshipManager
from pentaquark.relationships.enums import RelationshipCardinality, RelationshipDirection
from ..constants import SEPARATOR, RELATIONSHIP_OBJECT_KEY
from ..exceptions import PentaQuarkInvalidMatchOperationException
from ..utils import split_kwargs_into_first_level_and_remaining
from ..patterns import R
from ..registry import node_registry
from .scalars import Property

logger = logging.getLogger(__name__)


class RelationshipProperty(Property):

    def __init__(self,
                 rel_type,
                 target_node_labels,
                 direction=RelationshipDirection.OUTGOING,
                 cardinality=RelationshipCardinality.NONE,
                 model=None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.rel_type = rel_type
        self.target_node_labels = target_node_labels
        self.direction = direction
        self.cardinality = cardinality
        self.model = model

    def get_target_node_class(self):
        return node_registry[self.target_node_labels]

    def rel_type_with_direction(self):
        if self.direction == RelationshipDirection.OUTGOING:
            rel_type = f"+{self.rel_type}"
        elif self.direction == RelationshipDirection.INCOMING:
            rel_type = f"-{self.rel_type}"
        else:
            rel_type = self.rel_type
        return rel_type

    def rel_pattern(self, alias, param_store, data=None):
        rel_type = self.rel_type_with_direction()
        return R(
            type=rel_type,
            alias=alias or "",
            data=data,
            param_store=param_store,
        )

    def to_cypher_match(self, alias="", rel_data=None, data=None,
                        variables=None, param_store=None,
                        include_alias=True, include_label=True):
        variables = variables or []
        rel_data = rel_data or {}
        kwargs = data or {}
        target_node_class = self.get_target_node_class()
        first_level_ks, remaining_ks = split_kwargs_into_first_level_and_remaining(target_node_class, data=kwargs)
        # logger.debug("RELATIONSHIP TO_CYPHER_MATCH kws %s / %s", first_level_ks, remaining_ks)
        if len(remaining_ks) > 1:
            # do not allow 'branching', ie (a)-[r1]-(b) and (a)-[r2]-(c)
            # only direct paths are supported for now (a)-[r1]-(b)-[r2]-(c)
            raise PentaQuarkInvalidMatchOperationException(
                "Branching not supported in MATCH clause, maybe you can use a WHERE instead?"
            )
        if alias:
            rel_alias = alias + SEPARATOR + RELATIONSHIP_OBJECT_KEY
            variables.append(rel_alias)
        else:
            rel_alias = ""
        h = R(
            self.rel_type_with_direction(),
            rel_alias,
            rel_data,
        ) & target_node_class.to_cypher_match(
                alias=alias,
                include_alias=include_alias,
                include_label=include_label,
                param_store=param_store,
                data=first_level_ks,
            )
        for k, v in remaining_ks.items():
            # NB: for now, it is actually not a loop, since remaining_ks must contain only one element
            # perform another HOP through a relationship to a target node
            # this hop is managed by the target_node_class manager
            h &= target_node_class.traverse_cypher(k, variables=variables, data=v, alias=rel_alias+k)
        return h

    @classmethod
    def to_cypher_return(cls, *args):
        pass

    def bind(self, instance, name):
        # WARNING: do not set instance here, since it is only called once
        #  when model is initialized
        super().bind(None, name)

    def __get__(self, instance, owner):
        """Get value from cache in instance or retrieve from db.

        :param instance: instance of calling class
        :param owner: type of calling class
        :return:
        """
        return RelationshipManager(instance, self)

    def __set__(self, instance, value):
        raise AttributeError()

    def get_graphql_type(self):
        model = node_registry[self.target_node_labels]
        if self.cardinality == RelationshipCardinality.UNIQUE_STRICT:
            return model.get_graphql_type()
        return f"[{model.get_graphql_type()}]"


class RelationshipPropertyIn(RelationshipProperty):
    def __init__(self,
                 rel_type,
                 target_node_labels,
                 cardinality=RelationshipCardinality.NONE,
                 model=None,
                 **kwargs
                 ):
        if "direction" in kwargs:
            raise TypeError("RelationshipIn does not accept 'direction' parameter")
        super().__init__(rel_type, target_node_labels,
                         direction=RelationshipDirection.INCOMING,
                         cardinality=cardinality,
                         model=model, **kwargs)


class RelationshipPropertyOut(RelationshipProperty):
    def __init__(self,
                 rel_type,
                 target_node_labels,
                 cardinality=RelationshipCardinality.NONE,
                 model=None,
                 **kwargs
                 ):
        if "direction" in kwargs:
            raise TypeError("RelationshipOut does not accept 'direction' parameter")
        super().__init__(rel_type, target_node_labels,
                         direction=RelationshipDirection.OUTGOING,
                         cardinality=cardinality,
                         model=model, **kwargs)
