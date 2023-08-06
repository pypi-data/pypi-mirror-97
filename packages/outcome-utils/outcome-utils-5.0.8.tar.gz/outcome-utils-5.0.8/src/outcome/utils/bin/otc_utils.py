"""Utils CLI."""

import click
from outcome.utils.feature_set import FeatureSetModule
from outcome.utils.loader import load_obj


@click.group()
def main():
    ...


@main.command(help='List available feature flags')
@click.option('--feature-set', default='outcome.utils:feature_set')
def features(feature_set: str):
    fs = load_obj(feature_set, default_obj='feature_set', t=FeatureSetModule)
    fs.display_features()
