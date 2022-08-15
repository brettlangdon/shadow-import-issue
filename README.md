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
<module 'shadow_import_issue.shadow' from '/src/shadow_import_issue/shadow.py'>
VAR
<module 'shadow_import_issue.c_exts.shadow_import_issue.shadow' from '/src/shadow_import_issue/c_exts/shadow.py'>
Traceback (most recent call last):
  File "/src/test.py", line 1, in <module>
    import shadow_import_issue
  File "/src/shadow_import_issue/__init__.py", line 3, in <module>
    import shadow_import_issue.c_exts._child  # isort:skip
  File "shadow_import_issue/c_exts/_child.pyx", line 4, in init shadow_import_issue.c_exts._child
    print(shadow_import_issue.shadow.VAR)
AttributeError: module 'shadow_import_issue.c_exts.shadow_import_issue.shadow' has no attribute 'VAR'
```

The module and variable will import fine with Python, but will fail the import from the Cython module.


## Analysis

- This only happens with editable install
- This only occurs with `setuptools>=64.0.0`
   - `setuptools>=64.0.0` changed from using `.egg-link` to `.pth` + editable loader
- The module loaded by Cython has the name `shadow_import_issue.c_exts.shadow_import_issue.shadow` and is loaded from `shadow_import_issue/c_exts/shadow.py`
- The issue does not happen with `Cython==3.0.0a11`
