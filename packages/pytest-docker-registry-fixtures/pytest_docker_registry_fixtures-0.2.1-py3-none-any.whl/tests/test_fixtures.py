#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""pytest fixture tests."""

import logging

from base64 import b64decode
from pathlib import Path
from ssl import SSLContext
from typing import Dict, List

import pytest
import requests

from docker import DockerClient
from requests.exceptions import SSLError

from pytest_docker_registry_fixtures import (
    DockerRegistryCerts,
    DockerRegistryInsecure,
    DockerRegistrySecure,
    DOCKER_REGISTRY_SERVICE_PATTERN,
    get_pushed_images,
    ImageName,
)

LOGGER = logging.getLogger(__name__)


# Override fixture for testing
@pytest.fixture(scope="session")
def pdrf_scale_factor() -> int:
    """Provides the number enumerated instances to be instantiated."""
    return 4


def no_duplicates(lst: List) -> bool:
    """Tests if a list contains duplicate values."""
    return len(lst) == len(set(lst))


def test_docker_client(docker_client: DockerClient):
    """Tests that a docker client can be instantiated."""
    assert docker_client


def test_docker_compose_insecure(docker_compose_insecure: Path):
    """Test that the embedded docker-compose for insecure registries can be copied to a temporary file."""
    service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("insecure", 0)
    assert service_name in docker_compose_insecure.read_text()


def test_docker_compose_insecure_list(
    docker_compose_insecure_list: List[Path], pdrf_scale_factor: int
):
    """Test that the embedded docker-compose for insecure registries can be copied to a temporary file."""
    for i in range(pdrf_scale_factor):
        service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("insecure", i)
        assert service_name in docker_compose_insecure_list[i].read_text()
    assert no_duplicates(docker_compose_insecure_list)


def test_docker_compose_secure(docker_compose_secure: Path):
    """Test that the embedded docker-compose for secure registries can be copied to a temporary file."""
    service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("secure", 0)
    assert service_name in docker_compose_secure.read_text()


def test_docker_compose_secure_list(
    docker_compose_secure_list: List[Path], pdrf_scale_factor: int
):
    """Test that the embedded docker-compose for secure registries can be copied to a temporary file."""
    for i in range(pdrf_scale_factor):
        service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("secure", i)
        assert service_name in docker_compose_secure_list[i].read_text()
    assert no_duplicates(docker_compose_secure_list)


def test_docker_registry_auth_header(
    docker_registry_auth_header: Dict[str, str],
    docker_registry_password: str,
    docker_registry_username: str,
):
    """Test that an HTTP basic authentication header can be provided."""
    assert "Authorization" in docker_registry_auth_header
    string = b64decode(
        docker_registry_auth_header["Authorization"].split()[1].encode("utf-8")
    ).decode("utf-8")
    assert docker_registry_password in string
    assert docker_registry_username in string


def test_docker_registry_auth_header_list(
    docker_registry_auth_header_list: List[Dict[str, str]],
    docker_registry_password_list: List[str],
    docker_registry_username_list: List[str],
    pdrf_scale_factor: int,
):
    """Test that an HTTP basic authentication header can be provided."""
    for i in range(pdrf_scale_factor):
        assert "Authorization" in docker_registry_auth_header_list[i]
        string = b64decode(
            docker_registry_auth_header_list[i]["Authorization"]
            .split()[1]
            .encode("utf-8")
        ).decode("utf-8")
        assert docker_registry_password_list[i] in string
        assert docker_registry_username_list[i] in string
    assert no_duplicates([str(i) for i in docker_registry_auth_header_list])
    assert no_duplicates(docker_registry_password_list)
    assert no_duplicates(docker_registry_username_list)


def test_docker_registry_cacerts(
    docker_registry_cacerts: Path, docker_registry_certs: DockerRegistryCerts
):
    """Test that a temporary CA certificate trust store can be provided."""
    assert docker_registry_cacerts.exists()
    cacerts = docker_registry_cacerts.read_text("utf-8")

    ca_cert = docker_registry_certs.ca_certificate.read_text("utf-8")
    assert ca_cert in cacerts

    ca_key = docker_registry_certs.ca_private_key.read_text("utf-8")
    assert ca_key not in cacerts

    cert = docker_registry_certs.certificate.read_text("utf-8")
    assert cert not in cacerts

    key = docker_registry_certs.private_key.read_text("utf-8")
    assert key not in cacerts


def test_docker_registry_cacerts_list(
    docker_registry_cacerts_list: List[Path],
    docker_registry_certs_list: List[DockerRegistryCerts],
    pdrf_scale_factor: int,
):
    """Test that a temporary CA certificate trust store can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_registry_cacerts_list[i].exists()
        cacerts = docker_registry_cacerts_list[i].read_text("utf-8")

        ca_cert = docker_registry_certs_list[i].ca_certificate.read_text("utf-8")
        assert ca_cert in cacerts

        ca_key = docker_registry_certs_list[i].ca_private_key.read_text("utf-8")
        assert ca_key not in cacerts

        cert = docker_registry_certs_list[i].certificate.read_text("utf-8")
        assert cert not in cacerts

        key = docker_registry_certs_list[i].private_key.read_text("utf-8")
        assert key not in cacerts
    assert no_duplicates(docker_registry_cacerts_list)
    assert no_duplicates(docker_registry_certs_list)


def test_docker_registry_certs(docker_registry_certs: DockerRegistryCerts):
    """Test that a certificate and private key can be provided."""
    assert docker_registry_certs.ca_certificate.exists()
    assert "BEGIN CERTIFICATE" in docker_registry_certs.ca_certificate.read_text(
        "utf-8"
    )
    assert docker_registry_certs.ca_private_key.exists()
    assert "BEGIN PRIVATE KEY" in docker_registry_certs.ca_private_key.read_text(
        "utf-8"
    )
    assert docker_registry_certs.certificate.exists()
    assert "BEGIN CERTIFICATE" in docker_registry_certs.certificate.read_text("utf-8")
    assert docker_registry_certs.private_key.exists()
    assert "BEGIN PRIVATE KEY" in docker_registry_certs.private_key.read_text("utf-8")


def test_docker_registry_certs_list(
    docker_registry_certs_list: List[DockerRegistryCerts], pdrf_scale_factor: int
):
    """Test that a certificate and private key can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_registry_certs_list[i].ca_certificate.exists()
        assert "BEGIN CERTIFICATE" in docker_registry_certs_list[
            i
        ].ca_certificate.read_text("utf-8")
        assert docker_registry_certs_list[i].ca_private_key.exists()
        assert "BEGIN PRIVATE KEY" in docker_registry_certs_list[
            i
        ].ca_private_key.read_text("utf-8")
        assert docker_registry_certs_list[i].certificate.exists()
        assert "BEGIN CERTIFICATE" in docker_registry_certs_list[
            i
        ].certificate.read_text("utf-8")
        assert docker_registry_certs_list[i].private_key.exists()
        assert "BEGIN PRIVATE KEY" in docker_registry_certs_list[
            i
        ].private_key.read_text("utf-8")
    assert no_duplicates(docker_registry_certs_list)


def test_docker_registry_htpasswd(
    docker_registry_htpasswd: Path,
    docker_registry_password: str,
    docker_registry_username: str,
):
    """Test that a htpasswd can be provided."""
    assert docker_registry_htpasswd.exists()
    content = docker_registry_htpasswd.read_text("utf-8")
    assert docker_registry_username in content
    assert docker_registry_password not in content


def test_docker_registry_htpasswd_list(
    docker_registry_htpasswd_list: List[Path],
    docker_registry_password_list: List[str],
    docker_registry_username_list: List[str],
    pdrf_scale_factor: int,
):
    """Test that a htpasswd can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_registry_htpasswd_list[i].exists()
        content = docker_registry_htpasswd_list[i].read_text("utf-8")
        assert docker_registry_username_list[i] in content
        assert docker_registry_password_list[i] not in content
    assert no_duplicates(docker_registry_htpasswd_list)
    assert no_duplicates(docker_registry_password_list)
    assert no_duplicates(docker_registry_username_list)


# Note: Cannot test both w/ and w/o images, as the fixtures is session scoped, and will push_images
#       from other test cases.
@pytest.mark.online
def test_docker_registry_insecure(docker_registry_insecure: DockerRegistryInsecure):
    """Test that an insecure docker registry can be instantiated without images."""
    assert "127.0.0.1" in docker_registry_insecure.endpoint

    # Should be there from session level import of 'push_image' decorator on 'test_docker_registry_secure_images'
    image_name = ImageName.parse("busybox:1.30.1")

    # Version
    response = requests.head(f"http://{docker_registry_insecure.endpoint}/v2/")
    assert response.status_code == 200

    # Tag list
    response = requests.get(
        f"http://{docker_registry_insecure.endpoint}/v2/{image_name.image}/tags/list"
    )
    assert response.status_code == 200
    assert image_name.tag in response.json()["tags"]

    # Manifest
    response = requests.head(
        f"http://{docker_registry_insecure.endpoint}/v2/{image_name.image}/manifests/{image_name.tag}"
    )
    assert response.status_code == 200
    assert "Docker-Content-Digest" in response.headers


# Note: Cannot test both w/ and w/o images, as the fixtures is session scoped, and will push_images
#       from other test cases.
@pytest.mark.online
def test_docker_registry_insecure_list(
    docker_registry_insecure_list: List[DockerRegistryInsecure], pdrf_scale_factor: int
):
    """Test that an insecure docker registry can be instantiated without images."""
    for i in range(pdrf_scale_factor):
        assert "127.0.0.1" in docker_registry_insecure_list[i].endpoint

        # Should be there from session level import of 'push_image' decorator on 'test_docker_registry_secure_images'
        image_name = ImageName.parse("busybox:1.30.1")

        # Version
        response = requests.head(
            f"http://{docker_registry_insecure_list[i].endpoint}/v2/"
        )
        assert response.status_code == 200

        if i > 0:
            continue

        # Tag list
        response = requests.get(
            f"http://{docker_registry_insecure_list[i].endpoint}/v2/{image_name.image}/tags/list"
        )
        assert response.status_code == 200
        assert image_name.tag in response.json()["tags"]

        # Manifest
        response = requests.head(
            f"http://{docker_registry_insecure_list[i].endpoint}/v2/{image_name.image}/manifests/{image_name.tag}"
        )
        assert response.status_code == 200
        assert "Docker-Content-Digest" in response.headers
    assert no_duplicates([str(i) for i in docker_registry_insecure_list])


def test_docker_registry_password(docker_registry_password: str):
    """Test that a password can be provided."""
    assert docker_registry_password


def test_docker_registry_password_list(
    docker_registry_password_list: List[str], pdrf_scale_factor: int
):
    """Test that a password can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_registry_password_list[i]
    assert no_duplicates(docker_registry_password_list)


@pytest.mark.online
@pytest.mark.push_image("busybox:1.30.1")
def test_docker_registry_secure(docker_registry_secure: DockerRegistrySecure, request):
    """Test that an secure docker registry can be instantiated with images."""
    assert "127.0.0.1" in docker_registry_secure.endpoint

    image_name = ImageName.parse(get_pushed_images(request)[0])

    # Version
    response = requests.head(
        f"https://{docker_registry_secure.endpoint}/v2/",
        headers=docker_registry_secure.auth_header,
        verify=str(docker_registry_secure.cacerts),
    )
    assert response.status_code == 200

    # Tag list
    response = requests.get(
        f"https://{docker_registry_secure.endpoint}/v2/{image_name.image}/tags/list",
        headers=docker_registry_secure.auth_header,
        verify=str(docker_registry_secure.cacerts),
    )
    assert response.status_code == 200
    assert image_name.tag in response.json()["tags"]

    # Manifest
    response = requests.head(
        f"https://{docker_registry_secure.endpoint}/v2/{image_name.image}/manifests/{image_name.tag}",
        headers=docker_registry_secure.auth_header,
        verify=str(docker_registry_secure.cacerts),
    )
    assert response.status_code == 200
    assert "Docker-Content-Digest" in response.headers

    # Error: Unauthenticated
    response = requests.head(
        f"https://{docker_registry_secure.endpoint}/v2/",
        verify=str(docker_registry_secure.cacerts),
    )
    assert response.status_code == 401

    # Error: CA not trusted
    with pytest.raises(SSLError) as exc_info:
        requests.head(
            f"https://{docker_registry_secure.endpoint}/v2/",
            headers=docker_registry_secure.auth_header,
        )
    assert "CERTIFICATE_VERIFY_FAILED" in str(exc_info.value)


@pytest.mark.online
@pytest.mark.push_image("busybox:1.30.1")
def test_docker_registry_secure_list(
    docker_registry_secure_list: List[DockerRegistrySecure],
    pdrf_scale_factor: int,
    request,
):
    """Test that an secure docker registry can be instantiated with images."""
    for i in range(pdrf_scale_factor):
        assert "127.0.0.1" in docker_registry_secure_list[i].endpoint

        image_name = ImageName.parse(get_pushed_images(request)[0])

        # Version
        response = requests.head(
            f"https://{docker_registry_secure_list[i].endpoint}/v2/",
            headers=docker_registry_secure_list[i].auth_header,
            verify=str(docker_registry_secure_list[i].cacerts),
        )
        assert response.status_code == 200

        if i < 1:
            # Tag list
            response = requests.get(
                f"https://{docker_registry_secure_list[i].endpoint}/v2/{image_name.image}/tags/list",
                headers=docker_registry_secure_list[i].auth_header,
                verify=str(docker_registry_secure_list[i].cacerts),
            )
            assert response.status_code == 200
            assert image_name.tag in response.json()["tags"]

            # Manifest
            response = requests.head(
                f"https://{docker_registry_secure_list[i].endpoint}/v2/{image_name.image}/manifests/{image_name.tag}",
                headers=docker_registry_secure_list[i].auth_header,
                verify=str(docker_registry_secure_list[i].cacerts),
            )
            assert response.status_code == 200
            assert "Docker-Content-Digest" in response.headers

        # Error: Unauthenticated
        response = requests.head(
            f"https://{docker_registry_secure_list[i].endpoint}/v2/",
            verify=str(docker_registry_secure_list[i].cacerts),
        )
        assert response.status_code == 401

        # Error: CA not trusted
        with pytest.raises(SSLError) as exc_info:
            requests.head(
                f"https://{docker_registry_secure_list[i].endpoint}/v2/",
                headers=docker_registry_secure_list[i].auth_header,
            )
        assert "CERTIFICATE_VERIFY_FAILED" in str(exc_info.value)
    assert no_duplicates([str(i) for i in docker_registry_secure_list])


def test_docker_registry_ssl_context(docker_registry_ssl_context: SSLContext):
    """Test that an ssl context can be provided."""
    assert isinstance(docker_registry_ssl_context, SSLContext)


def test_docker_registry_ssl_context_list(
    docker_registry_ssl_context_list: List[SSLContext], pdrf_scale_factor: int
):
    """Test that an ssl context can be provided."""
    for i in range(pdrf_scale_factor):
        assert isinstance(docker_registry_ssl_context_list[i], SSLContext)
    assert no_duplicates(docker_registry_ssl_context_list)


def test_docker_registry_username(docker_registry_username: str):
    """Test that a username can be provided."""
    assert docker_registry_username


def test_docker_registry_username_list(
    docker_registry_username_list: List[str], pdrf_scale_factor: int
):
    """Test that a username can be provided."""
    for i in range(pdrf_scale_factor):
        assert docker_registry_username_list[i]
    assert no_duplicates(docker_registry_username_list)
