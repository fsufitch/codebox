print("Writing...")
with open('foo.out', 'w') as f:
    x = 1
    y = 1
    for i in range(20):
        print(x)
        f.write('%d\n' % x)
        x, y = y, x+y
print("Wrote file")

import os

print("Stuff in this dir:")
print(os.listdir("."))
