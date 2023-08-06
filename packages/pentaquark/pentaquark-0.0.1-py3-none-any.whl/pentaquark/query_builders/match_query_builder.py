"""Where the MATCH Cypher query is built.
"""
import logging
from pentaquark.constants import START_NODE_ALIAS, SEPARATOR
from .pattern_builder import PatternBuilder
from .where_query_builder import Predicate, C
from .query_builder import QueryBuilder


logger = logging.getLogger(__name__)


class MatchQueryBuilder(QueryBuilder):
    """MATCH query builder"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._order_by = []
        self._limit = None
        self._skip = None
        self._where = Predicate()

    def match(self, **kwargs):
        # self._variables = [START_NODE_ALIAS]
        pb = PatternBuilder(self.model, param_store=self._param_store, variables_in_external_scope=self._variables)
        match = pb.build(kwargs)
        self._match.append(match)
        # self._variables.extend(pb._variables)
        return self

    def optional_match(self, **kwargs):
        return self

    def where(self, *args, **kwargs):
        for a in args:
            if not isinstance(a, Predicate):
                raise TypeError(f"where args must be instances of 'C' (condition), found {a.__class__.__name__}")
            self._where &= a
        for a, value in kwargs.items():
            c = C(**{a: value})
            self._where &= c
        return self

    def order_by(self, *args):
        for a in args:
            a = START_NODE_ALIAS + SEPARATOR + a
            variable, prop = a.rsplit(SEPARATOR, 1)
            if variable not in self._variables:
                raise ValueError(f"Can not order by non existing variable ({variable})")
            # TODO: check that property exists, otherwise raise a Warning (not an Exception, to ease migrations)
            self._order_by.append(a)
        return self

    def skip(self, skip):
        self._skip = skip
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    def _build_match_query(self):
        return "MATCH " + "\n".join(self._match)

    def _build_where_query(self):
        if self._where:
            logger.info(self._where)
            q = self._where.compile(model=self.model, param_store=self._param_store, variables=self._variables)
            return "WHERE " + q
        return ""

    def _build_return_query(self):
        return "RETURN " + self._returns_to_cypher(self._return)

    def _build_order_by_query(self):
        q = []
        for a in self._order_by:
            variable, prop = a.rsplit(SEPARATOR, 1)
            q.append(f"{variable}.{prop}")
        return ",".join(q)

    def _build_post_return_query(self):
        q = ""
        if self._order_by:
            q += "ORDER BY " + self._build_order_by_query() + "\n"
        if self._skip:
            q += f"SKIP {self._skip}\n"
        if self._limit:
            q += f"LIMIT {self._limit}"
        return q

    def _build_query(self):
        self._query = self._build_match_query() + "\n" \
                      + self._build_where_query() + "\n" \
                      + self._build_return_query() + "\n" \
                      + self._build_post_return_query()
