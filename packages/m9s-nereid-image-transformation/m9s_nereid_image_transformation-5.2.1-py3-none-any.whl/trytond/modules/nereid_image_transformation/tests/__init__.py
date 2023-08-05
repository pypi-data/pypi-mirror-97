# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.nereid_image_transformation.tests.test_nereid_image_transformation import suite
except ImportError:
    from .test_nereid_image_transformation import suite

__all__ = ['suite']
