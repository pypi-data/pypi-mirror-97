# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.customs_value.tests.test_customs_value import suite
except ImportError:
    from .test_customs_value import suite

__all__ = ['suite']
