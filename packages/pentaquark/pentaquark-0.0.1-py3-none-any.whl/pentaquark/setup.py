import importlib
import logging

from pentaquark import settings
from pentaquark.models.nodes import Node
from pentaquark.registry import node_registry, RegistryConstants

logger = logging.getLogger(__name__)


def setup(paths=None, klasses=None):
    if klasses:
        for kls in klasses:
            register_models(kls)
        return
    paths = paths or settings.APPS
    for app in paths:
        importlib.import_module(f"{app}.models")
    for kls in Node.__subclasses__():
        logger.debug("PENTAQUARK SETUP registering %s", kls)
        register_model(kls, raises=False)


def register_models(models):
    for m in models:
        register_model(m)


def register_model(klass, name=None, raises=True):
    n = name or klass.get_label()
    if n in ["NodeModelBase", "Node"]:
        return
    node_registry.add(n, klass, if_exists=RegistryConstants.RAISE if raises else RegistryConstants.SKIP)
