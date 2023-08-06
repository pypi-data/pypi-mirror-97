"""Calculate the typed dict artifacts for a model."""

import typing

from open_alchemy import types as oa_types
from open_alchemy.schemas.artifacts import types as artifacts_types

from .. import types
from . import type_


class ReturnValue(typing.NamedTuple):
    """The return value for the calculated artifacts."""

    required: typing.List[types.ColumnArtifacts]
    not_required: typing.List[types.ColumnArtifacts]


def _get_write_only(
    artifacts: artifacts_types.TAnyPropertyArtifacts,
) -> typing.Optional[bool]:
    """Get write only for any property artifacts."""
    if artifacts.type == oa_types.PropertyType.SIMPLE:
        return artifacts.open_api.write_only
    if artifacts.type == oa_types.PropertyType.JSON:
        return artifacts.open_api.write_only
    if artifacts.type == oa_types.PropertyType.RELATIONSHIP:
        return artifacts.write_only
    return None


def _calculate(
    *,
    artifacts: typing.Iterable[typing.Tuple[str, artifacts_types.TAnyPropertyArtifacts]]
) -> typing.Iterable[types.ColumnArtifacts]:
    """Calculate the typed dict artifacts from property artifacts."""
    no_dict_ignore_properties = filter(
        lambda args: not (
            args[1].type == oa_types.PropertyType.SIMPLE
            and args[1].extension.dict_ignore
        ),
        artifacts,
    )
    no_dict_ignore_no_write_only = filter(
        lambda args: not _get_write_only(args[1]),
        no_dict_ignore_properties,
    )
    return map(
        lambda args: types.ColumnArtifacts(
            name=args[0],
            type=type_.typed_dict(artifacts=args[1]),
            description=args[1].description,
        ),
        no_dict_ignore_no_write_only,
    )


def calculate(*, artifacts: artifacts_types.ModelArtifacts) -> ReturnValue:
    """
    Calculate the typed dict artifacts from model schema artifacts.

    Args:
        artifacts: The schema artifacts for a model.

    Returns:
        The artifacts for the typed dict.

    """
    required = filter(lambda args: args[1].required, artifacts.properties)
    not_required = filter(lambda args: not args[1].required, artifacts.properties)

    return ReturnValue(
        required=list(_calculate(artifacts=required)),
        not_required=list(_calculate(artifacts=not_required)),
    )
