# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.webdav.tests.test_webdav import suite
except ImportError:
    from .test_webdav import suite

__all__ = ['suite']
