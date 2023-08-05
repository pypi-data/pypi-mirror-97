import numpy as np
from pyctlib import vector
import copy

class matrix(np.ndarray):

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        if len(obj.shape) == 1:
            obj.resize(obj.size, 1)
        if len(obj.shape) != 2 and len(obj.shape) != 4:
            print("warning size: {}".format(obj.shape))
        return obj

    def __mul__(self, other):
        if isinstance(other, diffmatrix):
            assert self.dim() == 2
            assert self.shape[1] == other.left_size[0]
            ret = create_matrix(self.shape[0], other.left_size[1], *other.right_size, style="zero")
            for i in range(self.shape[0]):
                for j in range(other.left_size[1]):
                    for k in range(other.left_size[0]):
                        ret[i, j, :, :] = ret[i, j, :, :] + self[i, k] * other.matrix[k, j, :, :]
            return diffmatrix(matrix(ret))
        elif isinstance(other, matrix):
            return self @ other
        else:
            return super().__mul__(other)

    def dim(self):
        return len(self.shape)

    def abs(self):
        return matrix(abs(self))

    def allclose(self, other):
        return bool(((self - other).abs() < 1e-6).all())

    def t(self):
        return self.T

    def __and__(self, other):
        # element wise product
        if isinstance(other, matrix):
            assert self.dim() == 2 and other.dim() == 2
            assert self.shape == other.shape
            return matrix((np.asarray(self) * other))
        return super().__and__(other)

    def __pow__(self, other):
        # krok product
        if isinstance(other, matrix):
            assert self.dim() == 2 and other.dim() == 2
            n, m = self.shape
            p, q = other.shape
            ret = create_matrix(n * p, m * q, style="zero")
            for i in range(n):
                for j in range(m):
                    for k in range(p):
                        for l in range(q):
                            I = k + p * (i)
                            J = l + q * (j)
                            ret[I, J] = self[i,j] * other[k, l]
            return matrix(ret)
        return super.__pow__(other)

def create_matrix(*shape, style="gaussian"):
    shape = totuple(shape)
    if style == "gaussian":
        return matrix(np.random.randn(*shape))
    if style == "unit":
        return matrix(np.random.rand(*shape))
    if style == "one":
        return matrix(np.ones(shape))
    if style == "eye":
        assert len(shape) == 1 or (len(shape) == 2 and shape[0] == shape[1])
        return matrix(np.eye(shape[0]))
    return matrix(np.zeros(shape))

def totuple(args):
    if len(args) == 0:
        return args
    if len(args) > 1:
        return args
    if len(args) == 1 and (isinstance(args[0], tuple) or isinstance(args[0], list) or isinstance(args[0], vector)):
        return tuple(args[0])
    return args

class diffmatrix:

    def __init__(self, *args, style="gaussian"):
        self.left_size = None
        self.right_size = None
        self.matrix = None
        self.E = False
        self.ET = False
        if len(args) > 0 and isinstance(args[0], str) and args[0] == "E":
            self.E = True
            return
        if len(args) > 0 and isinstance(args[0], str) and args[0] == "ET":
            self.E = True
            return
        args = totuple(args)
        if style == "E" and len(args) == 0:
            self.E = True
            return
        if style == "ET" and len(args) == 0:
            self.ET = True
            return
        if len(args) == 0:
            return
        elif len(args) == 4:
            self.left_size = args[:2]
            self.right_size = args[2:]
            self.matrix = create_matrix(*self.left_size, *self.right_size, style=style)
        elif len(args) == 2:
            assert style == "E" or style == "ET" or style == "gaussian"
            if style == "gaussian":
                style = "E"
            if style == "E":
                self.left_size = copy.copy(args)
                self.right_size = copy.copy(args)
                self.matrix = create_matrix(*self.left_size, *self.right_size, style="zero")
                for i in range(self.left_size[0]):
                    for j in range(self.left_size[1]):
                        self.matrix[i][j][i][j] = 1.
            else:
                self.left_size = copy.copy(args)
                self.right_size = copy.copy(args)[::-1]
                self.matrix = create_matrix(*self.left_size, *self.right_size, style="zero")
                for i in range(self.left_size[0]):
                    for j in range(self.left_size[1]):
                        self.matrix[i][j][j][i] = 1.
        elif len(args) == 1 and isinstance(args[0], diffmatrix):
            self.left_size = copy.copy(args[0].left_size)
            self.right_size = copy.copy(args[0].right_size)
            self.matrix = copy.deepcopy(args[0].matrix)
        elif len(args) == 1 and isinstance(args[0], np.ndarray):
            self.matrix = copy.deepcopy(matrix(args[0]))
            if len(self.matrix.shape) == 1:
                self.matrix.resize((1, 1, self.matrix.size, 1))
            if len(self.matrix.shape) == 2:
                self.matrix.resize((*(1,1), *self.matrix.shape))
            self.left_size = self.matrix.shape[:2]
            self.right_size = self.matrix.shape[2:]
        assert isinstance(self.matrix, matrix)
        return

    def __str__(self):
        if self.E:
            return "E, <unknown shape>"
        if self.ET:
            return "ET, <unknown shape>"
        ret = vector()
        for i in range(self.left_size[0]):
            for k in range(self.right_size[0]):
                sen = vector()
                sen.append("[")
                for j in range(self.left_size[1]):
                    sen.append("[")
                    for l in range(self.right_size[1]):
                        sen.append(("{:3}".format(float(self.matrix[i, j, k, l])) + " " * 4)[:4])
                        if l < self.right_size[1] - 1:
                            sen.append(" ")
                    sen.append("]")
                    if j < self.left_size[1] - 1:
                        sen.append(" ")
                sen.append("]")
                ret.append(sen)
            if i < self.left_size[0] - 1:
                sen = vector()
                sen.append("[")
                for j in range(self.left_size[1]):
                    sen.append(" ")
                    for l in range(self.right_size[1]):
                        sen.append("    ")
                        if l < self.right_size[1] - 1:
                            sen.append(" ")
                    sen.append(" ")
                    if j < self.left_size[1] - 1:
                        sen.append(" ")
                sen.append("]")
                ret.append(sen)
        return "\n".join(ret.map(lambda x: "".join(x))) + "\n" + "{}x{}->{}x{}".format(*self.left_size, *self.right_size)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if self.E:
            if isinstance(other, diffmatrix):
                assert not other.E and other.ET
                assert other.left_size == other.right_size
                return diffmatrix(other.left_size, "E") + other
            raise RuntimeError("unknown shape")
        if self.ET:
            if isinstance(other, diffmatrix):
                assert not other.E and other.ET
                assert other.left_size == other.right_size[::-1]
                return diffmatrix(other.left_size, "ET") + other
            raise RuntimeError("unknown shape")
        if isinstance(other, diffmatrix):
            if other.E:
                assert self.left_size == self.right_size
                return self + diffmatrix(self.left_size, "E")
            if other.ET:
                assert self.left_size == self.right_size[::-1]
                return self + diffmatrix(self.left_size, "ET")
            return diffmatrix(self.matrix + other.matrix)
        if isinstance(other, float):
            return diffmatrix(self.matrix + other)
        if isinstance(other, int):
            return diffmatrix(self.matrix + other)

    def __sub__(self, other):
        if self.E:
            if isinstance(other, diffmatrix):
                assert not other.E and other.ET
                assert other.left_size == other.right_size
                return diffmatrix(other.left_size, "E") - other
            raise RuntimeError("unknown shape")
        if self.ET:
            if isinstance(other, diffmatrix):
                assert not other.E and other.ET
                assert other.left_size == other.right_size[::-1]
                return diffmatrix(other.left_size, "ET") - other
            raise RuntimeError("unknown shape")
        if isinstance(other, diffmatrix):
            if other.E:
                assert self.left_size == self.right_size
                return self - diffmatrix(self.left_size, "E")
            if other.ET:
                assert self.left_size == self.right_size[::-1]
                return self - diffmatrix(self.left_size, "ET")
            return diffmatrix(self.matrix - other.matrix)
        if isinstance(other, float):
            return diffmatrix(self.matrix - other)
        if isinstance(other, int):
            return diffmatrix(self.matrix - other)

    def __mul__(self, other):
        if self.E:
            if isinstance(other, diffmatrix):
                return other
            raise RuntimeError("unknown shape")
        if self.ET:
            if isinstance(other, diffmatrix):
                return other.t()
            raise RuntimeError("unknown shape")
        if isinstance(other, int):
            return diffmatrix(self.matrix * other)
        if isinstance(other, float):
            return diffmatrix(self.matrix * other)
        if isinstance(other, np.ndarray) and not isinstance(other, matrix):
            return self.__mul__(matrix(other))
        if isinstance(other, matrix):
            if self.left_size == (1, 1) and other.shape[0] != 1:
                ret = create_matrix(*other.shape, *self.right_size, style="zero")
                for i in range(other.shape[0]):
                    for j in range(other.shape[1]):
                        ret[i, j, :, :] = ret[i, j, :, :] + other[i, j] * self.matrix[0, 0, :, :]
                return diffmatrix(matrix(ret))
            assert other.dim() == 2
            assert other.shape[0] == self.left_size[1]
            ret = create_matrix(self.left_size[0], other.shape[1], *self.right_size, style="zero")
            for i in range(self.left_size[0]):
                for j in range(other.shape[1]):
                    for k in range(self.left_size[1]):
                        ret[i, j, :, :] = ret[i, j, :, :] + self.matrix[i, k, :, :] * other[k, j]
            return diffmatrix(matrix(ret))
        if isinstance(other, diffmatrix):
            if other.E:
                return self
            if other.ET:
                return self * diffmatrix(self.right_size, style="ET")
            assert self.right_size == other.left_size
            ret = create_matrix(*self.left_size, *other.right_size, style="zero")
            for i in range(self.left_size[0]):
                for j in range(self.left_size[1]):
                    for k in range(self.right_size[0]):
                        for l in range(self.right_size[1]):
                            ret[i, j, :, :] = ret[i, j, :, :] +  self.matrix[i, j, k, l] * other.matrix[k, l, :, :]
            return diffmatrix(matrix(ret))
        raise RuntimeError("error mul type: {}".format(type(other)))

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self * other
        raise RuntimeError("error in rmul: type {}".format(type(other)))

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return diffmatrix(-self.matrix)

    def __rsub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return diffmatrix(other - self.matrix)
        raise RuntimeError("error in rsub: type {}".format(type(other)))

    def __getitem__(self, *args, **kwargs):
        assert not self.E and not self.ET
        return self.matrix.__getitem__(*args, **kwargs)

    def __eq__(self, other):
        assert not self.E and not self.ET and not other.E and not other.ET
        assert isinstance(other, diffmatrix)
        return self.matrix == other.matrix

    def allclose(self, other):
        assert not self.E and not self.ET and not other.E and not other.ET
        assert isinstance(other, diffmatrix)
        return bool(self.matrix.allclose(other.matrix))

    def t(self):
        if self.E:
            return diffmatrix(style="ET")
        if self.ET:
            return diffmatrix(style="E")
        ret = create_matrix(*self.left_size[::-1], *self.right_size, style="zero")
        for i in range(self.left_size[1]):
            for j in range(self.left_size[0]):
                ret[i, j, :, :] = self.matrix[j, i, :, :]
        return diffmatrix(matrix(ret))

    def tr(self):
        assert not self.E and not self.ET
        assert self.left_size[0] == self.left_size[1]
        ret = create_matrix(*self.right_size, style="zero")
        for i in range(self.left_size[0]):
            for k in range(self.right_size[0]):
                for l in range(self.right_size[1]):
                    ret[k, l] = ret[k, l] + self.matrix[i,i,k,l]
        return ret

    def mat(self):
        assert not self.E and not self.ET
        n, m = self.left_size
        p, q = self.right_size
        ret = create_matrix(n*m, p*q, style="zero")
        index_l, index_r = 0, 0
        for j in range(m):
            for i in range(n):
                index_r = 0
                for l in range(q):
                    for k in range(p):
                        ret[index_l, index_r] = self.matrix[i, j, k, l]
                        index_r += 1
                index_l += 1
        return ret

    @property
    def shape(self):
        if self.E or self.ET:
            return None
        return (*self.left_size, *self.right_size)

E = diffmatrix("E")
ET = diffmatrix("ET")

# class EM:

#     def __init__(self, *args):
#         if len(args) == 0:
#             self.dm = None
#         if len(args) == 1 and isinstance(args[0], int):
#             self.dm = diffmatrix(args[0], args[0])
#         if len(args) == 1:
#             assert len(args[0]) == 2
#             self.dm = diffmatrix(args[0][1], args[0][1])
#         if len(args) == 2:
#             assert isinstance(args[0], int)
#             self.dm = diffmatrix(args[0], args[1])
#         self.dm = None
