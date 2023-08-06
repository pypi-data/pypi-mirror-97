import sys

#x = {}
#q = {}
#z = {}

#@profile
def main():
    x = {}
    z = {}
    a = 1
    for i in range(2000000):
        x = {"hello everybody" : x }
        # print(total_size(x))

        z = {"x" : 1 }
        # del z
        a = a + 1
        # del a
    #    q = {"quack" : 1 }
    #    r = {"x" : 1 }

    # print(x)
    print(len(x))

main()
