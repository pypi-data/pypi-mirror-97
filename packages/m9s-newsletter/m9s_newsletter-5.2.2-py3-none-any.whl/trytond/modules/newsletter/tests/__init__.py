# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.newsletter.tests.test_newsletter import suite
except ImportError:
    from .test_newsletter import suite

__all__ = ['suite']
