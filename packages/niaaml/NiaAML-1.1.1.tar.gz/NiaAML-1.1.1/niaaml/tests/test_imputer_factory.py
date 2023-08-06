from unittest import TestCase
from niaaml.preprocessing.imputation import Imputer, ImputerFactory

class ImputerFactoryTestCase(TestCase):
    def setUp(self):
        self.__factory = ImputerFactory()
    
    def test_get_result_works_fine(self):
        for entry in self.__factory._entities:
            instance = self.__factory.get_result(entry)
            self.assertIsNotNone(instance)
            self.assertIsInstance(instance, Imputer)
        
        with self.assertRaises(TypeError):
            self.__factory.get_result('non_existent_name')
    
    def test_get_dictionary_works_fine(self):
        d = self.__factory.get_name_to_classname_mapping()
        d_keys = d.keys()
        e_keys = self.__factory._entities.keys()

        self.assertEqual(len(e_keys), len(d_keys))
        
        for k in d:
            self.assertIsNotNone(d[k])