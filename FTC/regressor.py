import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


hypos = np.array([])
powers = np.array([])


with open('ftc\\test_data.csv', newline='') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        for hypo in range(0, len(row), 2):
            try:
                np.append(hypos, row[hypo])
            except IndexError:
                break
        hypos = hypos[:-1]
        for power in range(1, len(row), 2):
            try:
                np.append(powers, row[power])
            except IndexError:
                break


fig, ax = plt.subplots()
ax.scatter(x=hypos, y=powers, marker='o')
plt.show()


x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
y = np.array([5, 20, 14, 32, 22, 38])
model = LinearRegression(fit_intercept=True).fit(x, y)
