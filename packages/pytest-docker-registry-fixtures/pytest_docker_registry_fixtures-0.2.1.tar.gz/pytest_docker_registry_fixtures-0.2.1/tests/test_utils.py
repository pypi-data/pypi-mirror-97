#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""pytest fixture tests."""

import logging

from base64 import b64encode
from http.client import HTTPSConnection
from json import loads
from pathlib import Path
from typing import Dict, List, Union

import pytest
import www_authenticate

from OpenSSL import crypto
from _pytest.tmpdir import TempPathFactory

from pytest_docker_registry_fixtures import (
    DockerRegistrySecure,
    DOCKER_REGISTRY_SERVICE_PATTERN,
    generate_cacerts,
    generate_htpasswd,
    generate_keypair,
    get_docker_compose_user_defined,
    get_embedded_file,
    get_pushed_images,
    get_user_defined_file,
    ImageName,
    replicate_image,
    replicate_manifest_list,
)

LOGGER = logging.getLogger(__name__)


def get_auth_headers(
    docker_registry_secure: DockerRegistrySecure, image_name: ImageName
) -> Union[Dict[str, str], None]:
    # pylint: disable=protected-access
    """
    Retrieves the authentication headers for a given image.
    Args:
        docker_registry_secure: The secure docker registry from which to retrieve the authentication headers.
        image_name: The name of the image for which to retrieve the headers.

    Returns: The authentication headers, or None.
    """
    # Try to retrieve credentials first ...
    auth_header_src = None
    for endpoint in docker_registry_secure.docker_client.api._auth_configs.auths:
        if image_name.endpoint in endpoint:
            credentials = docker_registry_secure.docker_client.api._auth_configs.auths[
                endpoint
            ]
            auth = b64encode(
                f"{credentials['username']}:{credentials['password']}".encode("utf-8")
            ).decode("utf-8")
            auth_header_src = {"Authorization": f"Basic {auth}"}

    if not auth_header_src:
        return None

    # Try to retrieve an authentication token ...
    https_connection = HTTPSConnection(host=image_name.endpoint)
    https_connection.request("GET", url="/v2/", headers=auth_header_src)
    auth_params = www_authenticate.parse(
        https_connection.getresponse().headers["Www-Authenticate"]
    )
    bearer = auth_params["bearer"]

    https_connection = HTTPSConnection(host=image_name.endpoint)
    https_connection.request(
        "GET",
        url=f"{bearer['realm']}?service={bearer['service']}&scope=repository:{image_name.image}:pull&"
        f"client_id=pytest-docker-registry-fixtures",
        headers=auth_header_src,
    )
    payload = loads(https_connection.getresponse().read())
    assert payload["token"]
    return {"Authorization": f"Bearer {payload['token']}"}


def verify_http_response(
    https_connection: HTTPSConnection, image_name: ImageName, media_type: str
):
    """
    Verifies the http response checking for the existence of an image.
    Args:
        https_connection: The HTTPS connection from which to retrieve the HTTP response.
        image_name: The name of the image being verified.
        media_type: The media type of the registry manifest.
    """
    response = https_connection.getresponse()
    assert response.status == 200
    assert response.headers["Content-Type"] == media_type
    if image_name.digest:
        assert response.headers["Docker-Content-Digest"] == image_name.digest


# TODO: test_check_url_secure


def test_generate_cacerts(tmp_path_factory: TempPathFactory, tmp_path: Path):
    """Test that a temporary cacerts file can be generated."""
    certificate = "MY CERTIFICATE VALUE"
    path = tmp_path.joinpath("certificate")
    path.write_text(certificate, "utf-8")
    path_last = None
    for path in generate_cacerts(tmp_path_factory, certificate=path):
        assert path.exists()
        content = path.read_text("utf-8")
        assert certificate in content
        path_last = path
    assert path_last
    assert not path_last.exists()


def test_generate_htpasswd(tmp_path_factory: TempPathFactory):
    """Test that a temporary htpasswd file can be generated."""
    username = "myusername"
    password = "mypassword"
    path_last = None
    for path in generate_htpasswd(
        tmp_path_factory, password=password, username=username
    ):
        assert path.exists()
        content = path.read_text("utf-8")
        assert username in content
        assert password not in content
        path_last = path
    assert path_last
    assert not path_last.exists()


def test_generate_keypair():
    """Test that a keypair can be generated."""
    keypair = generate_keypair()
    assert keypair.ca_certificate
    assert keypair.ca_private_key
    assert keypair.certificate
    assert keypair.private_key

    x509_store = crypto.X509Store()
    ca_certificate = crypto.load_certificate(
        crypto.FILETYPE_PEM, keypair.ca_certificate
    )
    x509_store.add_cert(ca_certificate)

    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, keypair.certificate)
    x509_store_context = crypto.X509StoreContext(x509_store, certificate)
    x509_store_context.verify_certificate()


def test_get_docker_compose_user_defined(docker_compose_files: List[str]):
    """Tests that the user defined check fails here."""

    service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("insecure", 0)
    for _ in get_docker_compose_user_defined(docker_compose_files, service_name):
        assert False
    service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("secure", 0)
    for _ in get_docker_compose_user_defined(docker_compose_files, service_name):
        assert False


def test_get_embedded_file(tmp_path_factory: TempPathFactory):
    """Test that an embedded file can be replicated to a temporary file."""
    path_last = None
    for path in get_embedded_file(tmp_path_factory, name="docker-compose.yml"):
        assert path.exists()
        content = path.read_text("utf-8")
        assert "registry" in content
        path_last = path
    assert path_last
    assert not path_last.exists()


def test_get_pushed_images_empty(request):
    """Tests that 'push_image' pytest marks can be retrieved."""

    assert not get_pushed_images(request)


def test_get_user_defined_file(pytestconfig: "_pytest.config.Config"):
    """Tests that the user defined check fails here."""

    for _ in get_user_defined_file(pytestconfig, "does_not_exist"):
        assert False


@pytest.mark.push_image("tianon/true")
def test_get_pushed_images_not_empty(request):
    """Tests that 'push_image' pytest marks can be retrieved."""

    assert "tianon/true" in get_pushed_images(request)


@pytest.mark.online
@pytest.mark.parametrize(
    "image",
    [
        "tianon/true@sha256:009cce421096698832595ce039aa13fa44327d96beedb84282a69d3dbcf5a81b",
        "tianon/true:latest",
        "tianon/true:latest@sha256:009cce421096698832595ce039aa13fa44327d96beedb84282a69d3dbcf5a81b",
        "tianon/true",
    ],
)
def test_replicate_image(docker_registry_secure: DockerRegistrySecure, image: str):
    """Tests that images can be replicated."""

    image_name = ImageName.parse(image)
    replicate_image(
        docker_registry_secure.docker_client,
        image_name,
        docker_registry_secure.endpoint,
    )

    media_type = "application/vnd.docker.distribution.manifest.v2+json"
    https_connection = HTTPSConnection(
        context=docker_registry_secure.ssl_context, host=docker_registry_secure.endpoint
    )
    if image_name.digest:
        https_connection.request(
            "GET",
            url=f"/v2/{image_name.image}/manifests/{image_name.digest}",
            headers={"Accept": media_type, **docker_registry_secure.auth_header},
        )
        verify_http_response(https_connection, image_name, media_type)
    if image_name.tag:
        # TODO: Fixgure out why HTTPSConnection cannot perform multiple requests ?!?
        https_connection = HTTPSConnection(
            context=docker_registry_secure.ssl_context,
            host=docker_registry_secure.endpoint,
        )
        https_connection.request(
            "GET",
            url=f"/v2/{image_name.image}/manifests/{image_name.tag}",
            headers={"Accept": media_type, **docker_registry_secure.auth_header},
        )
        verify_http_response(https_connection, image_name, media_type)


@pytest.mark.online
@pytest.mark.parametrize(
    "manifest_list",
    [
        "index.docker.io/library/busybox@sha256:4b6ad3a68d34da29bf7c8ccb5d355ba8b4babcad1f99798204e7abb43e54ee3d",
        "index.docker.io/library/busybox:1.30.1",
        "index.docker.io/library/busybox:1.30.1@"
        "sha256:4b6ad3a68d34da29bf7c8ccb5d355ba8b4babcad1f99798204e7abb43e54ee3d",
    ],
)
def test_replicate_manifest_list(
    docker_registry_secure: DockerRegistrySecure, manifest_list: str
):
    """Tests that manifest lists can be replicated."""

    image_name = ImageName.parse(manifest_list)

    # Try to retrieve credentials first ...
    auth_header_src = get_auth_headers(docker_registry_secure, image_name)
    if not auth_header_src:
        pytest.skip("Unable to retrieve credentials for: %s", image_name.endpoint)

    # Replicate all of the manifests referenced in the manifest list ...
    for image in [
        "library/busybox@sha256:4fe8827f51a5e11bb83afa8227cbccb402df840d32c6b633b7ad079bc8144100",
        "library/busybox@sha256:abc043b5132f825e44eefffc35535b1f24bd3f1bb60b11943863563a46795fdc",
        "library/busybox@sha256:07717dd5f074de0cf4f7ca8f635cb63aef63d789f15a22ab482a3d27a0a1f881",
        "library/busybox@sha256:8dfe92e22300734a185375b6316d01aa1a2b0623d425a5e6e406771ba5642bf1",
        "library/busybox@sha256:3bdba83255bf7c575e31e129b2ddf1c0c32382e112cb051af6c5143c24a5ddbd",
        "library/busybox@sha256:bb87f507b42a6efe6f1d5382c826f914673a065f4d777b54b52f5414d688837a",
        "library/busybox@sha256:a09f03056efb5d3facb5077a9e58e83e9bba74ad4d343b2afa92c70b5ae01e2b",
        "library/busybox@sha256:0b671b6a323d86aa6165883f698b557ca257c3a3ffa1e3152ffb6467e7ac11b3",
    ]:
        img_name = ImageName.parse(image)
        replicate_image(
            docker_registry_secure.docker_client,
            img_name,
            docker_registry_secure.endpoint,
        )

    # Replicate the manifest list ...
    replicate_manifest_list(
        image_name,
        docker_registry_secure.endpoint,
        auth_header_dest=docker_registry_secure.auth_header,
        auth_header_src=auth_header_src,
        ssl_context_dest=docker_registry_secure.ssl_context,
    )

    media_type = "application/vnd.docker.distribution.manifest.list.v2+json"
    https_connection = HTTPSConnection(
        context=docker_registry_secure.ssl_context, host=docker_registry_secure.endpoint
    )
    if image_name.digest:
        https_connection.request(
            "GET",
            url=f"/v2/{image_name.image}/manifests/{image_name.digest}",
            headers={"Accept": media_type, **docker_registry_secure.auth_header},
        )
        verify_http_response(https_connection, image_name, media_type)
    if image_name.tag:
        # TODO: Figure out why HTTPSConnection cannot perform multiple requests ?!?
        https_connection = HTTPSConnection(
            context=docker_registry_secure.ssl_context,
            host=docker_registry_secure.endpoint,
        )
        https_connection.request(
            "GET",
            url=f"/v2/{image_name.image}/manifests/{image_name.tag}",
            headers={"Accept": media_type, **docker_registry_secure.auth_header},
        )
        verify_http_response(https_connection, image_name, media_type)


# TODO: test_start_service
