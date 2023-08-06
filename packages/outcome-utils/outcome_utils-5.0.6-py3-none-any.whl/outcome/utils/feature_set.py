"""Feature flag management."""

import re
import warnings
from enum import Enum
from typing import Dict, Literal, Optional, Protocol, Union

from outcome.utils import env
from outcome.utils.config import Config
from rich.console import Console
from rich.table import Table

StateSource = Literal['config', 'default']


class FeatureSetModule(Protocol):  # pragma: no cover
    def display_features(self) -> None:
        ...


class FeatureException(Exception):
    ...


class FeatureType(Enum):
    boolean = 'boolean'
    string = 'string'


_feature_pattern = '^[a-z]+(_?[a-z]+_?[a-z])*$'
_feature_prefix = 'WITH_FEAT_'

_features: Dict[str, Union[bool, str, None]]
_feature_types: Dict[str, FeatureType]
_config: Config


def reset():
    global _config, _features, _feature_types
    _config = Config()  # noqa: WPS122,WPS442
    _features = {}  # noqa: WPS122,WPS442
    _feature_types = {}  # noqa: WPS122,WPS442


reset()


def _is_valid_feature_name(feature: str) -> bool:
    return all(re.match(_feature_pattern, part) is not None for part in feature.split('.'))


def _feature_to_config_key(feature: str) -> str:
    replaced = feature.replace('.', '_').upper()
    return f'{_feature_prefix}{replaced}'


def _coerce_boolean(v: object) -> bool:
    return str(v).lower() in {'yes', 'y', 'true', 't', '1'}


def set_config(config: Config) -> None:
    global _config
    _config = config  # noqa: WPS122,WPS442


def register_feature(
    feature: str, default: Optional[Union[bool, str]] = None, feature_type: FeatureType = FeatureType.boolean,
) -> None:
    if not _is_valid_feature_name(feature):
        raise FeatureException(f'Invalid feature name: {feature}')

    if feature in _features:
        raise FeatureException(f'Duplicate feature: {feature}')

    if feature_type not in list(FeatureType):
        raise FeatureException(f'Invalid Type: {feature_type}')

    if default is None and feature_type == FeatureType.boolean:
        default = False

    _features[feature] = default
    _feature_types[feature] = feature_type


def features() -> Dict[str, bool]:
    return {k: is_active(k) for k in _features.keys()}


def display_features() -> None:  # pragma: no cover
    console = Console()

    table = Table(show_header=True, header_style='bold')
    table.add_column('Feature Flag')
    table.add_column('State', justify='right')
    table.add_column('Feature Type')
    table.add_column('Default State', justify='right')
    table.add_column('Config Key', justify='left')
    table.add_column('Set By', justify='right')

    def state_repr(state: Union[str, bool, None]):
        return '[bold green]active[/bold green]' if state else '[bold red]inactive[/bold red]'

    def type_repr(feature_type: FeatureType):
        return feature_type.value

    for feat, state in features().items():
        table.add_row(
            feat,
            state_repr(state),
            type_repr(_feature_types[feat]),
            state_repr(_features[feat]),
            _feature_to_config_key(feat),
            _feature_state_source(feat),
        )

    console.print(table)


def is_active(feature: str) -> bool:
    if not _feature_check(feature):
        return False

    value = _feature_status_from_config(feature)

    if value is not None:
        return bool(value)

    return bool(_features[feature])


def value(feature: str) -> Optional[Union[str, bool]]:
    if not _feature_check(feature):
        return None

    val = _feature_status_from_config(feature)

    if val is not None:
        return val

    return _features[feature]


def _feature_status_from_config(feature: str) -> Optional[Union[str, bool]]:
    try:
        feature_key = _feature_to_config_key(feature)
        val = _config.get(feature_key)

        if _feature_types[feature] == FeatureType.boolean:
            return val if isinstance(val, bool) else _coerce_boolean(val)
        return str(val)

    except KeyError:
        return None


def _feature_state_source(feature: str) -> StateSource:
    _feature_check(feature)

    val = _feature_status_from_config(feature)

    if val is None:
        return 'default'
    return 'config'


def _feature_check(feature: str) -> bool:
    if feature not in _features:
        if env.is_dev():
            warnings.warn(
                f'Checking unknown feature "{feature}", maybe you forgot to register it? This will raise an exception in production',  # noqa: E501
                RuntimeWarning,
            )
            return False
        raise FeatureException(f'Unknown feature: {feature}')
    return True


def set_feature_default(feature: str, default_state: bool) -> None:
    _feature_check(feature)
    _features[feature] = default_state
