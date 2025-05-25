#arg => argment 可以處理任意數量的參數  * => tuplekwarg
#kwarg =>
def add(*args):
    total=0
    for arg in args:
        print(f"arg:{arg}")
        total+=arg
    return total
print(add(1,2,3,4))

#print_info 印出資訊
def print_info(**kwargs):
    for key,value in kwargs.items():
        print(f"key: {key} value: {value}")
print_info(name="daniel",age="16",career="student")