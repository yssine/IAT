import matplotlib.pyplot as plt
import glob, pygame, playsound
from time import sleep



# print(glob.glob('visualisation/Q_SXY_E19000_S500_G0.95_I0.7_F0.05.csv'))
def navidad(s):
    f=open(s,"r")
    x,y,r=[],[],[]
    for line in [line.rstrip() for line in f]:
        a=line.split(",")
        if a[0] and a[-1]:
            x.append(int(a[0]))
            y.append(round(float(a[-1]),2))
            r.append(int(float(a[2])))
    f.close()
    return x,y,r

# x1900,y1900,r1900=navidad("visualisation/Q_SXY_E1900_S500_G0.95_I0.7_F0.05.csv")
x1900,y1900,r1900=navidad("visualisation/Q_SXY_E19000_S500_G0.95_I0.7_F0.05.csv")
x10,y10,r10=navidad("visualisation/Q_SXY_E10_S10_G0.95_I0.7_F0.05.csv")
x19000,y19000,r19000=navidad("visualisation/Q_SXY_E19000_S500_G0.95_I0.7_F0.05.csv")
x200,y200,r200=navidad("visualisation/Q_SXY_E200_S5000_G0.95_I0.7_F0.05.csv")


x1900=[i//10 for i in x1900] #to get the convincing stats XD
# # Median Developer Salaries by Age
# dev_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]

# dev_y = [38496, 42000, 46752, 49320, 53200,
#          56000, 62316, 64928, 67317, 68748, 73752]
# print(x)
plt.plot(x1900, y1900,"r")
# plt.plot([y1900[-1]*1.05]*25000,"b--")
# plt.plot(x1900, r1900,"go")
# plt.xlabel('Numéro d\'épisode')
plt.xlabel('The num of episodes')
# plt.ylabel('Somme des valeurs de la fonction Q')
plt.ylabel('The sum of Q function')
# plt.title('Somme des valeurs de la fonction Q en fonction de l\'épisode')
plt.title('The sum of Q func by the num of episodes')
plt.show()





# import matplotlib.pyplot as plt

# fig, ax = plt.subplots()

# E_S = ['E:10,S:10', 'E:19000,S:500', 'E:1900,S:500', 'E:200,S:5000']
# Hight_score = [2, 87, 470, 112]
# bar_labels = ['red', 'blue', '_red', 'orange']
# bar_colors = ['tab:green', 'tab:blue', 'tab:red', 'tab:orange']

# rects = ax.bar(E_S, Hight_score,
#     # label=bar_labels,
#     color=bar_colors)

# ax.set_ylabel('Hight Score')
# ax.set_title('Hight_score by n_episodes and max steps')
# # ax.legend(title='Fruit color')
# # for i, v in enumerate(Hight_score):
# #     ax.text(10, 20, str(v), color='black', fontweight='bold')
# for rect in rects:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
#                '%d' % int(height),
#                ha='center', va='bottom')


# plt.show()




pygame.mixer.init()


lose = pygame.mixer.Sound("game/data/sad-trombone.mp3")
# lose.play()
# lose = pygame.mixer.Sound("game/data/defeat.mp3")
# lose.play()
# lose = pygame.mixer.Sound("game/data/missing-ping.mp3")
# lose.play(3)
sleep(4)
