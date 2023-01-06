import random, time


def bubble_sort(array):
    while True:
        changed = False
        for i in range(len(array)-1):
            if array[i] > array[i+1]:
                a = array[i+1]
                array[i+1] = array[i]
                array[i] = a
                changed = True

        if(changed == False):
            return array




def merge(l, r):
    n=[]
    while len(l) != 0 and len(r) != 0:

        if l[0] <= r[0]:
            n.append(l[0])
            l.pop(0)
        else:
            n.append(r[0])
            r.pop(0)
    while len(l) != 0:
        n.append(l[0])
        l.pop(0)
    while len(r) !=0:
        n.append(r[0])
        r.pop(0)
    return n


def merge_sort(array):
    if len(array) < 2:
        return array
    else:
        l = array[:round(len(array) / 2)]
        r = array[round(len(array)/2):]
        l = merge_sort(l)
        r = merge_sort(r)
        return merge(l, r)







array = []
for i in range(11000):
    array.append(random.randint(1, 1000))


t0 = time.time()
bubble_sort(array)
t1 = time.time()
merge_sort(array)
t2 = time.time()

print(format(t1-t0))
print(format(t1-t2))

