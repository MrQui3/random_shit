import matplotlib.pyplot as plt

array = [1000]

for i in range(200):
    if i % 30 == 0:
        array[i] -= 100
    array.append(round(array[i] + array[i]*0.004, 2))




plt.plot(array)
plt.ylabel('some numbers')
plt.show()