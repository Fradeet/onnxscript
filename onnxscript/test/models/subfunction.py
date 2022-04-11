# SPDX-License-Identifier: Apache-2.0

from onnxscript import script
from onnxscript.onnx_types import FLOAT
from onnxscript.values import CustomOpset
from onnxscript.onnx import opset15 as op


@script(CustomOpset('this', 1))
def MySelu(X: FLOAT[None], alpha: FLOAT[1], gamma: FLOAT[1]) -> FLOAT[None]:
    neg = gamma * (alpha * op.Exp(X) - alpha)
    pos = gamma * X
    return op.Where(X <= 0., neg, pos)

@script(CustomOpset('this', 1))
def MyElu(X: FLOAT[None], beta: FLOAT[1]) -> FLOAT[None]:
    alpha = op.Constant(value_float=1.)
    return MySelu(X, alpha, beta)

@script(CustomOpset('this', 1))
def MyEluB(X: FLOAT[None], beta: FLOAT[1]) -> FLOAT[None]:
    alpha = op.Constant(value_float=1.)
    res = MySelu(X, alpha, beta)
    return res

@script(CustomOpset('this', 1))
def MyEluC(X: FLOAT[None], beta: FLOAT[1]) -> FLOAT[None]:
    alpha = op.Constant(value_float=1.)
    res = op.Identity(MySelu(X, alpha, beta))
    return res

@script(CustomOpset('this', 1))
def IfMyEluD(X: FLOAT[None], beta: FLOAT[1]) -> FLOAT[None]:
    zero = op.Constant(value_float=1.)
    if beta > 0:
        result = MyEluB(X, beta)
    else:
        result = MyEluC(X, beta)
    return result
