#!/usr/bin/env python

# pylint: disable=redefined-outer-name,protected-access

"""ImageName tests."""

from typing import Generator, TypedDict

import pytest

from pytest_docker_registry_fixtures import ImageName


class TypingGetTestData(TypedDict):
    # pylint: disable=missing-class-docstring
    digest: str
    endpoint: str
    image: str
    object: ImageName
    string: str
    tag: str


def get_test_data() -> Generator[TypingGetTestData, None, None]:
    """Dynamically initializes test data."""
    for endpoint in ["endpoint.io", "endpoint:port", None]:
        for image in ["image", "ns0/image", "ns0/ns1/image", "ns0/ns1/ns2/image"]:
            for tag in ["tag", None]:
                for digest in ["sha256:ABCD1234", None]:
                    # Construct a complex string ...
                    string = image
                    if tag:
                        string = f"{string}:{tag}"
                    if digest:
                        string = f"{string}@{digest}"
                    if endpoint:
                        string = f"{endpoint}/{string}"
                    yield {
                        "digest": digest,
                        "endpoint": endpoint,
                        "image": image,
                        "object": ImageName.parse(string),
                        "string": string,
                        "tag": tag,
                    }


@pytest.fixture(params=get_test_data())
def image_data(request) -> TypingGetTestData:
    """Provides ImageName instance and associated data."""
    return request.param


def test___init__(image_data: TypingGetTestData):
    """Test that image name can be instantiated."""
    assert ImageName(
        digest=image_data["digest"],
        endpoint=image_data["endpoint"],
        image=image_data["image"],
        tag=image_data["tag"],
    )


def test___str__(image_data: TypingGetTestData):
    """Test __str__ pass-through for different variants."""
    string = str(image_data["object"])
    assert image_data["image"] in string
    if image_data["digest"]:
        assert image_data["digest"] in string
    else:
        assert "sha256" not in string
    if image_data["endpoint"]:
        assert image_data["endpoint"] in string
    if image_data["tag"]:
        assert image_data["tag"] in string
    assert "None" not in string


def test_clone(image_data: TypingGetTestData):
    """Test object cloning."""
    clone = image_data["object"].clone()
    assert clone != image_data["object"]
    assert str(clone) == str(image_data["object"])
    clone.endpoint = "gemini.man"
    assert str(clone) != str(image_data["object"])


def test_parse_string(image_data: TypingGetTestData):
    """Test string parsing for complex image names."""
    result = ImageName._parse_string(image_data["string"])
    assert result["digest"] == image_data["digest"]
    assert result["endpoint"] == image_data["endpoint"]
    assert result["image"] == image_data["image"]
    assert result["tag"] == image_data["tag"]


def test_parse(image_data: TypingGetTestData):
    """Test initialization via parsed strings."""
    image_name = ImageName.parse(image_data["string"])
    assert image_name.digest == image_data["digest"]
    assert image_name.endpoint == image_data["endpoint"]
    assert image_name.image == image_data["image"]
    assert image_name.tag == image_data["tag"]

    with pytest.raises(ValueError) as exception:
        ImageName.parse("a:b:c:d")
    assert str(exception.value).startswith("Unable to parse string:")


def test_digest(image_data: TypingGetTestData):
    """Tests digest retrieval."""
    assert image_data["object"].digest == image_data["digest"]


def test_endpoint(image_data: TypingGetTestData):
    """Tests endpoint retrieval."""
    assert image_data["object"].endpoint == image_data["endpoint"]


def test_image(image_data: TypingGetTestData):
    """Tests image retrieval."""
    assert image_data["object"].image == image_data["image"]


def test_tag(image_data: TypingGetTestData):
    """Tests tag retrieval."""
    assert image_data["object"].tag == image_data["tag"]
