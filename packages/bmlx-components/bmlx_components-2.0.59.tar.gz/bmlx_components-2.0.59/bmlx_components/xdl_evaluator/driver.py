import os
from bmlx.utils import artifact_utils, io_utils
from bmlx_components.proto import model_pb2
from bmlx_components.xdl_base.driver import XdlDriver


class XdlEvaluatorDriver(XdlDriver):
    # override super method
    def _rewrite_launch_config(self, exec_properties):
        pass

    def _resolve_model_paths(self, input_dict, exec_properties):
        model_uri = ""
        if "model" in input_dict:
            if len(input_dict["model"]) > 0:
                model_uri = artifact_utils.get_single_uri(input_dict["model"])
        if not model_uri:
            return ("", "")

        if "model_file_pattern" not in exec_properties:
            raise RuntimeError("model file pattern must set")

        if io_utils.exists(os.path.join(model_uri, "model.pbtxt")):
            model_pb = io_utils.parse_pbtxt_file(
                os.path.join(model_uri, "model.pbtxt"), model_pb2.Model()
            )
            model_uri = os.path.join(
                model_pb.model_path, model_pb.model_version
            )

        model_bank_uri = self._get_model_bank_uri(
            model_uri, exec_properties["model_file_pattern"]
        )
        # eval 阶段内存优化，强制只加载phase0 的 embedding 数据
        # TDOO: find a better way to handle model bank uri for different job types
        model_bank_uri = (
            "re#phase0.*,xdl_global_step@" + model_bank_uri.split("@")[1]
        )
        if exec_properties["is_local"]:
            return model_bank_uri, model_uri
        else:
            return model_bank_uri, exec_properties.get("model_uri_base", "")
