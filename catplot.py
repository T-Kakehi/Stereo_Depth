import csv
from matplotlib import pyplot as plt
from matplotlib import pyplot as Axes

DIRECTION = ["x","y","z"]

def scat_plot(ax, array, x, y):
    ax.set_title(str(DIRECTION[x]+"-"+DIRECTION[y]))
    ax.set_xlabel(DIRECTION[x])
    ax.set_ylabel(DIRECTION[y])
    return ax.scatter(array[x], array[y],s=1)

def motion(event):
    if event.button == 1:
        global cut_point
        global select
        x = event.xdata
        y = event.ydata
        if select == 1 or select == 3:
            line.set_xdata(int(x))
            cut_point = int(x)
        elif select == 2:
            line.set_ydata(int(y))
            cut_point = int(y)
        plt.draw()

print("What is the name of the file to be loaded?")
file_name = input("File name: ")
with open(str(file_name+'.csv')) as f:
    temp = []
    reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
    for i, row in enumerate(reader):
        print(DIRECTION[i]+": "+str(len(row)))
        temp.append(row)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=270, azim=90)
ax.scatter(temp[0], temp[1],temp[2],c=temp[2],cmap='jet',s=5)
plt.show()


fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
plt.connect('motion_notify_event', motion)


print("Which area to separate?\n1: y-z\n2: x-z\n3: x-y")
select = int(input("> "))

flag = True
while flag:
    print("How many separete "+DIRECTION[select-1]+" point?\nx: "+str(min(temp[select-1]))+" ~ "+str(max(temp[select-1])))
    cut_point = int(input("> "))
    if min(temp[select-1]) <= cut_point <= max(temp[select-1]):
        flag = False

while True:
    idx = -1
    result = [[],[],[]]
    for cnt in range(temp[select-1].count(cut_point)):
        idx = temp[select-1].index(cut_point, idx+1)
        result[0].append(int(temp[0][idx]))
        result[1].append(int(temp[1][idx]))
        result[2].append(int(temp[2][idx]))    

    if select == 1:
        plot1 = scat_plot(ax1, temp, 0, 1)
        line = ax1.axvline(cut_point, color="red")
        plot2 = scat_plot(ax2, result, 2, 1)
    elif select == 2:
        plot1 = scat_plot(ax1, temp, 0, 1)
        line = ax1.axhline(cut_point, color="red")
        plot2 = scat_plot(ax2, result, 0, 2)
    elif select == 3:
        plot1 = scat_plot(ax1, temp, 2, 1)
        line = ax1.axvline(cut_point, color="red")
        plot2 = scat_plot(ax2, result, 0, 1)
    
    fig.tight_layout()
    plt.pause(0.1)
    ax1.clear()
    ax2.clear()