# import enum
#
#
# class ValidationError(Exception):
#     pass
#
#
# class TypeDefsTypes(enum.Enum):
#     TYPE = "type"
#     INPUT = "input"
#     QUERY = "query"
#     MUTATION = "mutation"
#
#
# class TypeDef:
#     def __init__(self, name, properties, args=None, typ=TypeDefsTypes.TYPE, resolver=None):
#         self.type = typ
#         self.name = name
#         self.properties = properties
#         self.args = args
#         self.resolver = None
#
#     def _to_prop_list(self):
#         return "\n".join(
#             f"{k}: {v}" for k, v in self.properties.items()
#         )
#
#     def _to_arg_list(self):
#         return ",".join(
#             f"{k}: {v}" for k, v in self.args.items()
#         )
#
#     def _to_prefix(self):
#         if self.args:
#             return f"{self.type.value} ({self._to_arg_list()})"
#         return self.type.value
#
#     def to_graphql(self):
#         return f"""{self._to_prefix()} {{
#             {self._to_prop_list()}
#         }}
#         """
#
#     def bin_resolver(self, func):
#         self.resolver = func
#
#
# class QueryDef(TypeDef):
#     def __init__(self, name, args=None, properties=None, resolver=None):
#         super().__init__(name, properties, args, TypeDefsTypes.QUERY, resolver)
#
#
# class MutationDef(TypeDef):
#     def __init__(self, name, args, properties, resolver):
#         super().__init__(name, properties, args, TypeDefsTypes.MUTATION, resolver)
#
#
# class ModelTypeDef(TypeDef):
#     class Meta:
#         model = None
#
#     def __init__(self, model, name=None, args=None, properties=None, type=TypeDefsTypes.TYPE):
#         super().__init__(name, args, properties, type)
#         self.model = model
#         if self.name is None:
#             self.name = model.get_graphql_type()
#         if self.args is None:
#             self.args = model.get_property_graphql_type()
#         if self.properties is None:
#             self.properties = model.get_property_graphql_type()
#         self._validate()
#
#     def _validate(self):
#         for a in self.args:
#             if a not in self.model._properties:
#                 raise ValidationError()
#         for p in self.properties:
#             if p not in self.model._properties:
#                 raise ValidationError()
