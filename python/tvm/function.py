from __future__ import absolute_import as _abs
from numbers import Number as _Number, Integral as _Integral
from ._ctypes._api import _init_function_module
from . import _function_internal
from . import make as _make
from . import expr as _expr
from . import collections as _collections

int32 = "int32"
float32 = "float32"

def const(value, dtype=None):
    """construct a constant"""
    if dtype is None:
        if isinstance(value, _Integral):
            dtype = 'int32'
        else:
            dtype = 'float32'
    return _function_internal._const(value, dtype)


def Var(name="tindex", dtype=int32):
    """Create a new variable with specified name and dtype

    Parameters
    ----------
    name : str
        The name

    dtype : int
        The data type
    """
    return _function_internal._Var(name, dtype)


def convert(value):
    """Convert a value to expression."""
    if isinstance(value, _Number):
        return const(value)
    elif isinstance(value, (list, tuple)):
        value = [convert(x) for x in value]
        return _function_internal._Array(*value)
    else:
        return value


def Tensor(shape, fcompute=None, dtype=None, name="TensorObj"):
    """Construct a tensor object in dataflow.

    Parameters
    ----------
    shape: Tuple of Expr
        The shape of the tensor

    fcompute: lambda function of *indices-> value
        Specifies the input source expression

    dtype: str, optional
        The data type of the tensor, must specify when fcompute is not specified.

    name: str, optional
        The name hint of the tensor

    Returns
    -------
    tensor: tensor.Tensor
        The created tensor
    """
    ndim = len(shape)
    dim_var = [Var("dim_var%d" % i) for i in range(ndim)]
    if fcompute:
        source = fcompute(*dim_var)
        return _function_internal._Tensor(
            shape, name, source.dtype, dim_var, source)
    else:
        dtype = float32 if dtype is None else dtype
        return _function_internal._Tensor(
            shape, name, dtype, None, None)


def RDomain(dom):
    """Create a reduction domain given domain

    Parameters
    ----------
    dom : list of Range or list of pairs
       The reduction domain.

    Returns
    -------
    rdom : RDomain
       The result rdomain
    """
    if not isinstance(dom, (list, tuple)):
        dom = [dom]
    elif not isinstance(dom[0], (list, tuple)):
        dom = [dom]
    dnorm = []
    for x in dom:
        if isinstance(x, (list, tuple)):
            if len(x) != 2:
                raise ValueError("need to list of ranges")
            dnorm.append(Range(x[0], x[1]))
        else:
            dnorm.append(x)
    dnorm = convert(dnorm)
    return _function_internal._RDomain(dnorm)


def sum(expr, rdom):
    """Create a sum expression over rdom

    Parameters
    ----------
    expr : Expr
        The source expression.

    rdom : RDomain
        The reduction domainx
    """
    assert isinstance(rdom, _collections.RDomain)
    x =  _make.Reduce("Add", expr, rdom)
    return x

def sum(expr, rdom):
    """Create a sum expression over rdom

    Parameters
    ----------
    expr : Expr
        The source expression.

    rdom : RDomain
        The reduction domainx
    """
    assert isinstance(expr, _expr.Expr)
    assert isinstance(rdom, _collections.RDomain)
    x =  _make.Reduce("Add", expr, rdom)
    return x

def min(expr, rdom):
    """Create a min expression over rdom

    Parameters
    ----------
    expr : Expr
        The source expression.

    rdom : RDomain
        The reduction domainx
    """
    assert isinstance(expr, _expr.Expr)
    assert isinstance(rdom, _collections.RDomain)
    x =  _make.Reduce("Min", expr, rdom)
    return x


def max(expr, rdom):
    """Create a min expression over rdom

    Parameters
    ----------
    expr : Expr
        The source expression.

    rdom : RDomain
        The reduction domainx
    """
    assert isinstance(expr, _expr.Expr)
    assert isinstance(rdom, _collections.RDomain)
    x =  _make.Reduce("Max", expr, rdom)
    return x


_init_function_module("tvm")