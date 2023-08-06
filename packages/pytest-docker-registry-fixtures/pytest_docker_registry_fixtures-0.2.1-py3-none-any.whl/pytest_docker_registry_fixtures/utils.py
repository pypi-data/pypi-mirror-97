#!/usr/bin/env python

"""Utility classes."""

import logging

from http.client import HTTPSConnection
from importlib.resources import read_text
from pathlib import Path
from random import randrange
from shutil import copyfile
from socket import getfqdn
from ssl import SSLContext
from time import time
from typing import Dict, Generator, List, NamedTuple

import bcrypt

from certifi import where
from docker import DockerClient
from docker.errors import ImageNotFound
from OpenSSL import crypto
from _pytest.tmpdir import TempPathFactory
from lovely.pytest.docker.compose import Services

from .imagename import ImageName

LOGGER = logging.getLogger(__name__)

DOCKER_REGISTRY_SERVICE = "pytest-docker-registry"
DOCKER_REGISTRY_SERVICE_PATTERN = f"{DOCKER_REGISTRY_SERVICE}-{{0}}-{{1}}"


class CertificateKeypair(NamedTuple):
    # pylint: disable=missing-class-docstring
    ca_certificate: bytes
    ca_private_key: bytes
    certificate: bytes
    private_key: bytes


def check_url_secure(
    docker_ip: str,
    public_port: int,
    *,
    auth_header: Dict[str, str],
    ssl_context: SSLContext,
) -> bool:
    """
    Secure form of lovey/pytest/docker/compose.py::check_url() that checks when the secure docker registry service is
    operational.

    Args:
        docker_ip: IP address on which the service is exposed.
        public_port: Port on which the service is exposed.
        auth_header: HTTP basic authentication header to using when connecting to the service.
        ssl_context:
            SSL context referencing the trusted root CA certificated to used when negotiating the TLS connection.

    Returns:
        (bool) True when the service is operational, False otherwise.
    """
    try:
        https_connection = HTTPSConnection(
            context=ssl_context, host=docker_ip, port=public_port
        )
        https_connection.request("HEAD", "/v2/", headers=auth_header)
        return https_connection.getresponse().status < 500
    except Exception:  # pylint: disable=broad-except
        return False


def generate_cacerts(
    tmp_path_factory: TempPathFactory,
    *,
    certificate: Path,
    delete_after: bool = True,
) -> Generator[Path, None, None]:
    """
    Generates a temporary CA certificate trust store containing a given certificate.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        certificate: Path to the certificate to be included in the trust store.
        delete_after: If True, the temporary file will be removed after the iteration is complete.

    Yields:
        The path to the temporary file.
    """
    # Note: where() path cannot be trusted to be temporary, don't pollute persistent files ...
    name = DOCKER_REGISTRY_SERVICE_PATTERN.format("cacerts", "x")
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath(name)
    copyfile(where(), tmp_path)

    with certificate.open("r") as file_in:
        with tmp_path.open("w") as file_out:
            file_out.write(file_in.read())
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def generate_htpasswd(
    tmp_path_factory: TempPathFactory,
    *,
    delete_after: bool = True,
    password: str,
    username: str,
) -> Generator[Path, None, None]:
    """
    Generates a temporary htpasswd containing a given set of credentials.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        delete_after: If True, the temporary file will be removed after the iteration is complete.
        password: The password corresponding to the provided user name.
        username: The name of the user to include in the htpasswd file.

    Yields:
        The path to the temporary file.
    """
    hashpw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath("htpasswd")
    with tmp_path.open("w") as file:
        file.write(f"{username}:{hashpw}")
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def generate_keypair(
    *, keysize: int = 4096, life_cycle: int = 7 * 24 * 60 * 60
) -> CertificateKeypair:
    """
    Generates a keypair and certificate for the registry service.

    Args:
        keysize: size of the private key.
        life_cycle: Lifespan of the generated certificates, in seconds.

    Returns:
        tuple:
            certificate: The public certificate.
            private_key: The private key.
    """

    # Generate a self-signed certificate authority ...
    pkey_ca = crypto.PKey()
    pkey_ca.generate_key(crypto.TYPE_RSA, keysize)

    x509_ca = crypto.X509()
    x509_ca.get_subject().commonName = f"pytest-docker-registry-fixtures-ca-{time()}"
    x509_ca.gmtime_adj_notBefore(0)
    x509_ca.gmtime_adj_notAfter(life_cycle)
    x509_ca.set_issuer(x509_ca.get_subject())
    x509_ca.set_pubkey(pkey_ca)
    x509_ca.set_serial_number(randrange(100000))
    x509_ca.set_version(2)

    x509_ca.add_extensions(
        [crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=x509_ca)]
    )
    x509_ca.add_extensions(
        [
            crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE"),
            crypto.X509Extension(
                b"authorityKeyIdentifier", False, b"keyid:always", issuer=x509_ca
            ),
            crypto.X509Extension(
                b"keyUsage", True, b"digitalSignature, keyCertSign, cRLSign"
            ),
        ]
    )

    x509_ca.sign(pkey_ca, "sha256")

    # Generate a certificate ...
    pkey_cert = crypto.PKey()
    pkey_cert.generate_key(crypto.TYPE_RSA, keysize)

    x509_cert = crypto.X509()
    x509_cert.get_subject().commonName = getfqdn()
    x509_cert.gmtime_adj_notBefore(0)
    x509_cert.gmtime_adj_notAfter(life_cycle)
    x509_cert.set_issuer(x509_ca.get_subject())
    x509_cert.set_pubkey(pkey_cert)
    x509_cert.set_serial_number(randrange(100000))
    x509_cert.set_version(2)

    x509_cert.add_extensions(
        [
            crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
            crypto.X509Extension(b"extendedKeyUsage", False, b"serverAuth, clientAuth"),
            crypto.X509Extension(
                b"subjectAltName",
                False,
                ",".join(
                    [
                        f"DNS:{getfqdn()}",
                        f"DNS:*.{getfqdn()}",
                        "DNS:localhost",
                        "DNS:*.localhost",
                        "IP:127.0.0.1",
                    ]
                ).encode("utf-8"),
            ),
        ]
    )

    x509_cert.sign(pkey_ca, "sha256")

    return CertificateKeypair(
        ca_certificate=crypto.dump_certificate(crypto.FILETYPE_PEM, x509_ca),
        ca_private_key=crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey_ca),
        certificate=crypto.dump_certificate(crypto.FILETYPE_PEM, x509_cert),
        private_key=crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey_cert),
    )


def get_docker_compose_user_defined(
    docker_compose_files: List[str], service_name: str
) -> Generator[Path, None, None]:
    """
    Tests to see if a user-defined configuration exists, and contains the docker registry service name.

    Args:
        docker_compose_files: List of docker-compose.yml locations.
        service_name: Name of the docker registry service.

    Yields:
        The path to a user-defined docker-compose.yml file that contains the service.
    """
    for docker_compose_file in [Path(x) for x in docker_compose_files]:
        try:
            if f"{service_name}:" in docker_compose_file.read_text():
                yield docker_compose_file
        except (FileNotFoundError, IOError):
            ...


def get_embedded_file(
    tmp_path_factory: TempPathFactory, *, delete_after: bool = True, name: str
) -> Generator[Path, None, None]:
    """
    Replicates a file embedded within this package to a temporary file.

    Args:
        tmp_path_factory: Factory to use when generating temporary paths.
        delete_after: If True, the temporary file will be removed after the iteration is complete.
        name: The name of the embedded file to be replicated.

    Yields:
        The path to the temporary file.
    """
    tmp_path = tmp_path_factory.mktemp(__name__).joinpath(name)
    with tmp_path.open("w") as file:
        file.write(read_text(__package__, name))
    yield tmp_path
    if delete_after:
        tmp_path.unlink(missing_ok=True)


def get_pushed_images(request):
    """
    Retrieves the list of 'push_image' pytest marks from a given request.

    Args:
        request: The pytest request from which to retrieve the marks.

    Returns:
        The list of pushed images.
    """
    mark = request.node.get_closest_marker("push_image")
    return mark.args if mark else []


def get_user_defined_file(pytestconfig: "_pytest.config.Config", name: str):
    """
    Tests to see if a user-defined file exists.

    Args:
        pytestconfig: pytest configuration file to use when locating the user-defined file.
        name: Name of the user-defined file.

    Yields:
        The path to the user-defined file.
    """
    user_defined = Path(str(pytestconfig.rootdir), "tests", name)
    if user_defined.exists():
        yield user_defined


def replicate_image(
    docker_client: DockerClient,
    image: ImageName,
    endpoint: str,
    *,
    always_pull: bool = True,
    delete_after: bool = True,
):
    """
    Replicates a docker image into a docker registry at a given endpoint.

    Args:
        docker_client: The Docker client to use to replicate the image.
        image: The name of the docker image to be replicated.
        endpoint: Endpoint of the docker registry into which to replicate the image.
        always_pull:
            If True, an image will be pulled prior to replication. Otherwise, the pull will be skipped if the image is
            cached locally.
        delete_after: If True, the pushed image will be remove from the intermediary host.
    """
    # Tag needs to be populated or SDK will download multiple images
    if not image.digest and not image.tag:
        image.tag = "latest"

    img = None
    try:
        img = docker_client.images.get(str(image))
    except ImageNotFound:
        ...
    if always_pull or not img:
        img = docker_client.images.pull(str(image))

    destination = image.clone()
    destination.endpoint = endpoint
    # TODO: The Docker SDK doesn't appear to be able to push manifests by digest (refusing to create a tag with a digest
    #       reference) ...
    if destination.digest:
        destination.digest = None
    if not destination.tag:
        destination.tag = "pytest-docker-registry-fixtures"
    img.tag(str(destination))
    docker_client.images.push(str(destination))

    if always_pull and delete_after:
        docker_client.images.remove(image=str(image))


def replicate_manifest_list(
    image: ImageName,
    endpoint: str,
    *,
    auth_header_dest: Dict[str, str] = None,
    auth_header_src: Dict[str, str] = None,
    ssl_context_dest: SSLContext = None,
    ssl_context_src: SSLContext = None,
):
    """
    Helper function as docker-py cannot operate on manifest lists.

    Args:
        image: The name of the docker image to be replicated.
        endpoint: Endpoint of the docker registry into which to replicate the image.
        auth_header_dest: HTTP basic authentication header to using when connecting to the service.
        auth_header_src: HTTP basic authentication header to using when connecting to the service.
        ssl_context_dest:
            SSL context referencing the trusted root CA certificated to used when negotiating the TLS connection.
        ssl_context_src:
            SSL context referencing the trusted root CA certificated to used when negotiating the TLS connection.
    """
    media_type = "application/vnd.docker.distribution.manifest.list.v2+json"

    # Note: This cannot be imported above, as it causes a circular import!
    from . import __version__  # pylint: disable=import-outside-toplevel

    user_agent = f"pytest-docker-registry-fixtures/{__version__}"

    https_connection = HTTPSConnection(context=ssl_context_src, host=image.endpoint)
    identifier = image.digest if image.digest else image.tag  # Prefer digest
    https_connection.request(
        "GET",
        url=f"/v2/{image.image}/manifests/{identifier}",
        headers={"Accept": media_type, "User-Agent": user_agent, **auth_header_src},
    )
    response = https_connection.getresponse()
    assert response.status == 200
    assert response.headers["Content-Type"] == media_type
    if image.digest:
        assert response.headers["Docker-Content-Digest"] == image.digest
    manifest = response.read()

    https_connection = HTTPSConnection(context=ssl_context_dest, host=endpoint)
    identifier = image.tag if image.tag else image.digest  # Prefer tag
    https_connection.request(
        "PUT",
        url=f"/v2/{image.image}/manifests/{identifier}",
        headers={
            "Content-Type": media_type,
            "User-Agent": user_agent,
            **auth_header_dest,
        },
        body=manifest,
    )
    assert https_connection.getresponse().status == 201


def start_service(
    docker_services: Services, *, docker_compose: Path, service_name: str, **kwargs
):
    # pylint: disable=protected-access
    """
    Instantiates a given service using docker-compose.

    Args:
        docker_services: lovely service to use to start the service.
        docker_compose: Path to the docker-compose configuration file (to be injected).
        service_name: Name of the service, within the docker-compose configuration, to be instantiated.
    """
    # DUCK PUNCH: Don't get in the way of user-defined lovey/pytest/docker/compose.py::docker_compose_files()
    #             overrides ...
    docker_services._docker_compose._compose_files = [
        str(docker_compose)
    ]  # pylint: disable=protected-access
    docker_services.start(service_name)
    public_port = docker_services.wait_for_service(service_name, 5000, **kwargs)
    return f"{docker_services.docker_ip}:{public_port}"
