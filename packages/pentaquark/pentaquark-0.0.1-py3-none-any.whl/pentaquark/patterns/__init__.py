"""Helpers to build Cypher representation of a Node (N), a Relationship (R), a Hop (H), a Pattern (P)
and a Condition (C) including parameters
# TODO: deprecate this module? Too much correlation with the managers, especially because of the param store?
"""
from dataclasses import dataclass, field

from pentaquark.query_builders.param_store import ParameterStore


@dataclass
class ParametrizedMixin:
    param_store: ParameterStore = None
    data: dict = None

    def __post_init__(self):
        data = self.data or {}
        if self.param_store is None:
            self.param_store = ParameterStore()
        self._filters = []
        for k, v in data.items():
            key = self.param_store.add(k, v)
            self._filters.append(
                f'{k}: ${key}'
            )


@dataclass
class RelMixin:
    type: str = None
    alias: str = ""


@dataclass
class NodeMixin:
    label: str = None
    alias: str = ""


@dataclass
class N(ParametrizedMixin, NodeMixin):
    """A Node representation"""

    @property
    def _alias(self):
        return self.alias or ""

    @property
    def _label(self):
        return f":{self.label}" if self.label else ""

    def repr(self):
        alias_label = self._alias + self._label
        if not self.data:
            return f"({alias_label})"
        params = ",".join(self._filters)
        return f"({alias_label} {{ {params} }})"


@dataclass
class R(ParametrizedMixin, RelMixin):
    """A Relationship representation"""

    def repr(self):
        if self.type is None:
            self.type = ""
        if self.type.startswith("-"):
            typ = ":" + self.type[1:]
            before = "<-"
            after = "-"
        elif self.type.startswith("+"):
            typ = ":" + self.type[1:]
            before = "-"
            after = "->"
        else:
            typ = ":" + self.type if self.type else ""
            before = "-"
            after = "-"
        params = ",".join(self._filters)
        if params:
            p = f"{before}[{self.alias}{typ} {{ {params} }}]{after}"
        else:
            p = f"{before}[{self.alias}{typ}]{after}"
        return p

    def __and__(self, right_node):
        return H(
            None,
            None,
            self.type,
            self.alias,
            self.data,
            right_node.label,
            right_node.alias,
            right_node.data,
        )


@dataclass
class H(ParametrizedMixin):
    """Hop"""
    type: str = None
    r_alias: str = None
    r_data: dict = ""
    label: str = None
    n_alias: str = ""
    n_data: dict = None

    def __post_init__(self):
        super().__post_init__()
        self.rel = R(
            self.type,
            self.r_alias,
            self.param_store,
            self.r_data,
        )
        self.right_node = N(
            self.label,
            self.n_alias,
            self.param_store,
            self.n_data,
        )

    def repr(self):
        return f"{self.rel.repr()} {self.right_node.repr()}"


@dataclass
class P(ParametrizedMixin):
    """A Pattern with a right node and an arbitrary number of hops
     ()-[]-()....-[]-()
     """
    left_node: N = None
    hops: list[H] = field(default_factory=list)

    def __post_init__(self):
        if self.left_node is None:
            raise TypeError("P.left_node can not be null")
        self.left_node.param_store = self.param_store
        super().__post_init__()
        self._cypher = f"{self.left_node.repr()}"
        for h in self.hops:
            h.param_store = self.param_store
            self._cypher += f" {h.repr()}"

    def traverse(self, hop):
        self._cypher += " " + hop.repr()
        return self

    def __and__(self, hop):
        """
        P(...) & H(...)
        """
        return self.traverse(hop)

    def repr(self):
        return self._cypher
