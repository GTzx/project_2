# project_2
软工结对项目

需求：实现一个自动生成小学四则运算题目的命令行程序

此程序采用python编写

用法: 本程序有两个功能

-- 生成题目：需提供需要生成的题目数量 n 和数值范围 r

-- 正确答案统计：需提供题目文件和答案文件

注意：虽然在文件夹中有requirements.txt，但由于程序中所用的库均为python内置的，所以requirements.txt里内容为空，在此进行说明。

main.py 为主程序

test_main.py 为测试程序

Exercises_10000.txt 为生成的一万道题目，生成参数为 -n 10000 -r 100

test_exercises.txt 和 test_answers.txt 是统计答案正确和错误数量功能的文件，文件里有20道题目，我们手工计算题目答案并修改10道正确答案，程序统计的结果与修改后的结果一致。

-- Correct: 10 (6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

-- Wrong: 10 (1, 2, 3, 4, 5, 16, 17, 18, 19, 20)


