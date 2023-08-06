from io import StringIO
import os
import sys
import unittest
from importlib import reload

from confyml import confyml

confyml.set_config('resources/2.sample.config.yaml', mode='cf')

from tests.resources import sample_module

FILE_PATH = os.path.dirname(__file__)


class TestConfigMethodsMode3(unittest.TestCase):

    def setUp(self) -> None:
        file_path = os.path.dirname(__file__)
        yaml_file = os.path.abspath(os.path.join(
                                     file_path,
                                     'resources/1.test.config.yaml'))
        self._sut = confyml.Config(yaml_file, mode='mcf')

    def test_object_is_config(self):
        self.assertIsInstance(self._sut, confyml.Config)

    def test_should_return_list_of_configured_objects(self):
        objects = ['example_module1.ExampleClass11',
                   'example_module1.ExampleClass11.example_function111',
                   'example_module1.ExampleClass12',
                   'example_module1.ExampleClass12.example_function121',
                   'example_module1.ExampleClass12.example_function122',
                   'example_module_2.ExampleClass21.example_function211']
        self.assertEqual(set(objects), set(self._sut._get_objects()))

    def test_should_return_config_for_object(self):
        actual = self._sut._get_config('example_module1.ExampleClass11')
        expt = {'kwarg_1101': 1, 'kwarg_1102': 'test'}
        self.assertDictEqual(expt, actual)
        actual = self._sut._get_config('example_module1.ExampleClass11'
                                       '.example_function111')
        expt = {'kwarg_1111': 2, 'kwarg_1112': 'function_test',
                'kwarg_1113': 'yaml_test'}
        self.assertDictEqual(expt, actual)


class TestConfigMethodsMode2(unittest.TestCase):

    def setUp(self) -> None:
        file_path = os.path.dirname(__file__)
        yaml_file = os.path.abspath(os.path.join(
                                     file_path,
                                     'resources/2.test.config.yaml'))
        self._sut = confyml.Config(yaml_file, mode='cf')

    def test_object_is_config(self):
        self.assertIsInstance(self._sut, confyml.Config)

    def test_should_return_list_of_configured_objects(self):
        objects = ['ExampleClass', 'ExampleClass.example_function']
        self.assertEqual(set(objects), set(self._sut._get_objects()))

    def test_should_return_config_for_object(self):
        conf = self._sut._get_config('ExampleClass.example_function')
        expt = {'kwarg_1': 2,
                'kwarg_2': 'function_test',
                'kwarg_3': 'yaml_test'}
        self.assertDictEqual(expt, conf)
        conf = self._sut._get_config('ExampleClass')
        expt = {'kwarg_1': 1, 'kwarg_2': 'test'}
        self.assertDictEqual(expt, conf)

    def test_should_apply_config(self):
        confyml.set_config('resources/2.sample.config.yaml', mode='cf')
        reload(sample_module)
        ret = sample_module.SampleClass().sample_method()
        self.assertEqual((2, 1), ret)
        ret = sample_module.sample_function()
        self.assertEqual(1, ret)


class TestConfigMethodsMode1(unittest.TestCase):

    def setUp(self) -> None:
        objects = os.path.abspath(os.path.join(
                                     FILE_PATH,
                                     'resources/3.test.config.yaml'))
        self._sut = confyml.Config(objects, mode='f')

    def test_object_is_config(self):
        self.assertIsInstance(self._sut, confyml.Config)

    def test_should_return_list_of_configured_objects(self):
        objects = ['example_function']
        self.assertEqual(set(objects), set(self._sut._get_objects()))

    def test_should_return_config_for_object(self):
        actual = self._sut._get_config('example_function')
        expt = {'kwarg_1': 2,
                'kwarg_2': 'function_test',
                'kwarg_3': 'yaml_test'}
        self.assertDictEqual(expt, actual)

    def test_should_apply_config(self):
        confyml.set_config('resources/sample.config.yaml', mode='mcf')
        reload(sample_module)
        ret = sample_module.SampleClass().sample_method()
        self.assertEqual((2, 1), ret)
        ret = sample_module.sample_function()
        self.assertEqual(1, ret)

    def test_should_not_apply_config(self):
        os.environ['CONFYML_CONFIG'] = ''
        reload(sample_module)
        ret = sample_module.SampleClass().sample_method()
        self.assertEqual((1, None), ret)
        ret = sample_module.sample_function()
        self.assertEqual(None, ret)

    def test_should_be_overwritten_by_call(self):
        confyml.set_config('resources/sample.config.yaml', mode='mcf')
        reload(sample_module)
        ret = sample_module.sample_function_2(kwarg1=2)
        self.assertEqual(2, ret)
        ret = sample_module.sample_function_3()
        self.assertIsNone(ret)
