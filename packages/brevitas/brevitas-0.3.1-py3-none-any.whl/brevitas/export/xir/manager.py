from brevitas.export.base import BaseManager
from brevitas.export.onnx.base import ONNXBaseManager
from brevitas.export.onnx.pyxir.dpuv1.handler import DPUv1QuantConv2dHandler, DPUv1QuantMaxPool2dHandler
from brevitas.export.onnx.pyxir.handler import DPUQuantEltwiseAddHandler, DPUQuantReLUHandler
from brevitas.export.onnx.pyxir.handler import DPUQuantAvgPool2dHandler, DPUQuantLinearHandler


def onnx_conv_to_xir():
    pass


class XIRManager(ONNXBaseManager):

    handlers = [
        DPUv1QuantConv2dHandler,
        DPUQuantReLUHandler,
        DPUQuantEltwiseAddHandler,
        DPUQuantAvgPool2dHandler,
        DPUQuantLinearHandler,
        DPUv1QuantMaxPool2dHandler]

    onnx_passes = [
        "extract_constant_to_initializer",
        # remove unused graph inputs & initializers
        "eliminate_unused_initializer"]

    # @classmethod
    # def export_onnx(
    #         cls,
    #         module: Module,
    #         input_shape: Tuple[int, ...],
    #         export_path: str,
    #         input_t: Optional[Union[Tensor, QuantTensor]] = None,
    #         **kwargs):