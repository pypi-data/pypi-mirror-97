# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import io
import time
import os
import sys

from io import BytesIO
from urllib.parse import unquote
from pytz import timezone
from datetime import datetime
from jinja2 import Markup
from PIL import Image

import trytond.tests.test_tryton
from trytond.tests.test_tryton import DB_NAME, with_transaction
from trytond.config import config
from trytond.pool import Pool
from trytond.transaction import Transaction

from nereid.testing import NereidModuleTestCase
from nereid import render_template

from trytond.modules.nereid.tests.test_common import create_static_file


class NereidImageTransformationTestCase(NereidModuleTestCase):
    'Test Nereid Image Transformation module'
    module = 'nereid_image_transformation'

    def setUp(self):
        trytond.tests.test_tryton.activate_module('nereid_image_transformation')
        self.templates = {
            'home.jinja':
            '''
            {% set static_file = static_file_obj(static_file_id) %}
            {{ static_file.url }}
            ''',
            }
        # Ignore ResourceWarnings
        if not sys.warnoptions:
            import warnings
            warnings.simplefilter("ignore")

    def tearDown(self):
        """
        Delete the contents of the test directories
        """
        self.delete_directory('/tmp/nereid')
        self.delete_directory(config.get('database', 'path'))

    def delete_directory(self, dirname):
        for root, dirs, files in os.walk(dirname, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    @with_transaction()
    def test_0005_static_file_transform_command(self):
        file_memoryview = memoryview(b'test-content')
        static_file = create_static_file(file_memoryview)

        self.assertFalse(static_file.url)
        self.assertEqual(
            str(static_file.transform_command().thumbnail(200, 200, 'a')),
            'thumbnail,w_200,h_200,m_a')
        self.assertEqual(
            str(static_file.transform_command().resize(100, 100, 'n')),
            'resize,w_100,h_100,m_n')
        self.assertEqual(
            str(static_file.transform_command().fit(150, 150, 'l')),
            'fit,w_150,h_150,m_l')

    @with_transaction()
    def test_0010_static_file_url(self):
        pool = Pool()
        StaticFile = pool.get('nereid.static.file')

        file_memoryview = memoryview(b'test-content')
        static_file = create_static_file(file_memoryview)
        self.assertFalse(static_file.url)

        app = self.get_app()

        with app.test_request_context('/'):
            rv = render_template(
                'home.jinja',
                static_file_obj=StaticFile,
                static_file_id=static_file.id)
            self.assertTrue('/en/static-file/test/test.png'
                in unquote(str(rv)))

    @with_transaction()
    def test_0015_markup_test(self):
        """
        Tests that Markup wraps the URL.
        """
        file_memoryview = memoryview(b'test-content2')
        static_file = create_static_file(file_memoryview)
        self.assertFalse(static_file.url)

        app = self.get_app()
        static_file_command = static_file.transform_command()

        with app.test_request_context('/'):
            self.assertTrue(isinstance(static_file_command.__html__(),
                    Markup))

    @with_transaction()
    def test_0020_quoted_url(self):
        """
        Test that quoted urls work properly.
        """
        app = self.get_app()

        img_file = BytesIO()
        img = Image.new("RGB", (100, 100), "black")
        img.save(img_file, 'png')

        img_file.seek(0)
        static_file = create_static_file(memoryview(img_file.read()),
            name='2.png')

        self.assertFalse(static_file.url)

        with app.test_client() as c:
            rv = c.get(
                '/static-file-transform/{0}/thumbnail'
                '%2Cw_300%2Ch_300%2Cm_a.png'.format(static_file.id)
            )
            self.assertEqual(rv.status_code, 200)
            with Image.open(io.BytesIO(rv.data)) as img:
                # Assert if black
                self.assertEqual(img.getpixel((0, 0)), (0, 0, 0))
            # Improper URL won't work
            rv = c.get(
                '/static-file-transform/{0}/'
                'thumbnail%25252Cw_300%25252Ch_300%25252Cm_a.png'.
                format(static_file.id)
            )
            self.assertTrue(rv.status_code, 404)

    @with_transaction()
    def test_0025_quoted_url_localized(self):
        """
        Test that quoted urls work properly in localized environment.
        """
        app = self.get_app()

        img_file = BytesIO()
        img = Image.new("RGB", (100, 100), "black")
        img.save(img_file, 'png')

        img_file.seek(0)
        static_file = create_static_file(memoryview(img_file.read()),
            name='2.png')

        self.assertFalse(static_file.url)

        with app.test_client() as c:
            rv = c.get(
                '/en/static-file-transform/{0}/thumbnail'
                '%2Cw_300%2Ch_300%2Cm_a.png'.format(static_file.id))
            self.assertEqual(rv.status_code, 200)
            with Image.open(io.BytesIO(rv.data)) as img:
                # Assert if black
                self.assertEqual(img.getpixel((0, 0)), (0, 0, 0))
            # Improper URL won't work
            rv = c.get(
                '/en/static-file-transform/{0}/'
                'thumbnail%25252Cw_300%25252Ch_300%25252Cm_a.png'.
                format(static_file.id)
            )
            self.assertTrue(rv.status_code, 404)

    @with_transaction()
    def test_0030_transform_static_file_cache(self):
        pool = Pool()
        StaticFile = pool.get('nereid.static.file')

        img_file = BytesIO()
        img = Image.new("RGB", (100, 100), "white")
        img.save(img_file, 'png')

        img_file.seek(0)
        static_file = create_static_file(memoryview(img_file.read()),
            name='3.png')

        self.assertFalse(static_file.url)

        app = self.get_app()

        with app.test_client() as c:
            rv = c.get('/static-file-transform/%d/thumbnail,w_120,h_120,m_n/'
                'resize,w_100,h_100,m_n.png' % static_file.id)
            self.assertEqual(rv.status_code, 200)
            img = Image.open(io.BytesIO(rv.data))
            # Assert if white
            self.assertEqual(img.getpixel((0, 0)), (255, 255, 255))

        # Get temp image file datetime for later compare
        temp_image_time = datetime.fromtimestamp(os.path.getmtime(
            '/tmp/nereid/%s/%d/'
            'thumbnailw_120h_120m_n_resizew_100h_100m_n.png' %
            (DB_NAME, static_file.id)), timezone('UTC'))
        Transaction().commit()  # Commit to retain file

        time.sleep(1)

        # Access file again (should come from cache)
        with app.test_client() as c:
            rv = c.get(
                '/static-file-transform/%d/thumbnail,w_120,h_120,m_n/'
                'resize,w_100,h_100,m_n.png' % static_file.id)
            self.assertEqual(rv.status_code, 200)
            with Image.open(io.BytesIO(rv.data)) as img:
                # Assert if white
                self.assertEqual(img.getpixel((0, 0)), (255, 255, 255))

        # Assert if file on file system is not modified.
        self.assertEqual(temp_image_time, datetime.fromtimestamp(
                os.path.getmtime(
                    '/tmp/nereid/%s/%d/'
                    'thumbnailw_120h_120m_n_resizew_100h_100m_n.png' %
                    (DB_NAME, static_file.id)), timezone('UTC')))

        # Generate new image
        img_file = BytesIO()
        img = Image.new("RGB", (100, 100), "black")
        img.save(img_file, 'png')

        img_file.seek(0)

        # Update the image in same static file (i.e. update the cached file)
        static_file = StaticFile(static_file.id)
        static_file.file_binary = img_file.read()
        static_file.save()

        app = self.get_app()

        with app.test_client() as c:
            rv = c.get(
                '/static-file-transform/%d/thumbnail,w_120,h_120,m_n/'
                'resize,w_100,h_100,m_n.png' % static_file.id)
            self.assertEqual(rv.status_code, 200)
            with Image.open(io.BytesIO(rv.data)) as img:
                # Assert if black
                self.assertEqual(img.getpixel((0, 0)), (0, 0, 0))

        # Assert if file on file system was modified.
        self.assertTrue(temp_image_time < datetime.fromtimestamp(
                os.path.getmtime(
                    '/tmp/nereid/%s/%d/'
                    'thumbnailw_120h_120m_n_resizew_100h_100m_n.png' %
                    (DB_NAME, static_file.id)), timezone('UTC')))

    @with_transaction()
    def test_0040_allowed_operations(self):
        """
        Test that not allowed operations return 404
        """
        app = self.get_app()

        img_file = BytesIO()
        img = Image.new("RGB", (100, 100), "black")
        img.save(img_file, 'png')

        img_file.seek(0)
        static_file = create_static_file(memoryview(img_file.read()),
            name='2.png')

        self.assertFalse(static_file.url)

        with app.test_client() as c:
            rv = c.get(
                '/static-file-transform/{0}/grumbnail'
                '%2Cw_300%2Ch_300%2Cm_a.png'.format(static_file.id))
            self.assertEqual(rv.status_code, 404)

    @with_transaction()
    def test_0050_fit_image(self):
        """
        Test that the fit command works
        """
        app = self.get_app()

        img_file = BytesIO()
        img = Image.new("RGB", (100, 100), "black")
        img.save(img_file, 'png')

        img_file.seek(0)
        static_file = create_static_file(memoryview(img_file.read()),
            name='2.png')

        with app.test_client() as c:
            rv = c.get(
                '/static-file-transform/{0}/fit'
                '%2Cw_300%2Ch_300%2Cm_a.png'.format(static_file.id))
            self.assertEqual(rv.status_code, 200)


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            NereidImageTransformationTestCase))
    return suite
