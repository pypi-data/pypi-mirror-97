def make_required_install_packages():
    return [
        "click==7.0",
        "protobuf>=3.12,<4",
        "pyyaml>=5.1",
        "six>=1.10,<2",
        "docker>=4,<5",
        "versioneer==0.18",
        "kubernetes==11.0.0",
        "pyarrow==0.16.0",
        "urllib3<1.25,>=1.15",
        "bs4>=0.0.1",
        "tabulate==0.8.3",
        "pip-api==0.0.14",
        "pre-commit==2.4.0",
        "psutil==5.7.2",
        "boto3==1.14.52",
        "pytz==2020.1",
        # metadata package
        "ml-metadata==0.25.0",
        # api-server package
        "bmlx-openapi-client==0.0.79.1",
    ]


def make_required_test_packages():
    """Prepare extra packages needed for 'python setup.py test'."""
    return [
        "click==7.0",
        "protobuf>=3.12,<4",
        "pyyaml>=5.1",
        "six>=1.10,<2",
        "docker>=4,<5",
        "versioneer==0.18",
        "kubernetes==11.0.0",
        "pyarrow==0.16.0",
        "urllib3<1.25,>=1.15",
        "pytz==2020.1",
        "bmlx-openapi-client>=0.0.64",
    ]


def make_extra_packages_docker_image():
    return [
        "python-snappy>=0.5,<0.6",
    ]


def make_all_dependency_packages():
    return make_required_test_packages() + make_extra_packages_docker_image()
