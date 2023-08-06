"""
    binalyzer_vmf.extension
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Binalyzer VMF extension.
"""
from binalyzer_core import BinalyzerExtension

class VmfExtension(BinalyzerExtension):
    def __init__(self, binalyzer=None):
        super(VmfExtension, self).__init__(binalyzer, "vmf")

    def init_extension(self):
        super(VmfExtension, self).init_extension()
