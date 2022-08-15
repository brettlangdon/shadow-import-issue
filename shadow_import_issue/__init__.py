from .sub import child  # isort:skip

print("pure-python", child.VAR)

from .c_exts import _child  # isort:skip

print("cython", _child.VAR)
