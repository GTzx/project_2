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
            self.assertTrue(0 <= number < 10)

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

    def test_convert_fraction(self):
        # 测试convert_fraction函数是否正确将假分数转换为带分数
        test_num1 = '5/3'  # 带分数为 1‘2/3
        test_num2 = '34/11'  # 带分数为 3’1/11
        test_num3 = '59/8'  # 带分数为 7‘3/8
        test_num4 = '2612/315'  # 带分数为 8‘92/315
        test_num5 = '383/40'  # 带分数为 9‘23/40
        converted_test_num1 = '1‘2/3'
        converted_test_num2 = '3’1/11'
        converted_test_num3 = '7‘3/8'
        converted_test_num4 = '8‘92/315'
        converted_test_num5 = '9‘23/40'
        if convert_fraction(test_num1) == converted_test_num1 and convert_fraction(test_num2) == converted_test_num2 and convert_fraction(test_num3) == converted_test_num3 and convert_fraction(test_num4) == converted_test_num4 and convert_fraction(test_num5) == converted_test_num5:
            self.assertTrue(1)
        else:
            self.assertFalse(0)

    def test_add_parentheses(self):
        # 测试 add_parentheses 函数是否能正常为所有数加个括号
        exp1 = "1 - 0 ÷ 4/5 - 3/7"  # 加括号后为 (1 )-( 0 )÷( 4/5 )-( 3/7)
        exp2 = "7 + 2 - 4 ÷ 3/7"  # 加括号后为 (7 )+( 2 )-( 4 )÷( 3/7)
        exp3 = "1/4 ÷ 2 - 6/7"  # 加括号后为 (1/4 )÷( 2 )-( 6/7)
        exp4 = "4/5 × 6 + 1/3"  # 加括号后为 (4/5 )×( 6 )+( 1/3)
        exp5 = "2 × 5/8"  # 加括号后为 (2 )×( 5/8)

        pare_exp1 = "(1 )-( 0 )÷( 4/5 )-( 3/7)"
        pare_exp2 = "(7 )+( 2 )-( 4 )÷( 3/7)"
        pare_exp3 = "(1/4 )÷( 2 )-( 6/7)"
        pare_exp4 = "(4/5 )×( 6 )+( 1/3)"
        pare_exp5 = "(2 )×( 5/8)"

        if add_parentheses(exp1) == pare_exp1 and add_parentheses(exp2) == pare_exp2 and add_parentheses(exp3) == pare_exp3 and add_parentheses(exp4) == pare_exp4 and add_parentheses(exp5) == pare_exp5:
            self.assertTrue(1)
        else:
            self.assertFalse(0)

    def test_grade_questions(self):
        # 测试grade_questions函数是否正确统计正确和错误的题目
        correct_indices, wrong_indices = grade_questions("test_exercises.txt", "test_answers.txt")
        self.assertEqual(len(correct_indices), 5)
        self.assertEqual(len(wrong_indices), 5)

    # 异常处理
    def test_invalid_file_paths(self):
        # 文件不存在的情况
        self.assertEqual(grade_questions('non_existent_file.txt', 'non_existent_file.txt'), FileNotFoundError)

    def test_generate_expression(self):
        # 测试generate_expression函数生成的表达式是否合法
        for _ in range(100):
            expression, expression_1 = generate_expression(10)
            if Fraction(eval(expression.replace('÷', '/').replace('×', '*'))) == ZeroDivisionError:
                self.assertFalse(0)
            else:
                self.assertTrue(1)


if __name__ == "__main__":
    unittest.main()
