import cowsay
import camelcase
# import seaborn
# import matplotlib.pyplot as plt
cowsay.cow("Good Mooooorning!")
# seaborn.displot([2,4,6,8],kind="ecdf")
# plt.show()

c = camelcase.CamelCase()

txt = "hello world"

print(c.hump(txt))
print()
cowsay.cow("Good Nightttttttt!")