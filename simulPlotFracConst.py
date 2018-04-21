from random import *
import matplotlib.pyplot as plt
# current functionality: not able to perform match operation
numTrials = 20;
tempX = []
tempY = []

matrix = [[0 for i in range(numTrials)] for j in range(6)]
plt.ion()
animated_plot = plt.plot(tempX,tempY, 'ro')[0]
plt.ylim(0,1);
plt.xlim(0,200);
#plt.draw()
#plt.pause(0.5)


#matrix[0 = adversary, 1 = honest, 2 = state[0],3 = state[1], 4=state[2]][s]
print matrix
fracReward = 0.01
adv = 30;
total = 100;
numSlots = 200; #number of time slots
count = 0; # used to count number of trials exceeding threshold
#initialize matrix
reward = (total)*fracReward
for s in range (0, numTrials):
   matrix[0][s]= total*(adv/100.0);
   matrix[1][s] = total*((100.0-adv)/100.0)
   matrix[2][s] = 0;
   matrix[3][s] = reward;
   matrix[4][s] = 0;
   matrix[5][s] = adv/100.0;
for m in range (0,numSlots):
   # [a,h, 0 =irrelevant/1=relevant/2=active]
   for s in range (0,numTrials):
      adversary = matrix[0][s]   
      honest = matrix[1][s]
      a = matrix[2][s] #state[0]
      h = matrix[3][s] #state[1]
      state = [-1,-1,-1]
      randNum = random()
      alpha = adversary/(honest+adversary)
      reward = (adversary+honest)*fracReward
      if (alpha >= 0.33): #use selfish mining strategy
         if (h>a): #adopt
            #reward
            honest=honest+h
            #block generation
            if (randNum< alpha):
               state = [reward,0,0]
            else:
               state = [0,reward,0]
         #elif (a==1 and h==1 and state[2]==1) : #match (still needs to be implemented)
         elif (a>h): #override
            #reward
            adversary = adversary + h + reward   
            #block generation
            if (randNum < alpha):
               state = [a-h,0,0]
            else:      
               state = [a-h-reward,reward,1]
         else: #wait
            #block generation
            if (randNum < alpha):
               state = [a+reward,h,0] 
            else:
               state = [a,h+reward,1]
      else:
         if (randNum < alpha):
            adversary=adversary+reward
            state=[reward,0,0]
         else:
            honest= honest+reward
            state=[0,reward,0]
      matrix[0][s] = adversary
      matrix[1][s] = honest
      matrix[2][s] = state[0]
      matrix[3][s] = state[1]
      matrix[4][s] = state[2]
      matrix[5][s] = adversary / (adversary + honest)
   print matrix[0]
   print matrix[1]
   tempX = tempX  + [m for i in range(numTrials)]
   tempY = tempY + matrix[5]
   animated_plot.set_xdata(tempX)
   animated_plot.set_ydata(tempY)
   plt.draw()
   plt.pause(.1)
