from pentaquark.constants import START_NODE_ALIAS, SEPARATOR
from pentaquark.exceptions import PentaQuarkInvalidMatchOperationException
from pentaquark.patterns import P
from pentaquark.utils import split_kwargs_into_first_level_and_remaining, unflatten_dict


class PatternBuilder:
    """
    Helper class to build a pattern ()-[]-() (optionally with multiple hops)
    Manages parameters
    """
    def __init__(self,
                 model,
                 param_store,
                 start_node_alias=None,
                 create_aliases=True,
                 variables_in_external_scope=None,
                 append_to_global_scope=True,
                 ):
        self.model = model
        self._param_store = param_store
        self.start_node_alias = start_node_alias or START_NODE_ALIAS
        self.create_aliases = create_aliases
        self._global_scope = variables_in_external_scope if variables_in_external_scope is not None else []
        self._local_scope = self._global_scope if append_to_global_scope else []

    @staticmethod
    def _parse_kwargs_tree(**kwargs):
        return unflatten_dict(**kwargs)

    def build(self, data, include_alias=True, include_label=True):
        ks = self._parse_kwargs_tree(**data)
        first_level_ks, remaining_ks = split_kwargs_into_first_level_and_remaining(self.model, data=ks)
        if len(remaining_ks) > 1:
            # do not allow 'branching', ie (a)-[r1]-(b) and (a)-[r2]-(c)
            # only direct paths are supported for now (a)-[r1]-(b)-[r2]-(c)
            raise PentaQuarkInvalidMatchOperationException(
                "Branching not supported in MATCH clause, maybe you can use a WHERE instead?"
            )
        n = self.model.to_cypher_match(
            alias=self.start_node_alias,
            param_store=self._param_store,
            variables=self._global_scope,
            include_label=self.start_node_alias not in self._global_scope,
            include_alias=True,
            data=first_level_ks,
        )
        self._local_scope.append(n.alias)
        p = P(left_node=n, param_store=self._param_store)
        for k, v in remaining_ks.items():
            # NB: for now, it is actually not a loop, since remaining_ks must contain only one element
            # call manager for the relationship to build the -[]-() pattern
            if self.create_aliases:
                var = START_NODE_ALIAS + SEPARATOR + k
                self._local_scope.append(var)
            else:
                var = None
            h = self.model.traverse_cypher(
                k,
                alias=var,
                variables=self._global_scope,
                param_store=self._param_store,
                include_alias=include_alias,
                include_label=include_label,
                data=v,
            )
            p = p & h

        return p.repr()
