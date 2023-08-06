"""Interface between objects and Cypher Query Builder
"""
from pentaquark.db import connection
from pentaquark.query_builders import MatchQueryBuilder, CreateQueryBuilder, ParameterStore
from pentaquark.exceptions import PentaQuarkObjectDoesNotExistError, PentaquarkInvalidOperationError
from pentaquark.query_builders.call_query_builder import CallQueryBuilder


class Manager:
    def __init__(self, model):
        self.model = model
        self._executed = False

    # RAW CYPHER
    def cypher(self, query, parameters=None):
        """Raw Cypher query"""
        raise NotImplementedError("Not implemented yet")

    # MATCH
    def match(self, **kwargs):
        qb = MatchQueryBuilder(self.model)
        return qb.match(**kwargs)

    def match_full_text(self, index, text):
        cqb = CallQueryBuilder(self.model, procedure="db.index.fulltext.queryNodes", yield_names="node, score")
        return cqb.call(index, text)

    def all(self, limit=None):
        # TODO: add a batch mode to manage cases with MANY nodes and attributes
        return self.match().all(limit=limit)

    # EXISTENCE
    def exists(self, ins=None, **kwargs):
        if ins:
            if ins.is_sync:
                return True
            if ins.get_id():
                c = self.match(**ins.get_id_dict()).exists()
                return c > 0
        ins = self.model(**kwargs)
        # unique fields
        # FIXME: filters here should never be empty?
        if filters := ins.get_existance_query():
            return self.model.q.match(
                **filters
            ).exists()
        return False
        # Build match and where kwargs
        # self.match(mkwargs).where(wkwargs)
        # if result => return True
        # else return False

    # CREATE
    def create(self, ins=None, **kwargs):
        qb = CreateQueryBuilder(self.model)
        return qb.create(ins, **kwargs)

    def merge(self, ins=None, **kwargs):
        qb = CreateQueryBuilder(self.model)
        return qb.merge(ins)

    # GET OR CREATE
    def get_or_create(self, **kwargs):
        try:
            obj = self.match(**kwargs).one()
            return obj
        except PentaQuarkObjectDoesNotExistError:
            pass
        return self.create(**kwargs)

    # DELETE
    def _delete(self, data, detach=False):
        alias = "a"
        ps = ParameterStore()
        n = self.model.to_cypher_match(
            alias=alias,
            param_store=ps,
            data=data,
        )
        cypher = f"MATCH {n.repr()} "
        if detach:
            cypher += "DETACH "
        cypher += f"DELETE {alias}"
        params = ps.params
        connection.cypher(cypher, params)

    def detach_delete(self, **kwargs):
        self._delete(kwargs, detach=True)

    def delete(self, **kwargs):
        self._delete(kwargs, detach=False)

    def next(self, item):
        n = self.model._properties.get(item) or self.model._relationships.get(item)
        if n:
            return n
        raise PentaquarkInvalidOperationError(f"{item} is not a valid lookup for {self.model.__name__}")
