import random


def random_question():
    first_num = random.randint(0, 100)
    second_num = random.randint(0, 100)
    third_num = random.randint(0, 100)
    operator1 = random.choice(['+', '-', '*', '/'])
    operator2 = random.choice(['+', '-', '*', '/'])

    question = "{} {} {} {} {}".format(first_num, operator1, second_num, operator2, third_num)

    answer = int(eval(question))

    question += " = ?"

    print(question)


random_question()
