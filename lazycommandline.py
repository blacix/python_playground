import sys


class LazyCommandLine:
    def __init__(self):
        pass

    def stuff1(self, param):
        print('stuff1' + param)

    def stuff2(self, param1, param2):
        print('stuff' + param1 + param2)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        method_list = [func for func in dir(LazyCommandLine) if callable(getattr(LazyCommandLine, func)) and not func.startswith("_")]
        print(method_list)
        exit(1)

    method_name = sys.argv[1]
    params = ''
    if len(sys.argv) > 2:
        params = str(sys.argv[2])
    for i in range(3, len(sys.argv)):
        params += f', {sys.argv[i]}'

    stuff = LazyCommandLine()
    eval('stuff.' + method_name + '(' + params + ')')
