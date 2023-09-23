import random
from fractions import Fraction

# 定义运算符
operators = ['+', '-', '×', '÷']


# 生成随机数
def generate_number(range_limit):
    if random.random() < 0.5:  # 50% 的概率生成真分数
        numerator = random.randint(1, range_limit)
        denominator = random.randint(numerator + 1, range_limit + 1)
        return Fraction(numerator, denominator)
    else:  # 50% 的概率生成自然数
        return random.randint(1, range_limit)


# 生成算术表达式
def generate_expression(range_limit):
    if range_limit < 1:
        raise ValueError("数值范围必须大于等于1")
    num1 = generate_number(range_limit)
    num2 = generate_number(range_limit)
    operator = random.choice(operators)

    # 保证除法结果是真分数
    if operator == '÷':
        while num2 == 0 or (operator == '÷' and num1 % num2 != 0):
            num1 = generate_number(range_limit)
            num2 = generate_number(range_limit)

    return f"{num1} {operator} {num2}"


# 转换小数为分数表示
def convert_to_fraction(decimal_result):
    return Fraction(decimal_result).limit_denominator()

# 生成题目和答案
def generate_questions_and_answers(num_questions, range_limit):
    questions = []
    answers = []
    for _ in range(num_questions):
        expression = generate_expression(range_limit)
        decimal_result = eval(expression.replace('÷', '/').replace('×', '*'))
        fraction_result = convert_to_fraction(decimal_result)
        questions.append(expression)
        answers.append(fraction_result)
    return questions, answers


# 将题目和答案保存到文件
def save_to_files(questions, answers):
    with open("Exercises.txt", "w", encoding='utf-8') as exercise_file, open("Answers.txt", "w", encoding='utf-8') as answer_file:
        for i, (question, answer) in enumerate(zip(questions, answers), start=1):
            exercise_file.write(f"题目{i}：  {question}\n")
            answer_file.write(f"答案{i}：  {answer}\n")


# 判定答案是否正确
def is_answer_correct(expression, user_answer, correct_answer):
    return user_answer == correct_answer


# 统计对错题目
def grade_questions(exercise_file, answer_file):
    correct_indices = []
    wrong_indices = []

    with open(exercise_file, "r", encoding='utf-8') as exercises, open(answer_file, "r", encoding='utf-8') as answers:
        for i, (exercise, answer) in enumerate(zip(exercises, answers), start=1):
            exercise = exercise.strip()
            answer = answer.strip()

            # 检查题目行是否以"题目X："开头（X是题目编号）
            if exercise.startswith("题目"):
                parts = exercise.split("：", 1)
                if len(parts) == 2:
                    current_question = int(parts[0].replace("题目", "").strip())
                    exercise = parts[1].strip()
            # 检查答案行是否以"答案X："开头（X是题目编号）
            if answer.startswith("答案"):
                parts = answer.split("：", 1)
                if len(parts) == 2:
                    current_question = int(parts[0].replace("答案", "").strip())
                    answer = parts[1].strip()

            try:
                user_answer = eval(answer.replace('÷', '/').replace('×', '*'))
                user_answer = Fraction(user_answer).limit_denominator()  # 将小数答案转换为分数表示
                correct_answer = eval(exercise.replace('÷', '/').replace('×', '*'))
                correct_answer = Fraction(correct_answer).limit_denominator()  # 将小数答案转换为分数表示

                if is_answer_correct(exercise, user_answer, correct_answer):
                    correct_indices.append(i)
                else:
                    wrong_indices.append(i)
            except Exception as e:
                print(f"在评分第 {i} 题时发生错误：{e}")

    return correct_indices, wrong_indices


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
        # e = 'Exercises.txt'
        # a= 'Answers.txt'
        e = 'test_exercises.txt'
        a = 'test_answers.txt'
        correct_indices, wrong_indices = grade_questions(e, a)
        save_grade_to_file(correct_indices, wrong_indices)
        print(f"评分结果已保存到 Grade.txt 文件中")






