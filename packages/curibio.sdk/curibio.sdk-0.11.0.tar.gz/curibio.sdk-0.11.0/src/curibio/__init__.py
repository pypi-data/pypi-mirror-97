# -*- coding: utf-8 -*-
"""Placeholder init file for compatibility with namespaced package.

See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages, https://github.com/pypa/sample-namespace-packages/tree/master/pkg_resources/pkg_b
"""
from typing import Iterable  # noqa

try:
    __import__("pkg_resources").declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path

    __path__ = extend_path(__path__, __name__)  # type: Iterable[str]
