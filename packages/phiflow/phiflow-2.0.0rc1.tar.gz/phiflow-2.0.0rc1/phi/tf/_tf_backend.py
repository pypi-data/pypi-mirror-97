import numbers
import uuid
from contextlib import contextmanager
from functools import wraps
from typing import List, Tuple, Any, Callable

import numpy as np
import scipy.optimize as sopt
import tensorflow as tf
from tensorflow.python.client import device_lib

from phi.math.backend import Backend, DType, to_numpy_dtype, from_numpy_dtype, ComputeDevice, NUMPY_BACKEND
from ._tf_cuda_resample import resample_cuda, use_cuda
from ..math import LinearSolve
from ..math.backend._backend_helper import combined_dim
from ..math.backend._optim import SolveResult, Solve


class TFBackend(Backend):

    def __init__(self):
        Backend.__init__(self, "TensorFlow", default_device=None)

    def list_devices(self, device_type: str or None = None) -> List[ComputeDevice]:
        tf_devices = device_lib.list_local_devices()
        devices = []
        for device in tf_devices:
            if device_type in (None, device.device_type):
                devices.append(ComputeDevice(self, device.name, device.device_type, device.memory_limit,
                                             processor_count=-1,
                                             description=str(device),
                                             ref=device))
        return devices

    def is_tensor(self, x, only_native=False):
        if only_native:
            return tf.is_tensor(x)
        else:
            return tf.is_tensor(x) or NUMPY_BACKEND.is_tensor(x, only_native=False)

    def as_tensor(self, x, convert_external=True):
        if self.is_tensor(x, only_native=convert_external):
            tensor = x
        elif isinstance(x, np.ndarray):
            tensor = tf.convert_to_tensor(NUMPY_BACKEND.as_tensor(x))
        else:
            tensor = tf.convert_to_tensor(x)
        # --- Enforce Precision ---
        if not isinstance(tensor, numbers.Number):
            if isinstance(tensor, np.ndarray):
                tensor = NUMPY_BACKEND.as_tensor(tensor)
            elif tensor.dtype.is_floating:
                tensor = self.to_float(tensor)
        return tensor

    def is_available(self, tensor) -> bool:
        if self.is_tensor(tensor, only_native=True):
            return tf.executing_eagerly()
        else:
            return True

    def numpy(self, tensor):
        if tf.is_tensor(tensor):
            return tensor.numpy()
        return NUMPY_BACKEND.numpy(tensor)

    def copy(self, tensor, only_mutable=False):
        if not only_mutable or tf.executing_eagerly():
            return tf.identity(tensor)
        else:
            return tensor

    def jit_compile(self, f: Callable) -> Callable:
        return tf.function(f)

    def custom_gradient(self, f: Callable, gradient: Callable = None) -> Callable:
        @tf.custom_gradient
        def tf_function(*args, **kwargs):
            def grad(*grad_args):
                return gradient(*grad_args)
            return f(*args, **kwargs), grad
        return tf_function

    def transpose(self, tensor, axes):
        return tf.transpose(tensor, perm=axes)

    def equal(self, x, y):
        return tf.equal(x, y)

    def divide_no_nan(self, x, y):
        x, y = self.auto_cast(x, y)
        return tf.math.divide_no_nan(x, y)

    def random_uniform(self, shape):
        return tf.random.uniform(shape, dtype=to_numpy_dtype(self.float_type))

    def random_normal(self, shape):
        return tf.random.normal(shape, dtype=to_numpy_dtype(self.float_type))

    def rank(self, value):
        return len(value.shape)

    def range(self, start, limit=None, delta=1, dtype=None):
        return tf.range(start, limit, delta, dtype)

    def tile(self, value, multiples):
        if isinstance(multiples, (tuple, list)) and self.ndims(value) < len(multiples):
            value = self.expand_dims(value, axis=0, number=len(multiples) - self.ndims(value))
        return tf.tile(value, multiples)

    def stack(self, values, axis=0):
        return tf.stack(values, axis=axis)

    def concat(self, values, axis):
        return tf.concat(values, axis)

    def pad(self, value, pad_width, mode='constant', constant_values=0):
        if mode == 'boundary' and np.all(np.array(pad_width) <= 1):
            mode = 'symmetric'
        if mode in ('constant', 'symmetric', 'reflect'):
            return tf.pad(value, pad_width, mode.upper(), constant_values=constant_values)
        else:
            return NotImplemented

    def reshape(self, value, shape):
        return tf.reshape(value, shape)

    def sum(self, value, axis=None, keepdims=False):
        if axis is not None:
            if not isinstance(axis, int):
                axis = list(axis)
        if isinstance(value, tf.SparseTensor):
            return tf.sparse.reduce_sum(value, axis=axis, keepdims=keepdims, output_is_sparse=False)
        if isinstance(value, (tuple, list)) and any([isinstance(x, tf.SparseTensor) for x in value]):
            result = value[0]
            for v in value[1:]:
                result = tf.sparse.add(result, v, threshold=0)
            return result
        return tf.reduce_sum(value, axis=axis, keepdims=keepdims)

    def prod(self, value, axis=None):
        if axis is not None:
            if not isinstance(axis, int):
                axis = list(axis)
        if value.dtype == bool:
            return tf.reduce_all(value, axis=axis)
        return tf.reduce_prod(value, axis=axis)

    def where(self, condition, x=None, y=None):
        c = self.cast(condition, self.dtype(x))
        return c * x + (1 - c) * y
        # return tf.where(condition, x, y)  # TF1 has an inconsistent broadcasting rule for where

    def mean(self, value, axis=None, keepdims=False):
        if axis is not None:
            if not isinstance(axis, int):
                axis = list(axis)
        return tf.reduce_mean(value, axis, keepdims=keepdims)

    def grid_sample(self, grid, spatial_dims: tuple, coordinates, extrapolation='constant'):
        if use_cuda(grid):
            # TODO reshape for spatial_dims
            return resample_cuda(grid, coordinates, extrapolation)
        else:
            return NotImplemented

    def zeros(self, shape, dtype: DType = None):
        return tf.zeros(shape, dtype=to_numpy_dtype(dtype or self.float_type))

    def zeros_like(self, tensor):
        return tf.zeros_like(tensor)

    def ones(self, shape, dtype: DType = None):
        return tf.ones(shape, dtype=to_numpy_dtype(dtype or self.float_type))

    def ones_like(self, tensor):
        return tf.ones_like(tensor)

    def meshgrid(self, *coordinates):
        result = tf.meshgrid(*coordinates, indexing='ij')
        return result

    def linspace(self, start, stop, number):
        return self.to_float(tf.linspace(start, stop, number))

    def dot(self, a, b, axes):
        return tf.tensordot(a, b, axes)

    def matmul(self, A, b):
        if isinstance(A, tf.SparseTensor):
            result = tf.sparse.sparse_dense_matmul(A, tf.transpose(b))
            result = tf.transpose(result)
            # result.set_shape(tf.TensorShape([b.shape[0], A.shape[0]]))
            return result
        else:
            return tf.matmul(A, b)

    def einsum(self, equation, *tensors):
        return tf.einsum(equation, *tensors)

    def while_loop(self, cond, body, loop_vars, shape_invariants=None, parallel_iterations=10, back_prop=True,
                   swap_memory=False, name=None, maximum_iterations=None):
        return tf.while_loop(cond, body, loop_vars,
                             shape_invariants=shape_invariants,
                             parallel_iterations=parallel_iterations,
                             back_prop=back_prop,
                             swap_memory=swap_memory,
                             name=name,
                             maximum_iterations=maximum_iterations)

    def abs(self, x):
        return tf.abs(x)

    def sign(self, x):
        return tf.sign(x)

    def round(self, x):
        return tf.round(x)

    def ceil(self, x):
        return tf.math.ceil(x)

    def floor(self, x):
        return tf.floor(x)

    def max(self, x, axis=None, keepdims=False):
        return tf.reduce_max(x, axis=axis, keepdims=keepdims)

    def min(self, x, axis=None, keepdims=False):
        return tf.reduce_min(x, axis=axis, keepdims=keepdims)

    def maximum(self, a, b):
        a, b = self.auto_cast(a, b)
        return tf.maximum(a, b)

    def minimum(self, a, b):
        a, b = self.auto_cast(a, b)
        return tf.minimum(a, b)

    def clip(self, x, minimum, maximum):
        x, minimum, maximum = self.auto_cast(x, minimum, maximum)
        return tf.clip_by_value(x, minimum, maximum)

    def sqrt(self, x):
        return tf.sqrt(x)

    def exp(self, x):
        return tf.exp(x)

    def conv(self, tensor, kernel, padding="SAME"):
        rank = len(tensor.shape) - 2
        padding = padding.upper()
        if rank == 1:
            result = tf.nn.conv1d(tensor, kernel, 1, padding)
        elif rank == 2:
            result = tf.nn.conv2d(tensor, kernel, [1, 1, 1, 1], padding)
        elif rank == 3:
            result = tf.nn.conv3d(tensor, kernel, [1, 1, 1, 1, 1], padding)
        else:
            raise ValueError("Tensor must be of rank 1, 2 or 3 but is %d" % rank)
        return result

    def expand_dims(self, a, axis=0, number=1):
        if number == 0:
            return a
        for _i in range(number):
            a = tf.expand_dims(a, axis)
        return a

    def shape(self, tensor):
        return tf.shape(tensor)

    def staticshape(self, tensor):
        if self.is_tensor(tensor, only_native=True):
            return tuple(tensor.shape.as_list())
        else:
            return np.shape(tensor)

    def gather(self, values, indices):
        if isinstance(values, tf.SparseTensor):
            if isinstance(indices, (tuple, list)) and indices[1] == slice(None):
                result = sparse_select_indices(values, indices[0], axis=0, are_indices_sorted=True, are_indices_uniqua=True)
                return result
        if isinstance(indices, slice):
            return values[indices]
        return tf.gather(values, indices)

    def batched_gather_nd(self, values, indices):
        if self.staticshape(values)[0] == 1 and self.staticshape(indices)[0] != 1:
            result = tf.gather_nd(values[0, ...], indices, batch_dims=0)
            return result
        return tf.gather_nd(values, indices, batch_dims=1)

    def unstack(self, tensor, axis=0, keepdims=False):
        unstacked = tf.unstack(tensor, axis=axis)
        if keepdims:
            unstacked = [self.expand_dims(c, axis=axis) for c in unstacked]
        return unstacked

    def std(self, x, axis=None, keepdims=False):
        _mean, var = tf.nn.moments(x, axis, keepdims=keepdims)
        return tf.sqrt(var)

    def boolean_mask(self, x, mask):
        return tf.boolean_mask(x, mask)

    def isfinite(self, x):
        return tf.math.is_finite(x)

    def any(self, boolean_tensor, axis=None, keepdims=False):
        return tf.reduce_any(boolean_tensor, axis=axis, keepdims=keepdims)

    def all(self, boolean_tensor, axis=None, keepdims=False):
        return tf.reduce_all(boolean_tensor, axis=axis, keepdims=keepdims)

    def scatter(self, indices, values, shape, duplicates_handling='undefined', outside_handling='undefined'):
        assert duplicates_handling in ('undefined', 'add', 'mean', 'any')
        assert outside_handling in ('discard', 'clamp', 'undefined')
        if duplicates_handling == 'undefined':
            pass

        # Change indexing so batch number is included as first element of the index, for example: [0,31,24] indexes the first batch (batch 0) and 2D coordinates (31,24).
        buffer = tf.zeros(shape, dtype=values.dtype)

        repetitions = []
        for dim in range(len(indices.shape) - 1):
            if values.shape[dim] == 1:
                repetitions.append(indices.shape[dim])
            else:
                assert indices.shape[dim] == values.shape[dim]
                repetitions.append(1)
        repetitions.append(1)
        values = self.tile(values, repetitions)

        if duplicates_handling == 'add':
            # Only for Tensorflow with custom spatial_gradient
            @tf.custom_gradient
            def scatter_density(points, indices, values):
                result = tf.tensor_scatter_add(buffer, indices, values)

                def grad(dr):
                    return self.resample(gradient(dr, difference='central'), points), None, None

                return result, grad

            return scatter_density(points, indices, values)
        elif duplicates_handling == 'mean':
            # Won't entirely work with out of bounds particles (still counted in mean)
            count = tf.tensor_scatter_add(buffer, indices, tf.ones_like(values))
            total = tf.tensor_scatter_add(buffer, indices, values)
            return total / tf.maximum(1.0, count)
        else:  # last, any, undefined
            # indices = self.to_int(indices, int64=True)
            # st = tf.SparseTensor(indices, values, shape)  # ToDo this only supports 2D shapes
            # st = tf.sparse.reorder(st)   # only needed if not ordered
            # return tf.sparse.to_dense(st)
            count = tf.tensor_scatter_add(buffer, indices, tf.ones_like(values))
            total = tf.tensor_scatter_add(buffer, indices, values)
            return total / tf.maximum(1.0, count)

    def fft(self, x):
        rank = len(x.shape) - 2
        assert rank >= 1
        x = self.to_complex(x)
        if rank == 1:
            return tf.stack([tf.signal.fft(c) for c in tf.unstack(x, axis=-1)], axis=-1)
        elif rank == 2:
            return tf.stack([tf.signal.fft2d(c) for c in tf.unstack(x, axis=-1)], axis=-1)
        elif rank == 3:
            return tf.stack([tf.signal.fft3d(c) for c in tf.unstack(x, axis=-1)], axis=-1)
        else:
            raise NotImplementedError('n-dimensional FFT not implemented.')

    def ifft(self, k):
        rank = len(k.shape) - 2
        assert rank >= 1
        if rank == 1:
            return tf.stack([tf.signal.ifft(c) for c in tf.unstack(k, axis=-1)], axis=-1)
        elif rank == 2:
            return tf.stack([tf.signal.ifft2d(c) for c in tf.unstack(k, axis=-1)], axis=-1)
        elif rank == 3:
            return tf.stack([tf.signal.ifft3d(c) for c in tf.unstack(k, axis=-1)], axis=-1)
        else:
            raise NotImplementedError('n-dimensional inverse FFT not implemented.')

    def imag(self, complex):
        return tf.math.imag(complex)

    def real(self, complex):
        return tf.math.real(complex)

    def cast(self, x, dtype: DType):
        if not self.is_tensor(x, only_native=True):
            x = self.as_tensor(x, convert_external=True)
        if self.dtype(x) == dtype:
            return x
        else:
            return tf.cast(x, to_numpy_dtype(dtype))

    def sin(self, x):
        return tf.math.sin(x)

    def cos(self, x):
        return tf.math.cos(x)

    def dtype(self, array) -> DType:
        if tf.is_tensor(array):
            dt = array.dtype.as_numpy_dtype
            return from_numpy_dtype(dt)
        else:
            return NUMPY_BACKEND.dtype(array)

    def sparse_tensor(self, indices, values, shape):
        indices = [tf.convert_to_tensor(i, tf.int64) for i in indices]
        indices = tf.cast(tf.stack(indices, axis=-1), tf.int64)
        return tf.SparseTensor(indices=indices, values=values, dense_shape=shape)

    def coordinates(self, tensor, unstack_coordinates=False):
        if isinstance(tensor, tf.SparseTensor):
            idx = tensor.indices
            if unstack_coordinates:
                idx = tf.unstack(idx, axis=-1)
            return idx, tensor.values
        else:
            raise NotImplementedError()

    def conjugate_gradient(self, A, y, x0, solve_params=LinearSolve(), callback=None):
        if callable(A):
            function = A
        else:
            A = self.as_tensor(A)
            A_shape = self.staticshape(A)
            assert len(A_shape) == 2, f"A must be a square matrix but got shape {A_shape}"
            assert A_shape[0] == A_shape[1], f"A must be a square matrix but got shape {A_shape}"

            def function(vec):
                return self.matmul(A, vec)

        batch_size = combined_dim(x0.shape[0], y.shape[0])
        if x0.shape[0] < batch_size:
            x0 = tf.tile(x0, [batch_size, 1])

        def cg_forward(y, x0, params: LinearSolve):
            tolerance_sq = self.maximum(params.relative_tolerance ** 2 * tf.reduce_sum(y ** 2, -1), params.absolute_tolerance ** 2)
            x = x0
            dx = residual = y - function(x)
            dy = function(dx)
            iterations = 0
            converged = True
            while self.all(self.sum(residual ** 2, -1) > tolerance_sq):
                if iterations == params.max_iterations:
                    converged = False
                    break
                iterations += 1
                dx_dy = self.sum(dx * dy, axis=-1, keepdims=True)
                step_size = self.divide_no_nan(self.sum(dx * residual, axis=-1, keepdims=True), dx_dy)
                x += step_size * dx
                residual -= step_size * dy
                dx = residual - self.divide_no_nan(self.sum(residual * dy, axis=-1, keepdims=True) * dx, dx_dy)
                dy = function(dx)
            params.result = SolveResult(converged, iterations)
            return x

        @tf.custom_gradient
        def cg_with_grad(y):
            def grad(dx):
                return cg_forward(dx, tf.zeros_like(x0), solve_params.gradient_solve)
            return cg_forward(y, x0, solve_params), grad

        result = cg_with_grad(y)
        return result

    def minimize(self, function, x0, solve_params: Solve):
        x0 = self.numpy(x0)

        # @tf.function
        def val_and_grad(x):
            with tf.GradientTape() as tape:
                tape.watch(x)
                loss = function(x)
            grad = tape.gradient(loss, x)
            return loss, grad

        def min_target(x):
            x = self.as_tensor(x, convert_external=True)
            val, grad = val_and_grad(x)
            return val.numpy().astype(np.float64), grad.numpy().astype(np.float64)

        assert solve_params.relative_tolerance is None
        res = sopt.minimize(fun=min_target, x0=x0, jac=True,
                            method=solve_params.solver or 'L-BFGS-B',
                            tol=solve_params.absolute_tolerance,
                            options={'maxiter': solve_params.max_iterations})
        solve_params.result = SolveResult(res.success, res.nit)
        return res.x

    def add(self, a, b):
        if isinstance(a, tf.SparseTensor) or isinstance(b, tf.SparseTensor):
            return tf.sparse.add(a, b, threshold=1e-5)
        else:
            return Backend.add(self, a, b)

    def functional_gradient(self, f, wrt: tuple or list, get_output: bool):
        @wraps(f)
        def eval_grad(*args):
            args = [self.as_tensor(arg, True) if i in wrt else arg for i, arg in enumerate(args)]
            wrt_args = [arg for i, arg in enumerate(args) if i in wrt]
            with tf.GradientTape(watch_accessed_variables=False) as tape:
                for arg in wrt_args:
                    tape.watch(arg)
                output = f(*args)
            loss, aux = (output[0], output[1:]) if isinstance(output, (tuple, list)) else (output, None)
            grads = tape.gradient(loss, wrt_args)
            if get_output:
                return (loss, *aux, *grads)
            else:
                return grads
        return eval_grad

    # def variable(self, value):  # not supported, variables must record gradients outside a context
    #     return tf.Variable(value, trainable=True)

    def gradients(self, y, xs: tuple or list, grad_y):
        if _TAPES:
            tape = _TAPES[-1]
            return tape.gradient(y, xs, grad_y)
        return tf.gradients(y, xs, grad_y)

    @contextmanager
    def record_gradients(self, xs: tuple or list, persistent=False):
        tape = tf.GradientTape(persistent=persistent)
        tape.__enter__()
        for x in xs:
            tape.watch(x)
        _TAPES.append(tape)

        try:
            yield None
        finally:
            tape.__exit__(None, None, None)
            _TAPES.pop(-1)

    def stop_gradient(self, value):
        return tf.stop_gradient(value)


TF_BACKEND = TFBackend()
_TAPES = []


def sparse_select_indices(sp_input, indices, axis=0, are_indices_uniqua=False, are_indices_sorted=False):
    if not are_indices_uniqua:
        indices, _ = tf.unique(indices)
    n_indices = tf.size(indices)
    # Only necessary if indices may not be sorted
    if not are_indices_sorted:
        indices, _ = tf.math.top_k(indices, n_indices)
        indices = tf.reverse(indices, [0])
    # Get indices for the axis
    idx = sp_input.indices[:, axis]
    # Find where indices match the selection
    eq = tf.equal(tf.expand_dims(idx, 1), tf.cast(indices, tf.int64))
    # Mask for selected values
    sel = tf.reduce_any(eq, axis=1)
    # Selected values
    values_new = tf.boolean_mask(sp_input.values, sel, axis=0)
    # New index value for selected elements
    n_indices = tf.cast(n_indices, tf.int64)
    idx_new = tf.reduce_sum(tf.cast(eq, tf.int64) * tf.range(n_indices), axis=1)
    idx_new = tf.boolean_mask(idx_new, sel, axis=0)
    # New full indices tensor
    indices_new = tf.boolean_mask(sp_input.indices, sel, axis=0)
    indices_new = tf.concat([indices_new[:, :axis], tf.expand_dims(idx_new, 1), indices_new[:, axis + 1:]], axis=1)
    # New shape
    shape_new = tf.concat([sp_input.dense_shape[:axis], [n_indices], sp_input.dense_shape[axis + 1:]], axis=0)
    return tf.SparseTensor(indices_new, values_new, shape_new)
