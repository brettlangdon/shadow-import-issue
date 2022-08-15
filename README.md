# Shadow Import Issue

This repo includes a reproduction of an import issue when using `setuptools>=64.0.0` and Cython when installed in editable mode.

This issue occurs when importing a module from a parent module which has the same name as a sibling module.

For example:

```
├── shadow_import_issue
│   ├── __init__.py
│   ├── c_exts
│   │   ├── __init__.py
│   │   ├── _child.pyx
│   │   └── shadow.py
│   ├── shadow.py
│   └── sub
│       ├── __init__.py
│       ├── child.py
└──     └── shadow.py
```

When trying to import `shadow_import_issue.shadow` from `shadow_import_issue.c_exts._child` it will import `shadow_import_issue.c_exts.shadow` instead.

This issue is not present when importing `shadow_import_issue.shadow` from `shadow_import_issue.sub.child` (pure-python version).

## Running

``` shell
git clone https://github.com/brettlangdon/shadow-import-issue.git
cd ./shadow-import-issue/
docker build -t shadow-import-issue .
docker run --rm shadow-import-issue
```

Expected output is to fail with:

```
pure-python VAR
Traceback (most recent call last):
  File "/src/test.py", line 1, in <module>
    import shadow_import_issue
  File "/src/shadow_import_issue/__init__.py", line 5, in <module>
    from .c_exts import _child  # isort:skip
  File "shadow_import_issue/c_exts/_child.pyx", line 1, in init shadow_import_issue.c_exts._child
    from shadow_import_issue.shadow import VAR
ImportError: cannot import name VAR
```

The module and variable will import fine with Python, but will fail the import from the Cython module.
