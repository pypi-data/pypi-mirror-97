"""Functions for interacting with the OpenAlchemy models."""

import typing

import open_alchemy
from open_alchemy import types


def get_base() -> typing.Any:
    """
    Get the models.Base used as the declarative base for models.

    Returns:
        The models.Base.

    """
    # pylint: disable=no-member
    return open_alchemy.models.Base  # type: ignore


def get_model(*, name: str) -> typing.Optional[typing.Type]:
    """
    Get a model by name from models.

    Args:
        name: The name of the model.

    Returns:
        The model with the name.

    """
    return getattr(open_alchemy.models, name, None)


def get_model_schema(*, name: str) -> typing.Optional[types.Schema]:
    """
    Get the schema of a model by name from models.

    Args:
        name: The name of the model.

    Returns:
        The schema of the model with the name.

    """
    model = get_model(name=name)
    if model is None:
        return None
    return model._schema  # pylint: disable=protected-access


def set_model(*, name: str, model: typing.Type) -> None:
    """
    Set model by name on models.

    Args:
        model: The model to set.
        name: The name of the model.

    """
    setattr(open_alchemy.models, name, model)
