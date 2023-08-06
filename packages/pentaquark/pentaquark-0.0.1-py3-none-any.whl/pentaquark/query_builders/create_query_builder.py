import logging
import collections.abc

from pentaquark.db import connection
from .query_builder import QueryBuilder
from ..exceptions import PentaQuarkObjectDoesNotExistError

logger = logging.getLogger(__name__)


class CreateQueryBuilder(QueryBuilder):
    def create(self, ins=None, **kwargs):
        new_ins = ins or self.model(**kwargs)
        properties = new_ins._get_property_kwargs()
        new_ins.check_required_properties(properties)
        with connection.transaction():
            # create instance
            new_ins = self._create(**properties)
            # if relationships, add relationships
            for rn, rel_property in new_ins._relationships.items():
                related_obj = None
                if ins:  # get relationship from instance cached_properties
                    logger.warning(ins.cached_properties)
                    try:
                        related_obj = getattr(ins, rn).get()
                    except PentaQuarkObjectDoesNotExistError:
                        pass
                elif rn in kwargs:  # try to get relationship object from kwargs
                    related_obj = kwargs[rn]
                elif key := self._related_obj_id_in_kwargs(kwargs, rn):  # get target node id
                    related_obj = self._get_related_object(rel_property, kwargs[key])
                logger.warning(f"{rn}, {related_obj}")
                if related_obj:
                    rel_manager = getattr(new_ins, rn)
                    if isinstance(related_obj, collections.abc.Iterable):
                        for ro in related_obj:
                            rel_manager.connect(ro)
                    else:
                        rel_manager.connect(related_obj)
        new_ins.post_create()
        return new_ins

    def _related_obj_id_in_kwargs(self, kwargs, key):
        key_with_id = f"{key}_id"
        if key_with_id in kwargs:
            return key_with_id
        return None

    def _get_related_object(self, rel_property, target_id):
        target_model = rel_property.get_target_node_class()
        target_instance = target_model.q.match(**{target_model.get_id_property_name(): target_id}).one()
        return target_instance

    def _create(self, **kwargs):
        label = self.model._meta.label
        cypher = f"CREATE (n:{label})\n"
        cypher += "SET " + ",".join(f'n.{k}=${k}' for k in kwargs)
        cypher += "\nRETURN n"
        params = {
            pn: prop.to_cypher(kwargs[pn]) for pn, prop in self.model._properties.items() if pn in kwargs
        }
        res = connection.cypher(cypher, params)
        hydrated = self._hydrate(res)
        if hydrated:
            return hydrated[0]

    def merge(self, ins):
        return self._merge(ins)

    def _merge(self, ins):
        label = self.model._meta.label
        id_property_name = self.model.get_id_property_name()
        properties = ins._get_property_kwargs()
        ins.check_required_properties(properties)
        cypher = f"MATCH (n:{label} {{{id_property_name}: ${id_property_name} }})\n"
        cypher += "SET " + ",".join(f'n.{k}=${k}' for k in properties if k != id_property_name)
        params = {
            pn: prop.to_cypher(properties[pn]) for pn, prop in self.model._properties.items() if pn in properties
        }
        connection.cypher(cypher, params)
        return ins

    def _build_query(self):
        pass
