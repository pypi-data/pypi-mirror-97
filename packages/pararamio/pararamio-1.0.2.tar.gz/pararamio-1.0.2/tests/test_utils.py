# noqa
import unittest

from pararamio.utils.helpers import lazy_loader


# noinspection PyTypeChecker
class UtilsTestCase(unittest.TestCase):
    def test_001_lazy_loader(self):
        items = list(range(0, 50))
        calls_count = 0

        def load_more(_, items):
            nonlocal calls_count
            calls_count += 1
            return items

        self.assertListEqual(items, list(lazy_loader({}, items, load_more, per_load=25)), 'returned lists not equals')
        self.assertEqual(calls_count, 2, 'Calls count is not equal 2')

if __name__ == '__main__':
    unittest.main()
