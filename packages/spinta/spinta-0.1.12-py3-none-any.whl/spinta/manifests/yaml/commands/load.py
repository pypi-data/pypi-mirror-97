import logging

from spinta import commands
from spinta.components import Context
from spinta.manifests.components import Manifest
from spinta.manifests.helpers import load_manifest_nodes
from spinta.manifests.yaml.components import YamlManifest
from spinta.manifests.yaml.helpers import read_manifest_schemas
from spinta.manifests.yaml.helpers import read_freezed_manifest_schemas

log = logging.getLogger(__name__)


@commands.load.register(Context, YamlManifest)
def load(
    context: Context,
    manifest: YamlManifest,
    *,
    into: Manifest = None,
    freezed: bool = False,
):
    target = into or manifest
    if '_schema' not in target.models:
        store = context.get('store')
        commands.load(context, store.internal, into=target)

    if freezed:
        if into:
            log.info(
                'Loading freezed manifest %r into %r from %s.',
                manifest.name,
                into.name,
                manifest.path.resolve(),
            )
        else:
            log.info(
                'Loading freezed manifest %r from %s.',
                manifest.name,
                manifest.path.resolve(),
            )
        schemas = read_freezed_manifest_schemas(manifest)
    else:
        if into:
            log.info(
                'Loading manifest %r into %r from %s.',
                manifest.name,
                into.name,
                manifest.path.resolve(),
            )
        else:
            log.info(
                'Loading manifest %r from %s.',
                manifest.name,
                manifest.path.resolve(),
            )
        schemas = read_manifest_schemas(manifest)

    if into:
        load_manifest_nodes(context, into, schemas, source=manifest)
    else:
        load_manifest_nodes(context, manifest, schemas)
