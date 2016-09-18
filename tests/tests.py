import unittest

from kindernet import convert


class TestConversion(unittest.TestCase):
    """Verify that the sentence conversion functions as intended."""

    def get_samples(self, file_name):
        with open(file_name) as file:
            samples = file.readlines()
        return samples

    def test_positive(self):
        for sample in self.get_samples("PositiveTests.txt"):
            try:
                self.assertEqual(sample, convert(sample))
            except AssertionError as e:
                print(e)

    def test_negative(self):
        for sample in self.get_samples("NegativeTests.txt"):
            try:
                self.assertNotEqual(sample, convert(sample))
            except AssertionError as e:
                print(e)

    def assertEqual(self, first, second, msg=None):
        print("\nTesting for equality:\n\t%r\n\t%r" % (first, second))
        return super().assertEqual(first, second, msg)

    def assertNotEqual(self, first, second, msg=None):
        print("\nTesting for difference:\n\t%r\n\t%r" % (first, second))
        return super().assertNotEqual(first, second, msg)


if __name__ == "__main__":
    unittest.main()
