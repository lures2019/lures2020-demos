import cursor as cursor
import numpy as np
from matplotlib import pyplot as plt, font_manager

list00 = ['2019-04-24', '2019-04-25', '2019-04-26', '2019-04-27', '2019-05-02']
list01 = [180, 60, 90, 10, 80]

x = list00
y = list01

plt.title("DUAN PING SHU LIANG FEN XI")
plt.xlabel("TIME")
plt.ylabel("SHU LIANG")
plt.plot(x, y)
plt.show()
