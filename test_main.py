# from zx
# time 2023/9/22 22:54

import unittest
from main import *


class TestArithmeticGenerator(unittest.TestCase):

    def test_generate_number(self):
        # 测试generate_number函数生成的数是否在合理范围内
        for _ in range(100):
            number = generate_number(10)
            if isinstance(number, int):
                self.assertTrue(1 <= number <= 10)
            elif isinstance(number, Fraction):
            #     self.assertTrue(1 <= number.numerator <= 10)
            #     self.assertTrue(1 <= number.denominator <= 10)
            #     self.assertTrue(1.0 <= float(number) <= 10.0)
                decimal_value = float(number.numerator) / float(number.denominator)
                self.assertTrue(1.0 <= decimal_value <= 10.0)

    def test_generate_expression(self):
        # 测试generate_expression函数生成的表达式是否合法
        for _ in range(100):
            expression = generate_expression(10)
            self.assertTrue(self.is_valid_expression(expression))

    def test_convert_to_fraction(self):
        # 测试convert_to_fraction函数是否正确将小数转换为分数
        decimal_values = [0.25, 0.5, 0.75, 1.2, 2.5]
        expected_fractions = [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(6, 5), Fraction(5, 2)]
        for decimal, expected in zip(decimal_values, expected_fractions):
            result = convert_to_fraction(decimal)
            self.assertEqual(result, expected)

    def test_is_answer_correct(self):
        # 测试is_answer_correct函数是否正确判定答案是否正确
        self.assertTrue(is_answer_correct("2 + 3", Fraction(5, 1), Fraction(5, 1)))
        self.assertTrue(is_answer_correct("1/2 + 1/3", Fraction(5, 6), Fraction(5, 6)))
        self.assertFalse(is_answer_correct("3 × 4", Fraction(12, 1), Fraction(7, 2)))

    def test_grade_questions(self):
        # 测试grade_questions函数是否正确统计正确和错误的题目
        correct_indices, wrong_indices = grade_questions("test_exercises.txt", "test_answers.txt")
        self.assertEqual(len(correct_indices), 5)
        self.assertEqual(len(wrong_indices), 5)

    def is_valid_expression(self, expression):
        # 辅助函数，用于检查生成的表达式是否合法
        operators = ['+', '-', '×', '÷']
        parts = expression.split()
        if len(parts) != 3:
            return False
        if not parts[0].isdigit() and not parts[0].count("/") == 1:
            return False
        if parts[1] not in operators:
            return False
        if not parts[2].isdigit() and not parts[2].count("/") == 1:
            return False
        return True


if __name__ == "__main__":
    unittest.main()
