import Cython.Distutils
from Cython.Build import cythonize
from setuptools import find_packages, setup

setup(
    name="shadow_import_issue",
    version="1.0",
    packages=find_packages(),
    ext_modules=cythonize(
        [
            Cython.Distutils.Extension(
                "shadow_import_issue.c_exts._child",
                sources=["shadow_import_issue/c_exts/_child.pyx"],
                language="c",
            ),
        ],
        force=True,
        annotate=True,
    ),
)
