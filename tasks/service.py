import os
from invoke import task
from .config import *


@task()
def simple_storage_run(conf):
    """Run simple storage service"""
    service_name = 'simple_storage'
    cmd = f"cd {os.path.join(SERVER_STUBS_BASE_OUTPUT_PATH, service_name, 'python', 'src')} && uvicorn simple_storage.main:app --host 0.0.0.0 --port 8080"
    conf.run(cmd)
