import time


class Test:
    def __init__(self):
        self.x = 1

    @staticmethod
    def func():
        return 1

    def my_func(self):
        p = self.func()
        print('p=', p)


if __name__ == '__main__':
    test = Test()
    for i in range(10):
        print(i)
        if i == 2 or i == 9:
            try:
                data = __import__('robot_move').func
                test.func = data
            except Exception as e:
                print(e)
        time.sleep(1)
        try:
            test.my_func()
        except Exception as e:
            print('e', e)
