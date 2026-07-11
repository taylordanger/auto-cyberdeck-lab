import unittest

from forge.led_bitmap_generator import (
    LED_HEIGHT,
    LED_WIDTH,
    generate_led_bitmap,
)


class TestLEDBitmapGenerator(unittest.TestCase):
    def test_default_bitmap_is_blank_60_by_9(self):
        bitmap = generate_led_bitmap()

        self.assertEqual(len(bitmap), LED_HEIGHT)
        self.assertTrue(all(len(row) == LED_WIDTH for row in bitmap))
        self.assertTrue(all(pixel == 0 for row in bitmap for pixel in row))

    def test_default_bitmap_rows_are_independent(self):
        bitmap = generate_led_bitmap()
        bitmap[0][0] = 1

        self.assertEqual(bitmap[0][0], 1)
        self.assertEqual(bitmap[1][0], 0)

    def test_separate_default_calls_are_independent(self):
        first = generate_led_bitmap()
        second = generate_led_bitmap()

        first[0][0] = 1

        self.assertEqual(second[0][0], 0)

    def test_valid_bitmap_is_copied(self):
        source = [[0] * LED_WIDTH for _ in range(LED_HEIGHT)]
        result = generate_led_bitmap(source)

        self.assertEqual(result, source)
        self.assertIsNot(result, source)
        self.assertTrue(
            all(result_row is not source_row for result_row, source_row in zip(result, source))
        )

    def test_boolean_pixels_are_normalized(self):
        source = [[False] * LED_WIDTH for _ in range(LED_HEIGHT)]
        source[0][0] = True

        result = generate_led_bitmap(source)

        self.assertEqual(result[0][0], 1)
        self.assertIs(type(result[0][0]), int)

    def test_rejects_wrong_height(self):
        with self.assertRaisesRegex(ValueError, "exactly 9 rows"):
            generate_led_bitmap([[0] * LED_WIDTH])

    def test_rejects_wrong_width(self):
        source = [[0] * LED_WIDTH for _ in range(LED_HEIGHT)]
        source[4] = [0] * (LED_WIDTH - 1)

        with self.assertRaisesRegex(ValueError, "row 4"):
            generate_led_bitmap(source)

    def test_rejects_invalid_pixel(self):
        source = [[0] * LED_WIDTH for _ in range(LED_HEIGHT)]
        source[3][12] = 2

        with self.assertRaisesRegex(ValueError, "row 3, column 12"):
            generate_led_bitmap(source)

    def test_rejects_string_bitmap(self):
        with self.assertRaises(TypeError):
            generate_led_bitmap("0" * (LED_WIDTH * LED_HEIGHT))


if __name__ == "__main__":
    unittest.main()