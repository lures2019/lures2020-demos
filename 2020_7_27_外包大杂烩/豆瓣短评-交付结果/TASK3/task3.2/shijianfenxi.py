import cursor as cursor
import numpy as np
from matplotlib import pyplot as plt, font_manager

list00 = ['3:00','6:00', '12:00', '18:00', '24:00']
list01 = [3039, 1203, 890, 786, 5698]

x = list00
y = list01

plt.title("DUAN PING SHU LIANG")
plt.xlabel("SHI KE")
plt.ylabel("SHU LIANG")
plt.plot(x, y)
plt.show()
