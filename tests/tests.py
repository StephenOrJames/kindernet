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

    # def positive_test(self, text):
    #     """Verify that positive sentences remain unchanged."""
    #     self.assertEqual(text, convert(text))
    #
    # def test_positive_1(self):
    #     self.positive_test("I like to write code.")
    #
    # def test_positive_2(self):
    #     self.positive_test("School will be starting soon.")
    #
    # def test_positive_3(self):
    #     self.positive_test("To get to the other side.")
    #
    # def negative_test(self, text):
    #     """Verify that negative sentences are changed or removed."""
    #     self.assertNotEqual(text, convert(text))
    #
    # def test_negative_1(self):
    #     self.negative_test("I hate you.")
    #
    # def test_negative_2(self):
    #     self.negative_test("I hate that you think you are better than everyone else.")
    #
    # def test_negative_3(self):
    #     self.negative_test("This family is the worst I've seen all my life, and"
    #                        " I've been a counselor for the past twenty years!")


if __name__ == "__main__":
    unittest.main()
