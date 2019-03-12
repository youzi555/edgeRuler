if __name__ == '__main__':
    func = "def fact(n): " \
           "\n\tif n==1:" \
           "\n\t\treturn 1 " \
           "\n\telse:" \
           "\n\t\treturn n*fact(n-1)"
    print(func)
    exec(func)
    a = fact(5)
    print(a)