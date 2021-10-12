import os
from invoke import task
from .config import *
from .colors import *
from os import listdir
from pathlib import Path


def build_python_server_stubs(config, yml_path, service_name):
    print_blue(f"Build python fast api server stub for: {yml_path}")
    print_blue(f"Generated service name: {service_name}")
    try:
        output_path = os.path.join(SERVER_STUBS_BASE_OUTPUT_PATH, service_name, 'python')
        cmd = f"./tools/openapi-generator-cli generate -i {yml_path}" \
              f" -g python-fastapi" \
              f" --additional-properties=packageName={service_name},packageVersion={PACKAGE_VERSION},serverPort=5680" \
              f" -t openapi/templates/python-fastapi/" \
              f" -o {output_path}"
        print(cmd)
        config.run(cmd)
        print_green("Build python fast api server stub - DONE")
        return True

    except Exception as e:
        print_red("Build python fast api server stub - FAIL")
        print_red(e)
        raise e


def build_python_client(config, yml_path, service_name):
    try:
        print_blue("Build python client stub")
        output_path = os.path.join(CLIENT_BASE_OUTPUT_PATH, service_name, 'python')
        cmd = f"./tools/openapi-generator-cli generate -i {yml_path}" \
              f" -g python-legacy --additional-properties=packageName={service_name},packageVersion={PACKAGE_VERSION}" \
              f" --library asyncio" \
              f" -o {output_path}"
        print(cmd)
        config.run(cmd)
        print_green("Build python client - DONE")
        return True
    except Exception as e:
        print_red("Build python client - FAIL")
        print_red(e)
        raise e


def copy_implementation_to_generated(config, service_name):
    print_blue(f"Copy implementations fro service: {service_name}")
    src_path = f"./impl/{service_name}"
    dst_path = os.path.join(SERVER_STUBS_BASE_OUTPUT_PATH, service_name, 'python', 'src',
                            service_name)
    try:
        if not Path(src_path).exists():
            return
        print_blue("Copy implementation to generated folder")
        cmd = f"cp -rf {os.path.join(src_path, '*')} {dst_path}"
        config.run(cmd)
        print_green("Copy implementation to generated folder - DONE")
    except Exception as e:
        print_red("Copy implementation to generated folder - FAIL")
        print_red(e)
        raise e


@task()
def inc_sub_version(config):
    print_blue("Inc package subversion")
    print(f"Current version {PACKAGE_VERSION}")
    version = [int(i) for i in PACKAGE_VERSION.split('.')]
    version[-1] += 1
    version_str = ".".join([str(i) for i in version])
    config.run(f"cat config.py | sed 's/PACKAGE_VERSION.*/PACKAGE_VERSION = \"{version_str}\"/g' > config.py.upd")
    config.run("mv config.py.upd config.py")


def build_python_client_release(config, service_name='simple_storage'):
    client_path = os.path.join(CLIENT_BASE_OUTPUT_PATH, service_name, 'python')
    print(client_path)
    config.run(f"tar -czvf simple_storage_client_{PACKAGE_VERSION}.tar.gz --directory={client_path}/ .")


def build_python_stub_release(config, service_name='simple_storage'):
    client_path = os.path.join(SERVER_STUBS_BASE_OUTPUT_PATH, service_name, 'python')
    print(client_path)
    config.run(f"tar -czvf simple_storage_server_{PACKAGE_VERSION}.tar.gz --directory={client_path}/ .")


@task()
def build_releases(config):
    build_python_client_release(config, service_name='simple_storage')
    build_python_stub_release(config, service_name='simple_storage')


@task()
def build(config):
    """ Build openapi package """

    yml_files = [f for f in listdir(OPENAPI_DEFINITION_PATH) if f.endswith('.yml')]
    print_blue("Found next yml files: {yml_files}")
    for f in yml_files:
        service_name = f.replace(".yml", "")
        build_python_server_stubs(config=config, yml_path=os.path.join(OPENAPI_DEFINITION_PATH, f),
                                  service_name=service_name)
        copy_implementation_to_generated(config, service_name=service_name)
        build_python_client(config=config, yml_path=os.path.join(OPENAPI_DEFINITION_PATH, f),
                            service_name=service_name)
    print_green("Build openapi package - DONE")


@task()
def clean(config):
    """ Remove all built openapi packages"""
    config.run(f"rm -rf {SERVER_STUBS_BASE_OUTPUT_PATH}")
    config.run(f"rm -rf {CLIENT_BASE_OUTPUT_PATH}")
    print_green("Openapi package remove - DONE")
