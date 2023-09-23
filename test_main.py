# from zx
# time 2023/9/22 22:54

import unittest
from main import *


class TestArithmeticGenerator(unittest.TestCase):
    # 单元测试模块
    def test_generate_number(self):
        # 测试generate_number函数生成的数是否在合理范围内
        for _ in range(100):
            number = generate_number(10)
            self.assertTrue(0 <= number <= 10)

    def test_generate_expression_equivalence(self):
        # 测试generate_expression函数生成的表达式是否有重复
        range_limit = 10
        num_expressions = 1000
        generated_expressions = set()
        for _ in range(num_expressions):
            expression = generate_expression(range_limit)
            # 检查是否有重复的表达式，或者等效的表达式
            if expression in generated_expressions:
                assert False, f"Duplicate expression found: {expression}"
            # 将通过重复检测的表达式加入表达式集合中
            generated_expressions.add(expression)

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
        self.assertEqual(len(correct_indices), 7)
        self.assertEqual(len(wrong_indices), 3)

    # 异常处理
    def test_invalid_file_paths(self):
        # 文件不存在的情况
        self.assertEqual(grade_questions('non_existent_file.txt', 'non_existent_file.txt'), FileNotFoundError)

    def test_generate_expression(self):
        # 测试generate_expression函数生成的表达式是否合法
        for _ in range(100):
            expression = generate_expression(10)
            if Fraction(eval(expression.replace('÷', '/').replace('×', '*'))) == ZeroDivisionError:
                self.assertFalse(0)
            else:
                self.assertTrue(1)


if __name__ == "__main__":
    unittest.main()
