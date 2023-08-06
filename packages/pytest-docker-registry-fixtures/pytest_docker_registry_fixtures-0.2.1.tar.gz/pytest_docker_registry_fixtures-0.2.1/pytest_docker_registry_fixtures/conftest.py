#!/usr/bin/env python

"""Configures execution of pytest."""


def pytest_addoption(parser):
    """pytest add option."""
    # TODO: Figure out why pytest tries to load this file twice ?!?
    try:
        parser.addoption(
            "--push-image",
            action="append",
            default=[],
            help="list of docker images to be replicated into the pytest docker registry.",
        )
        parser.addoption(
            "--always-pull",
            action="store",
            default=True,
            help="If True, images will be pulled prior to replication.",
        )
    except ValueError as exception:
        if "already added" not in str(exception):
            raise exception


def pytest_collection_modifyitems(config: "_pytest.config.Config", items):
    """pytest collection modifier."""

    # pytest fixtures of scope=session don't appear to be able to find markers using request.node.get_closest_marker().
    # Copy from markers to options here, and counteract for duplicate invocations / assignments when used in fixtures.
    for item in items:
        images = item.get_closest_marker("push_image")
        if images:
            option = getattr(config.option, "push_image", [])
            option.extend(images.args)
            setattr(config.option, "push_image", option)


def pytest_configure(config: "_pytest.config.Config"):
    """pytest configuration hook."""
    config.addinivalue_line(
        "markers",
        "push_image: list of docker images to be staged in the pytest docker registry.",
    )
