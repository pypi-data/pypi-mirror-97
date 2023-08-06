import typing
import tempfile
import os
from os import path

from typing import Optional, Callable, Any, Dict, get_type_hints, Tuple, List

from tempo.serve.loader import (
    download,
    upload,
    load_custom,
    save_custom,
    save_environment,
)
from tempo.serve.runtime import Runtime

from tempo.serve.constants import (
    ModelDataType,
    DefaultModelFilename,
    DefaultEnvFilename,
)
from tempo.serve.metadata import (
    ModelDetails,
    ModelDataArgs,
    ModelDataArg,
    ModelFramework,
)

DEFAULT_CONDA_FILE = "conda.yaml"

class BaseModel:
    def __init__(
        self,
        name: str,
        user_func: Callable[[Any], Any] = None,
        local_folder: str = None,
        uri: str = None,
        platform: ModelFramework = None,
        inputs: ModelDataType = None,
        outputs: ModelDataType = None,
        conda_env: str = None,
        runtime: Runtime = None,
    ):
        self._name = name
        self._user_func = user_func
        self.conda_env_name = conda_env
        if uri is None:
            uri = ""

        local_folder = self._get_local_folder(local_folder)
        inputs, outputs = self._get_args(inputs, outputs)

        self.details = ModelDetails(
            name=name,
            local_folder=local_folder,
            uri=uri,
            platform=platform,
            inputs=inputs,
            outputs=outputs,
        )

        self.cls = None
        self.runtime = runtime

    def _get_args(
        self, inputs: ModelDataType = None, outputs: ModelDataType = None
    ) -> Tuple[ModelDataArgs, ModelDataArgs]:
        input_args = []
        output_args = []

        if inputs is None and outputs is None:
            if self._user_func is not None:
                hints = get_type_hints(self._user_func)
                for k, v in hints.items():
                    if k == "return":
                        if isinstance(v, typing._GenericAlias):
                            targs = v.__args__
                            for targ in targs:
                                output_args.append(ModelDataArg(ty=targ))
                        else:
                            output_args.append(ModelDataArg(ty=v))
                    else:
                        input_args.append(ModelDataArg(name=k, ty=v))
        else:
            if type(outputs) == Dict:
                for k, v in outputs.items():
                    output_args.append(ModelDataArg(name=k, ty=v))
            elif type(outputs) == Tuple:
                for ty in list(outputs):
                    output_args.append(ModelDataArg(ty=ty))
            else:
                output_args.append(ModelDataArg(ty=outputs))

            if type(inputs) == Dict:
                for k, v in inputs.items():
                    input_args.append(ModelDataArg(name=k, ty=v))
            elif type(inputs) == Tuple:
                for ty in list(inputs):
                    input_args.append(ModelDataArg(ty=ty))
            else:
                input_args.append(ModelDataArg(ty=inputs))

        return ModelDataArgs(args=input_args), ModelDataArgs(args=output_args)

    def _get_local_folder(self, local_folder: str = None) -> Optional[str]:
        if not local_folder:
            # TODO: Should we do cleanup at some point?
            local_folder = tempfile.mkdtemp()

        return local_folder

    def set_cls(self, cls):
        self.cls = cls

    @classmethod
    def load(cls, folder: str) -> "BaseModel":
        file_path_pkl = os.path.join(folder, DefaultModelFilename)
        return load_custom(file_path_pkl)

    def save(self, save_env=True):
        if not self._user_func:
            # Nothing to save
            return

        file_path_pkl = os.path.join(self.details.local_folder, DefaultModelFilename)
        save_custom(self, file_path_pkl)

        if save_env:
            file_path_env = os.path.join(self.details.local_folder, DefaultEnvFilename)
            conda_env_file_path = path.join(self.details.local_folder,DEFAULT_CONDA_FILE)
            if not path.exists(conda_env_file_path):
                conda_env_file_path = None

            save_environment(conda_pack_file_path=file_path_env, conda_env_file_path=conda_env_file_path, env_name=self.conda_env_name)

    def upload(self):
        """
        Upload from local folder to uri
        """
        upload(self.details.local_folder, self.details.uri)

    def download(self):
        """
        Download from uri to local folder
        """
        # TODO: This doesn't make sense for custom methods?
        download(self.details.uri, self.details.local_folder)

    def request(self, req: Dict) -> Dict:
        if self.runtime is None:
            raise ValueError("Runtime most not be none to handle a request")
        protocol = self.runtime.get_protocol()
        req_converted = protocol.from_protocol_request(req, self.details.inputs)
        if type(req_converted) == dict:
            if self.cls is not None:
                response = self._user_func(self.cls, **req_converted)
            else:
                response = self._user_func(**req_converted)
        elif type(req_converted) == list or type(req_converted) == tuple:
            if self.cls is not None:
                response = self._user_func(self.cls, *req_converted)
            else:
                response = self._user_func(*req_converted)
        else:
            if self.cls is not None:
                response = self._user_func(self.cls, req_converted)
            else:
                response = self._user_func(req_converted)

        if type(response) == dict:
            response_converted = protocol.to_protocol_response(self.details, **response)
        elif type(response) == list or type(response) == tuple:
            response_converted = protocol.to_protocol_response(self.details, *response)
        else:
            response_converted = protocol.to_protocol_response(self.details, response)
        return response_converted

    def set_runtime(self, runtime: Runtime):
        self.runtime = runtime

    def remote(self, *args, **kwargs):
        return self.runtime.remote(self.details, *args, **kwargs)

    def wait_ready(self, timeout_secs=None):
        return self.runtime.wait_ready(self.details, timeout_secs=timeout_secs)

    def get_endpoint(self):
        return self.runtime.get_endpoint(self.details)

    def to_k8s_yaml(self) -> str:
        """
        Get k8s yaml
        """
        return self.runtime.to_k8s_yaml(self.details)

    def deploy(self):
        self.runtime.deploy(self.details)

    def undeploy(self):
        self.runtime.undeploy(self.details)
