# Only expose public API

from .util import check_if_update_needed

from .client import (
    Client,
    LabeledDataset,
    LabeledFrame,
    Inferences,
    InferencesFrame,
    LabelClassMap,
    ClassMapEntry,
    ClassMapUpdateEntry,
    CustomMetricsDefinition,
    StratifiedMetricsDefinition,
    viridis_rgb,
)
from .collection_client import CollectionClient

from .issues import IssueManager, Issue, IssueElement


# TODO: Avoid duplicating here while still getting nice autodoc?
__all__ = [
    "Client",
    "CollectionClient",
    "LabeledDataset",
    "LabeledFrame",
    "Inferences",
    "InferencesFrame",
    "LabelClassMap",
    "ClassMapEntry",
    "ClassMapUpdateEntry",
    "CustomMetricsDefinition",
    "StratifiedMetricsDefinition",
    "viridis_rgb",
    "IssueManager",
    "Issue",
    "IssueElement",
]

check_if_update_needed()
