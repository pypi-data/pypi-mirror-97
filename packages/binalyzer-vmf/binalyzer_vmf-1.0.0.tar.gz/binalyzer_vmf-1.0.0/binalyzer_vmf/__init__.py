# -*- coding: utf-8 -*-
"""
    binalyzer_vmf
    ~~~~~~~~~~~~~

    Binalyzer VMF Extension

    :copyright: 2021 Denis Vasilík
    :license: MIT, see LICENSE for details.
"""

name = "binalyzer_vmf"

__tag__ = "v1.0.0"
__build__ = 6
__version__ = "{}".format(__tag__)
__commit__ = "ef21988"

from .extension import VmfExtension
