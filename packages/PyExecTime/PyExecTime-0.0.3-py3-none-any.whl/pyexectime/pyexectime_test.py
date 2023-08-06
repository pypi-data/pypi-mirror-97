from pyexectime.inspector import PyExecTime, py_exec_time

def test_clm():
    with PyExecTime():
        for i in range(10000):
            print(i, end= ' ')


@py_exec_time()
def test_dec(j):
    for i in range(j):
        print(i, end= ' ')

