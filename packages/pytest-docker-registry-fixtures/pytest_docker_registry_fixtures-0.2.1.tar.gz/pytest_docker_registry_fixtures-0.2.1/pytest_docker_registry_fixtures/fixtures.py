#!/usr/bin/env python

# pylint: disable=redefined-outer-name,too-many-arguments,too-many-locals

"""The actual fixtures, you found them ;)."""

import logging
import itertools

from base64 import b64encode
from distutils.util import strtobool
from functools import partial
from pathlib import Path
from ssl import create_default_context, SSLContext
from string import Template
from time import sleep, time
from typing import Dict, Generator, List, NamedTuple

import pytest

from docker import DockerClient, from_env
from lovely.pytest.docker.compose import Services
from _pytest.tmpdir import TempPathFactory

from .imagename import ImageName
from .utils import (
    check_url_secure,
    DOCKER_REGISTRY_SERVICE,
    DOCKER_REGISTRY_SERVICE_PATTERN,
    generate_cacerts,
    generate_htpasswd,
    generate_keypair,
    get_docker_compose_user_defined,
    get_embedded_file,
    get_user_defined_file,
    replicate_image,
    start_service,
)

# Caching is needed, as singular-fixtures and list-fixtures will conflict at scale_factor=1
# This appears to only matter when attempting to start the docker secure registry service
# for the second time.
CACHE = {}

LOGGER = logging.getLogger(__name__)


class DockerRegistryCerts(NamedTuple):
    # pylint: disable=missing-class-docstring
    ca_certificate: Path
    ca_private_key: Path
    certificate: Path
    private_key: Path


class DockerRegistryInsecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    docker_client: DockerClient
    docker_compose: Path
    endpoint: str
    images: List[ImageName]
    service_name: str


# Note: NamedTuple does not support inheritance :(
class DockerRegistrySecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    auth_header: Dict[str, str]
    cacerts: Path
    certs: DockerRegistryCerts
    docker_client: DockerClient
    docker_compose: Path
    endpoint: str
    htpasswd: Path
    images: List[ImageName]
    password: str
    service_name: str
    ssl_context: SSLContext
    username: str


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    """Provides an insecure Docker API client."""
    return from_env()


def _docker_compose_insecure(
    *,
    docker_compose_files: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure docker registry service.
    """
    cache_key = _docker_compose_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("insecure", i)
        chain = itertools.chain(
            get_docker_compose_user_defined(docker_compose_files, service_name),
            # TODO: lovely-docker-compose uses the file for teardown ...
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="docker-compose.yml"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find docker compose for: %s", service_name)
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_compose_insecure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure docker registry service.
    """
    for lst in _docker_compose_insecure(
        docker_compose_files=docker_compose_files,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_compose_insecure_list(
    docker_compose_files: List[str],
    pdrf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure docker registry service.
    """
    yield from _docker_compose_insecure(
        docker_compose_files=docker_compose_files,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_compose_secure(
    *,
    docker_compose_files: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure docker registry
    service.
    """
    cache_key = _docker_compose_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("secure", i)
        chain = itertools.chain(
            get_docker_compose_user_defined(docker_compose_files, service_name),
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="docker-compose.yml"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find docker compose for: %s", service_name)
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_compose_secure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure docker registry
    service.
    """
    for lst in _docker_compose_secure(
        docker_compose_files=docker_compose_files,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_compose_secure_list(
    docker_compose_files: List[str],
    pdrf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure docker registry
    service.
    """
    yield from _docker_compose_secure(
        docker_compose_files=docker_compose_files,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_registry_auth_header(
    *,
    docker_registry_password_list: List[str],
    docker_registry_username_list: List[str],
    scale_factor: int,
) -> List[Dict[str, str]]:
    """Provides an HTTP basic authentication header containing credentials for the secure docker registry service."""
    cache_key = _docker_registry_auth_header.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        auth = b64encode(
            f"{docker_registry_username_list[i]}:{docker_registry_password_list[i]}".encode(
                "utf-8"
            )
        ).decode("utf-8")
        result.append({"Authorization": f"Basic {auth}"})
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def docker_registry_auth_header(
    docker_registry_password: str, docker_registry_username: str
) -> Dict[str, str]:
    """Provides an HTTP basic authentication header containing credentials for the secure docker registry service."""
    return _docker_registry_auth_header(
        docker_registry_password_list=[docker_registry_password],
        docker_registry_username_list=[docker_registry_username],
        scale_factor=1,
    )[0]


@pytest.fixture(scope="session")
def docker_registry_auth_header_list(
    docker_registry_password_list: List[str],
    docker_registry_username_list: List[str],
    pdrf_scale_factor: int,
) -> List[Dict[str, str]]:
    """Provides an HTTP basic authentication header containing credentials for the secure docker registry service."""
    return _docker_registry_auth_header(
        docker_registry_password_list=docker_registry_password_list,
        docker_registry_username_list=docker_registry_username_list,
        scale_factor=pdrf_scale_factor,
    )


def _docker_registry_cacerts(
    *,
    docker_registry_certs_list: List[DockerRegistryCerts],
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure docker
    registry service.
    """
    cache_key = _docker_registry_cacerts.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "cacerts"),
            generate_cacerts(
                tmp_path_factory,
                certificate=docker_registry_certs_list[i].ca_certificate,
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find or generate cacerts!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_registry_cacerts(
    docker_registry_certs: DockerRegistryCerts,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure docker
    registry service.
    """
    for lst in _docker_registry_cacerts(
        docker_registry_certs_list=[docker_registry_certs],
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_registry_cacerts_list(
    docker_registry_certs_list: List[DockerRegistryCerts],
    pdrf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure docker
    registry service.
    """
    yield from _docker_registry_cacerts(
        docker_registry_certs_list=docker_registry_certs_list,
        pytestconfig=pytestconfig,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_registry_certs(
    *, scale_factor: int, tmp_path_factory: TempPathFactory
) -> Generator[List[DockerRegistryCerts], None, None]:
    """Provides the location of temporary certificate and private key files for the secure docker registry service."""
    # TODO: Augment to allow for reading certificates from /test ...
    cache_key = _docker_registry_certs.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        tmp_path = tmp_path_factory.mktemp(__name__)
        keypair = generate_keypair()
        docker_registry_cert = DockerRegistryCerts(
            ca_certificate=tmp_path.joinpath(f"{DOCKER_REGISTRY_SERVICE}-ca-{i}.crt"),
            ca_private_key=tmp_path.joinpath(f"{DOCKER_REGISTRY_SERVICE}-ca-{i}.key"),
            certificate=tmp_path.joinpath(f"{DOCKER_REGISTRY_SERVICE}-{i}.crt"),
            private_key=tmp_path.joinpath(f"{DOCKER_REGISTRY_SERVICE}-{i}.key"),
        )
        docker_registry_cert.ca_certificate.write_bytes(keypair.ca_certificate)
        docker_registry_cert.ca_private_key.write_bytes(keypair.ca_private_key)
        docker_registry_cert.certificate.write_bytes(keypair.certificate)
        docker_registry_cert.private_key.write_bytes(keypair.private_key)
        result.append(docker_registry_cert)
    CACHE[cache_key] = result
    yield result
    for docker_registry_cert in result:
        docker_registry_cert.ca_certificate.unlink(missing_ok=True)
        docker_registry_cert.ca_private_key.unlink(missing_ok=True)
        docker_registry_cert.certificate.unlink(missing_ok=True)
        docker_registry_cert.private_key.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def docker_registry_certs(
    tmp_path_factory: TempPathFactory,
) -> Generator[DockerRegistryCerts, None, None]:
    """Provides the location of temporary certificate and private key files for the secure docker registry service."""
    for lst in _docker_registry_certs(
        scale_factor=1, tmp_path_factory=tmp_path_factory
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_registry_certs_list(
    pdrf_scale_factor: int, tmp_path_factory: TempPathFactory
) -> Generator[List[DockerRegistryCerts], None, None]:
    """Provides the location of temporary certificate and private key files for the secure docker registry service."""
    yield from _docker_registry_certs(
        scale_factor=pdrf_scale_factor, tmp_path_factory=tmp_path_factory
    )


def _docker_registry_htpasswd(
    *,
    docker_registry_password_list: List[str],
    docker_registry_username_list: List[str],
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the htpasswd file for the secure registry service."""
    cache_key = _docker_registry_htpasswd.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "htpasswd"),
            generate_htpasswd(
                tmp_path_factory,
                username=docker_registry_username_list[i],
                password=docker_registry_password_list[i],
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find or generate htpasswd!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_registry_htpasswd(
    docker_registry_password: str,
    docker_registry_username: str,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the htpasswd file for the secure registry service."""
    for lst in _docker_registry_htpasswd(
        docker_registry_password_list=[docker_registry_password],
        docker_registry_username_list=[docker_registry_username],
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_registry_htpasswd_list(
    docker_registry_password_list: List[str],
    docker_registry_username_list: List[str],
    pdrf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the htpasswd file for the secure registry service."""
    yield from _docker_registry_htpasswd(
        docker_registry_username_list=docker_registry_username_list,
        docker_registry_password_list=docker_registry_password_list,
        pytestconfig=pytestconfig,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_registry_insecure(
    *,
    docker_client: DockerClient,
    docker_compose_insecure_list: List[Path],
    docker_services: Services,
    request,
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[DockerRegistryInsecure], None, None]:
    """Provides the endpoint of a local, mutable, insecure, docker registry."""
    cache_key = _docker_registry_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("insecure", i)
        tmp_path = tmp_path_factory.mktemp(__name__)

        # Create a secure registry service from the docker compose template ...
        path_docker_compose = tmp_path.joinpath(f"docker-compose-{i}.yml")
        template = Template(docker_compose_insecure_list[i].read_text("utf-8"))
        path_docker_compose.write_text(
            template.substitute(
                {
                    "CONTAINER_NAME": service_name,
                    # Note: Needed to correctly populate the embedded, consolidated, service template ...
                    "PATH_CERTIFICATE": "/dev/null",
                    "PATH_HTPASSWD": "/dev/null",
                    "PATH_KEY": "/dev/null",
                }
            ),
            "utf-8",
        )

        LOGGER.debug("Starting insecure docker registry service [%d] ...", i)
        LOGGER.debug("  docker-compose : %s", path_docker_compose)
        LOGGER.debug("  service name   : %s", service_name)
        endpoint = start_service(
            docker_services,
            docker_compose=path_docker_compose,
            service_name=service_name,
        )
        LOGGER.debug("Insecure docker registry endpoint [%d]: %s", i, endpoint)

        images = []
        if i == 0:
            LOGGER.debug("Replicating images into %s [%d] ...", service_name, i)
            images = _replicate_images(docker_client, endpoint, request)

        result.append(
            DockerRegistryInsecure(
                docker_client=docker_client,
                docker_compose=path_docker_compose,
                endpoint=endpoint,
                images=images,
                service_name=service_name,
            )
        )
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_registry_insecure(
    docker_client: DockerClient,
    docker_compose_insecure: Path,
    docker_services: Services,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[DockerRegistryInsecure, None, None]:
    """Provides the endpoint of a local, mutable, insecure, docker registry."""
    for lst in _docker_registry_insecure(
        docker_client=docker_client,
        docker_compose_insecure_list=[docker_compose_insecure],
        docker_services=docker_services,
        request=request,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_registry_insecure_list(
    docker_client: DockerClient,
    docker_compose_insecure_list: List[Path],
    docker_services: Services,
    pdrf_scale_factor: int,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[DockerRegistryInsecure], None, None]:
    """Provides the endpoint of a local, mutable, insecure, docker registry."""
    yield from _docker_registry_insecure(
        docker_client=docker_client,
        docker_compose_insecure_list=docker_compose_insecure_list,
        docker_services=docker_services,
        request=request,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_registry_password(*, scale_factor: int) -> List[str]:
    """Provides the password to use for authentication to the secure registry service."""
    cache_key = _docker_registry_password.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(f"pytest.password.{time()}")
        sleep(0.05)
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def docker_registry_password() -> str:
    """Provides the password to use for authentication to the secure registry service."""
    return _docker_registry_password(scale_factor=1)[0]


@pytest.fixture(scope="session")
def docker_registry_password_list(pdrf_scale_factor: int) -> List[str]:
    """Provides the password to use for authentication to the secure registry service."""
    return _docker_registry_password(scale_factor=pdrf_scale_factor)


def _docker_registry_secure(
    *,
    docker_client: DockerClient,
    docker_compose_secure_list: List[Path],
    docker_registry_auth_header_list: List[Dict[str, str]],
    docker_registry_cacerts_list: List[Path],
    docker_registry_certs_list: List[DockerRegistryCerts],
    docker_registry_htpasswd_list: List[Path],
    docker_registry_password_list: List[str],
    docker_registry_ssl_context_list: List[SSLContext],
    docker_registry_username_list: List[str],
    docker_services: Services,
    request,
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[DockerRegistrySecure], None, None]:
    """Provides the endpoint of a local, mutable, secure, docker registry."""
    cache_key = _docker_registry_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = DOCKER_REGISTRY_SERVICE_PATTERN.format("secure", i)
        tmp_path = tmp_path_factory.mktemp(__name__)

        # Create a secure registry service from the docker compose template ...
        path_docker_compose = tmp_path.joinpath(f"docker-compose-{i}.yml")
        template = Template(docker_compose_secure_list[i].read_text("utf-8"))
        path_docker_compose.write_text(
            template.substitute(
                {
                    "CONTAINER_NAME": service_name,
                    "PATH_CERTIFICATE": docker_registry_certs_list[i].certificate,
                    "PATH_HTPASSWD": docker_registry_htpasswd_list[i],
                    "PATH_KEY": docker_registry_certs_list[i].private_key,
                }
            ),
            "utf-8",
        )

        LOGGER.debug("Starting secure docker registry service [%d] ...", i)
        LOGGER.debug("  docker-compose : %s", path_docker_compose)
        LOGGER.debug(
            "  ca certificate : %s", docker_registry_certs_list[i].ca_certificate
        )
        LOGGER.debug("  certificate    : %s", docker_registry_certs_list[i].certificate)
        LOGGER.debug("  htpasswd       : %s", docker_registry_htpasswd_list[i])
        LOGGER.debug("  private key    : %s", docker_registry_certs_list[i].private_key)
        LOGGER.debug("  password       : %s", docker_registry_password_list[i])
        LOGGER.debug("  service name   : %s", service_name)
        LOGGER.debug("  username       : %s", docker_registry_username_list[i])

        check_server = partial(
            check_url_secure,
            auth_header=docker_registry_auth_header_list[i],
            ssl_context=docker_registry_ssl_context_list[i],
        )
        endpoint = start_service(
            docker_services,
            check_server=check_server,
            docker_compose=path_docker_compose,
            service_name=service_name,
        )
        LOGGER.debug("Secure docker registry endpoint [%d]: %s", i, endpoint)

        # DUCK PUNCH: Inject the secure docker registry credentials into the docker client ...
        docker_client.api._auth_configs.add_auth(  # pylint: disable=protected-access
            endpoint,
            {
                "password": docker_registry_password_list[i],
                "username": docker_registry_username_list[i],
            },
        )

        images = []
        if i == 0:
            LOGGER.debug("Replicating images into %s [%d] ...", service_name, i)
            images = _replicate_images(docker_client, endpoint, request)

        result.append(
            DockerRegistrySecure(
                auth_header=docker_registry_auth_header_list[i],
                cacerts=docker_registry_cacerts_list[i],
                certs=docker_registry_certs_list[i],
                docker_client=docker_client,
                docker_compose=path_docker_compose,
                endpoint=endpoint,
                htpasswd=docker_registry_htpasswd_list[i],
                password=docker_registry_password_list[i],
                images=images,
                service_name=service_name,
                ssl_context=docker_registry_ssl_context_list[i],
                username=docker_registry_username_list[i],
            )
        )
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def docker_registry_secure(
    docker_client: DockerClient,
    docker_compose_secure: Path,
    docker_registry_auth_header: Dict[str, str],
    docker_registry_cacerts: Path,
    docker_registry_certs: DockerRegistryCerts,
    docker_registry_htpasswd: Path,
    docker_registry_password: str,
    docker_registry_ssl_context: SSLContext,
    docker_registry_username: str,
    docker_services: Services,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[DockerRegistrySecure, None, None]:
    """Provides the endpoint of a local, mutable, secure, docker registry."""
    for lst in _docker_registry_secure(
        docker_client=docker_client,
        docker_compose_secure_list=[docker_compose_secure],
        docker_registry_auth_header_list=[docker_registry_auth_header],
        docker_registry_cacerts_list=[docker_registry_cacerts],
        docker_registry_certs_list=[docker_registry_certs],
        docker_registry_htpasswd_list=[docker_registry_htpasswd],
        docker_registry_password_list=[docker_registry_password],
        docker_registry_ssl_context_list=[docker_registry_ssl_context],
        docker_registry_username_list=[docker_registry_username],
        docker_services=docker_services,
        request=request,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def docker_registry_secure_list(
    docker_client: DockerClient,
    docker_compose_secure_list: List[Path],
    docker_registry_auth_header_list: List[Dict[str, str]],
    docker_registry_cacerts_list: List[Path],
    docker_registry_certs_list: List[DockerRegistryCerts],
    docker_registry_htpasswd_list: List[Path],
    docker_registry_password_list: List[str],
    docker_registry_ssl_context_list: List[SSLContext],
    docker_registry_username_list: List[str],
    docker_services: Services,
    pdrf_scale_factor: int,
    request,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[DockerRegistrySecure], None, None]:
    """Provides the endpoint of a local, mutable, secure, docker registry."""
    yield from _docker_registry_secure(
        docker_client=docker_client,
        docker_compose_secure_list=docker_compose_secure_list,
        docker_registry_auth_header_list=docker_registry_auth_header_list,
        docker_registry_cacerts_list=docker_registry_cacerts_list,
        docker_registry_certs_list=docker_registry_certs_list,
        docker_registry_htpasswd_list=docker_registry_htpasswd_list,
        docker_registry_password_list=docker_registry_password_list,
        docker_registry_ssl_context_list=docker_registry_ssl_context_list,
        docker_registry_username_list=docker_registry_username_list,
        docker_services=docker_services,
        request=request,
        scale_factor=pdrf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _docker_registry_ssl_context(
    *, docker_registry_cacerts_list: List[Path], scale_factor: int
) -> List[SSLContext]:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure docker registry service.
    """
    cache_key = _docker_registry_ssl_context.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(
            create_default_context(cafile=str(docker_registry_cacerts_list[i]))
        )
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def docker_registry_ssl_context(docker_registry_cacerts: Path) -> SSLContext:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure docker registry service.
    """
    return _docker_registry_ssl_context(
        docker_registry_cacerts_list=[docker_registry_cacerts], scale_factor=1
    )[0]


@pytest.fixture(scope="session")
def docker_registry_ssl_context_list(
    docker_registry_cacerts_list: List[Path],
    pdrf_scale_factor: int,
) -> List[SSLContext]:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure docker registry service.
    """
    return _docker_registry_ssl_context(
        docker_registry_cacerts_list=docker_registry_cacerts_list,
        scale_factor=pdrf_scale_factor,
    )


def _docker_registry_username(*, scale_factor: int) -> List[str]:
    """Retrieve the name of the user to use for authentication to the secure registry service."""
    cache_key = _docker_registry_username.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(f"pytest.username.{time()}")
        sleep(0.05)
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def docker_registry_username() -> str:
    """Retrieve the name of the user to use for authentication to the secure registry service."""
    return _docker_registry_username(scale_factor=1)[0]


@pytest.fixture(scope="session")
def docker_registry_username_list(
    pdrf_scale_factor: int,
) -> List[str]:
    """Retrieve the name of the user to use for authentication to the secure registry service."""
    return _docker_registry_username(scale_factor=pdrf_scale_factor)


@pytest.fixture(scope="session")
def pdrf_scale_factor() -> int:
    """Provides the number enumerated instances to be instantiated."""
    return 1


def _replicate_images(
    docker_client: DockerClient, endpoint: str, request
) -> List[ImageName]:
    """
    Replicates all marked images to a docker registry service at a given endpoint.

    Args:
        docker_client: Docker client with which to replicate the marked images.
        endpoint: The endpoint of the docker registry service.
        request: The pytest requests object from which to retrieve the marks.

    Returns: The list of images that were replicated.
    """
    always_pull = strtobool(str(request.config.getoption("--always-pull", True)))
    images = request.config.getoption("--push-image", [])
    # images.extend(request.node.get_closest_marker("push_image", []))

    # * Split ',' separated lists
    # * Remove duplicates - see conftest.py::pytest_collection_modifyitems()
    images = [image for i in images for image in i.split(",")]
    images = [ImageName.parse(image) for image in list(set(images))]
    for image in images:
        LOGGER.debug("- %s", image)
        try:
            replicate_image(docker_client, image, endpoint, always_pull=always_pull)
        except Exception as exception:  # pylint: disable=broad-except
            LOGGER.warning(
                "Unable to replicate image '%s': %s", image, exception, exc_info=True
            )
    return images
