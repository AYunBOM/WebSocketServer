from threading import Timer

answer = ''

def timeout_function():
    global answer
    if answer == "":
        print("1 {}".format(answer))
    else:
        print("답: {}".format(answer))

t = Timer(5, timeout_function)
t.start()

prompt = "You have {} seconds to choose the correct answer...\n".format(5)
answer = input(prompt)
print("1 {}".format(answer))
t.cancel()
print("2 {}".format(answer))