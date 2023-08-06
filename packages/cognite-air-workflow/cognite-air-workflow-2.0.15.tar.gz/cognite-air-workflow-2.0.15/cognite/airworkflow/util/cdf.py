import os
import shutil
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from cognite.client import CogniteClient
from cognite.experimental import CogniteClient as ExperimentalClient

from cognite.airworkflow.constants import PROJECTS_TO_API_KEYS

os.environ["COGNITE_MAX_RETRIES"] = "5"
os.environ["COGNITE_TIMEOUT"] = "120"


def data_set_id(client: CogniteClient, name: str) -> int:
    data_sets = client.data_sets.list(limit=-1).dump()
    for ds in data_sets:
        if "name" in ds:
            if ("archived" not in ds["metadata"] or ds["metadata"]["archived"] != "true") and ds["name"] == name:
                return ds["id"]
    raise LookupError(f"Not able to find dataset named {name}")


def zip_and_upload(client: CogniteClient, code_path: Path, file_name: str, data_set_name: str) -> int:
    print(f"Uploading code from {code_path} ... ", flush=True)
    with TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / "function"
        shutil.make_archive(str(zip_path), "zip", str(code_path))
        id = data_set_id(client, data_set_name)
        file = client.files.upload(
            f"{zip_path}.zip",
            name=f"{file_name}.zip",
            external_id=f"{file_name}.zip",
            overwrite=True,
            data_set_id=id,
        )
        counter = 0
        while client.files.retrieve(file.id) is None:
            time.sleep(0.5)
            counter += 1
            if counter > 5:
                break
        print(f"Upload complete. \n{file}", flush=True)
        return file.id


def does_function_exist(client: ExperimentalClient, function_name: str) -> bool:
    return bool(client.functions.retrieve(external_id=function_name))


def await_function_deployment(client: ExperimentalClient, function_name: str, max_wait: int) -> bool:
    t_end = time.time() + max_wait
    while time.time() < t_end:
        function = client.functions.retrieve(external_id=function_name)
        print(f"Function status {function.status}")
        if function.status == "Ready":
            return True
        if function.status == "Failed":
            return False
        time.sleep(5.0)

    return False


def experimental_client(project: str, api_key: str = "", base_url: str = None) -> ExperimentalClient:
    return ExperimentalClient(
        api_key=api_key if api_key else PROJECTS_TO_API_KEYS[project].get_client_api_key(),
        client_name="AIR Functions Client",
        project=project,
        base_url=base_url if base_url else PROJECTS_TO_API_KEYS[project].base_url,
    )
