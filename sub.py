import csv
from matplotlib import pyplot as plt
from matplotlib import pyplot as Axes

DIRECTION = ["x","y","z"]

print("What a name of input file?")
file_name = input()
with open(str(file_name+'.csv')) as f:
    temp = []
    reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
    for i, row in enumerate(reader):
        print(DIRECTION[i]+": "+str(len(row)))
        temp.append(row)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=270, azim=90)
ax.scatter(temp[0], temp[1],temp[2],c=temp[2],cmap='jet')
plt.show()

print("How many cut point?\n1: y-z\n2: x-z\n3: x-y")
select = int(input())

flag = True
while flag:
    print("How many cut "+DIRECTION[select-1]+" point?\nx: "+str(min(temp[select-1]))+" ~ "+str(max(temp[select-1])))
    cut_point = int(input())
    if min(temp[select-1]) <= cut_point <= max(temp[select-1]):
        flag = False

idx = -1
result_x = []
result_y = []
result_z = []
for cnt in range(temp[select-1].count(cut_point)):
    idx = temp[select-1].index(cut_point, idx+1)
    result_y.append(temp[1][idx])
    result_z.append(temp[2][idx])

fig = plt.figure()

ax = fig.add_subplot(1,1,1)

ax.scatter(result_z,result_y)

ax.set_title('first scatter plot')
ax.set_xlabel('z')
ax.set_ylabel('y')

plt.show()