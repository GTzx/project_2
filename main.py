import math
import random
import re
from fractions import Fraction

# 定义运算符
operators = ['+', '-', '×', '÷']


# 生成随机数
def generate_number(range_limit):
    if random.random() < 0.5:  # 50% 的概率生成真分数
        numerator = random.randint(0, range_limit - 1)
        denominator = random.randint(numerator + 1, range_limit)
        return Fraction(numerator, denominator)
    else:  # 50% 的概率生成自然数
        return random.randint(0, range_limit - 1)


# 用集合来存储已生成的表达式
generated_expressions = set()


# 确保除法结果是真分数
def proper_fraction(range_limit, num1, num2):
    while num2 == 0 or num1 % num2 != 0:
        num1 = generate_number(range_limit)
        num2 = generate_number(range_limit)
    return num1, num2


# 生成一个运算符的表达式
def generate_one_expression(range_limit):
    num1 = generate_number(range_limit)
    num2 = generate_number(range_limit)
    operator1 = random.choice(operators)
    if operator1 == '÷':
        num1, num2 = proper_fraction(range_limit, num1, num2)
    while num1 == 0:
        num1 = generate_number(range_limit)
    # 确保不会出现通过交换律得到的表达式是一样的
    if operator1 in ('+', '×'):
        num1, num2 = min(num1, num2), max(num1, num2)
        if math.floor(num2) == 0:
            num2 = random.randint(1, range_limit)
        if min(num1, num2) == 0:
            num1 = random.randint(1, math.floor(num2))
    # 确保在计算过程中不会出现负数
    if operator1 == '-':
        num1, num2 = max(num1, num2), min(num1, num2)

    expression = f"{num1} {operator1} {num2}"
    expression_1 = f"({num1}) {operator1} ({num2})"

    return expression, expression_1


# def generate_two_expression(range_limit):
#     num1 = generate_number(range_limit)
#     num2 = generate_number(range_limit)
#     num3 = generate_number(range_limit)
#     nums = [num1, num2, num3]
#     sort_nums = sorted(nums)
#
#     # 随机选择两个不同的运算符
#     operators_subset = random.sample(operators, 2)
#     operator1, operator2 = operators_subset[0], operators_subset[1]
#
#     # 保证除法结果是真分数
#     if operator1 == '÷':
#         while num2 == 0:
#             num2 = generate_number(range_limit)
#     if operator2 == '÷':
#         while num3 == 0:
#             num3 = generate_number(range_limit)
#
#     # 确保不会出现通过交换律得到的表达式是一样的
#     if (operator1 == '+' and operator2 == '+') or (operator1 == '×' and operator2 == '×'):
#         num1, num2, num3 = sort_nums[0], sort_nums[1], sort_nums[2]
#
#     # 更新表达式中的数值以确保顺序正确
#     if operator1 == '-':
#         num1, num2 = max(num1, num2), min(num1, num2)
#     if operator2 == '-':
#         num2, num3 = max(num2, num3), min(num2, num3)
#
#     expression = f"{num1} {operator1} {num2} {operator2} {num3}"
#     expression_1 = f"({num1}) {operator1} ({num2}) {operator2} ({num3})"
#     return expression, expression_1

def generate_two_expression(range_limit):
    num3 = generate_number(range_limit)
    operators = ['+', '-']
    operator2 = random.choice(operators)
    exp1, exp1_1 = generate_one_expression(range_limit)
    if operator2 == '-':
        while eval(exp1_1.replace('÷', '/').replace('×', '*')) < num3:
            num3 = generate_number(range_limit)
    expression = f"{exp1} {operator2} {num3}"
    expression_1 = f"{exp1_1} {operator2} ({num3})"
    return expression, expression_1


# 生成三个运算符的表达式
def generate_three_expression(range_limit):
    operators_3 = ['+', '×', '÷']
    operator = random.choice(operators_3)
    exp1, exp1_1 = generate_one_expression(range_limit)
    exp2, exp2_1 = generate_one_expression(range_limit)
    expression = exp1 + ' ' + operator + ' ' + exp2
    expression_1 = exp1_1 + operator + exp2_1
    while eval(expression_1.replace('÷', '/').replace('×', '*')) < 0:
        exp1, exp1_1 = generate_one_expression(range_limit)
        exp2, exp2_1 = generate_one_expression(range_limit)
        expression = exp1 + ' ' + operator + ' ' + exp2
        expression_1 = exp1_1 + operator + exp2_1
    return expression, expression_1


# 生成算术表达式
def generate_expression(range_limit):
    if range_limit < 1:
        raise ValueError("数值范围必须大于等于1")

    while True:
        yunsuanfu_num = random.randint(1, 3)

        if yunsuanfu_num == 1:
            expression, expression_1 = generate_one_expression(range_limit)
        elif yunsuanfu_num == 2:
            expression, expression_1 = generate_two_expression(range_limit)
        else:
            expression, expression_1 = generate_three_expression(range_limit)

        # 检查是否已生成过这个表达式，如果是则重新生成
        if expression not in generated_expressions:
            generated_expressions.add(expression)
            return expression, expression_1


# 转换小数为分数表示
def convert_to_fraction(decimal_result):
    return Fraction(decimal_result).limit_denominator()


# 把假分数结果转换为带分数
def convert_fraction(s):
    # 把字符串分割成分子和分母
    numerator, denominator = map(int, s.split('/'))
    # 判断分子是否大于等于分母，如果是，就进行转换
    if numerator >= denominator:
        # 计算整数部分和余数部分
        integer = numerator // denominator
        remainder = numerator % denominator
        # 如果余数为零，就返回整数部分
        if remainder == 0:
            return str(integer)
        # 否则，就返回带分数的形式
        else:
            return f"{integer}‘{remainder}/{denominator}"
    # 否则，就返回原来的字符串
    else:
        return s


# 生成题目和答案
def generate_questions_and_answers(num_questions, range_limit):
    questions = []
    answers = []
    for _ in range(num_questions):
        expression, expression_1 = generate_expression(range_limit)
        decimal_result = eval(expression_1.replace('÷', '/').replace('×', '*'))
        # while decimal_result < 0:
        #     expression, expression_1 = generate_expression(range_limit)
        #     decimal_result = eval(expression_1.replace('÷', '/').replace('×', '*'))
        fraction_result = convert_to_fraction(decimal_result)
        if isinstance(fraction_result, int) == False and fraction_result % 1 != 0:
            fraction_result = convert_fraction(f"{Fraction(fraction_result).limit_denominator()}")
        questions.append(expression)
        answers.append(fraction_result)
    return questions, answers


# 将题目和答案保存到文件
def save_to_files(questions, answers):
    with open("Exercises.txt", "w", encoding='utf-8') as exercise_file, open("Answers.txt", "w",
                                                                             encoding='utf-8') as answer_file:
        for i, (question, answer) in enumerate(zip(questions, answers), start=1):
            exercise_file.write(f"题目{i}：  {question}\n")
            answer_file.write(f"答案{i}：  {answer}\n")


# 为所有数加个括号以保证能够正确运算
def add_parentheses(s):
    # 初始化一个空列表，用来存储字符串中的数字和运算符
    tokens = []
    # 初始化一个空字符串，用来存储当前的数字
    num = ''
    # 遍历字符串中的每个字符
    for c in s:
        # 如果字符是运算符，就把之前的数字加入到列表中，并把运算符也加入到列表中，然后清空数字字符串
        if c in '+-×÷':
            tokens.append(num)
            tokens.append(c)
            num = ''
        # 否则，就把字符加入到数字字符串中
        else:
            num += c
    # 把最后一个数字也加入到列表中
    tokens.append(num)
    # 初始化一个空字符串，用来存储结果
    result = ''
    # 遍历列表中的每个元素
    for i, token in enumerate(tokens):
        # 如果元素是运算符，就直接加入到结果中
        if token in '+-×÷':
            result += token
        # 否则，元素是数字，就加上括号
        else:
            result += '(' + token + ')'
    # 返回结果字符串
    return result


# 统计对错题目
def grade_questions(exercise_file, answer_file):
    correct_indices = []
    wrong_indices = []

    try:
        with open(exercise_file, "r", encoding='utf-8') as exercises, open(answer_file, "r",
                                                                           encoding='utf-8') as answers:
            for i, (exercise, answer) in enumerate(zip(exercises, answers), start=1):
                exercise = exercise.strip()
                answer = answer.strip()

                # 检查题目行是否以"题目X："开头（X是题目编号）
                if exercise.startswith("题目"):
                    parts = exercise.split("：", 1)
                    if len(parts) == 2:
                        exercise = parts[1].strip()
                # 检查答案行是否以"答案X："开头（X是题目编号）
                if answer.startswith("答案"):
                    parts = answer.split("：", 1)
                    if len(parts) == 2:
                        answer = parts[1].strip()

                try:
                    user_answer = eval(answer.replace('‘', '+'))
                    user_answer = Fraction(user_answer).limit_denominator()  # 将小数答案转换为分数表示
                    correct_answer = eval(add_parentheses(exercise).replace('÷', '/').replace('×', '*'))
                    correct_answer = Fraction(correct_answer).limit_denominator()  # 将小数答案转换为分数表示

                    if user_answer == correct_answer:
                        correct_indices.append(i)
                    else:
                        wrong_indices.append(i)
                except Exception as e:
                    print(f"在评分第 {i} 题时发生错误：{e}")

        return correct_indices, wrong_indices
    except FileNotFoundError:
        print(f"文件不存在")
        return FileNotFoundError


# 保存评分结果到文件
def save_grade_to_file(correct_indices, wrong_indices):
    with open("Grade.txt", "w") as grade_file:
        grade_file.write(f"Correct: {len(correct_indices)} ({', '.join(map(str, correct_indices))})\n")
        grade_file.write(f"Wrong: {len(wrong_indices)} ({', '.join(map(str, wrong_indices))})\n")


if __name__ == "__main__":

    # 设计题目生成和正确答案统计两个功能入口
    print("功能按键\n生成题目：1\t正确答案统计：2\n")
    a = int(input("请输入数字（1/2）："))
    if a == 1:
        n = int(input("请输入题目数量n："))
        r = int(input("请输入数值的范围："))
        questions, answers = generate_questions_and_answers(n, r)
        save_to_files(questions, answers)
        print(f"生成 {n} 题并保存到 Exercises.txt 和 Answers.txt 文件中")

    elif a == 2:
        # e = input("请输入题目文件e：")
        # a = input("请输入答案文件a：")
        e = 'Exercises.txt'
        a = 'Answers.txt'
        # 测试功能是否正常
        # e = 'test_exercises.txt'
        # a = 'test_answers.txt'
        correct_indices, wrong_indices = grade_questions(e, a)
        save_grade_to_file(correct_indices, wrong_indices)
        print(f"统计结果已保存到 Grade.txt 文件中")
