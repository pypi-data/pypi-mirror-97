from typing import List
from typing import Optional

from spinta import exceptions
from spinta.auth import authorized
from spinta.backends import Backend
from spinta.backends.components import BackendOrigin
from spinta.backends.helpers import load_backend
from spinta.components import Action
from spinta.components import Context
from spinta.components import Model
from spinta.core.ufuncs import Expr
from spinta.core.ufuncs import ShortExpr
from spinta.datasets.components import Resource
from spinta.dimensions.enum.helpers import get_prop_enum
from spinta.types.datatype import Ref
from spinta.ufuncs.components import ForeignProperty
from spinta.ufuncs.helpers import merge_formulas
from spinta.utils.data import take
from spinta.utils.naming import to_code_name


def load_resource_backend(
    context: Context,
    resource: Resource,
    name: Optional[str],  # Backend name given in `ref` column.
) -> Backend:
    if name:
        # If backend name is given, just use an exiting backend.
        store = resource.dataset.manifest.store
        possible_backends = [
            # Backend defined in manifest.
            resource.dataset.manifest.backends,
            # Backend defined via configuration.
            store.backends,
        ]
        for backends in possible_backends:
            if name in backends:
                return backends[name]
        raise exceptions.BackendNotFound(resource, name=name)

    elif resource.type or resource.external:
        # If backend is defined inline on resource itself, try to load it.
        name = f'{resource.dataset.name}/{resource.name}'
        return load_backend(context, resource, name, BackendOrigin.resource, {
            'type': resource.type,
            'name': name,
            'dsn': resource.external,
        })

    else:
        # If backend was not given, try to check configuration with resource and
        # dataset names as backend names or fallback to manifest backend.
        store = resource.dataset.manifest.store
        possible_backends = [
            # Dataset and resource name combination.
            f'{resource.dataset.name}/{resource.name}',
            # Just dataset name.
            resource.dataset.name,
            # Just resource type.
            # XXX: I don't think that using resource type as a backend name is a
            #      good idea. Probably should be removed.
            resource.type,
        ]
        for name in filter(None, possible_backends):
            name = to_code_name(name)
            if name in store.backends:
                return store.backends[name]
        return resource.dataset.manifest.backend


def get_enum_filters(
    context: Context,
    model: Model,
    fpr: ForeignProperty = None,
) -> Optional[Expr]:
    args: List[Expr] = []
    for prop in take(['_id', all], model.properties).values():
        if (
            (enum := get_prop_enum(prop)) and
            authorized(context, prop, Action.GETALL)
        ):
            if not all(item.access >= prop.access for item in enum.values()):
                values = []
                for item in enum.values():
                    if item.access >= prop.access:
                        values.append(item.prepare)

                if fpr:
                    dtype = fpr.push(prop)
                else:
                    dtype = prop.dtype

                if len(values) == 1:
                    arg = values[0]
                elif len(values) > 1:
                    arg = values
                else:
                    arg = None

                if arg is not None:
                    expr = ShortExpr('eq', dtype.get_bind_expr(), arg)
                    args.append(expr)
    if len(args) == 1:
        return args[0]
    elif len(args) > 1:
        return ShortExpr('and', *args)
    else:
        return None


def get_ref_filters(
    context: Context,
    model: Model,
    fpr: ForeignProperty = None,
) -> Optional[Expr]:
    query: Optional[Expr] = None
    if fpr:
        # TODO: Rewrite properties in formula relative to base model.
        # query = merge_formulas(query, change_base_model(model.external.prepare))
        query = merge_formulas(
            query,
            get_enum_filters(context, model, fpr),
        )

    for prop in take(['_id', all], model.properties).values():
        if (
            isinstance(prop.dtype, Ref) and
            authorized(context, prop, Action.GETALL)
        ):
            if fpr:
                fpr = fpr.push(prop)
            else:
                fpr = ForeignProperty(fpr, prop.dtype)

            query = merge_formulas(
                query,
                get_ref_filters(context, prop.dtype.model, fpr),
            )

    return query
