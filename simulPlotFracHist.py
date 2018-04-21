from random import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# current functionality: not able to perform match operation
numTrials = 20;
tempX = []
tempY = []

matrix = [[0 for i in range(numTrials)] for j in range(6)] #adversary matrix
honestMatrix = [[0 for i in range(numTrials)] for j in range(6)]


plt.ion()

#matrix[0 = adversary, 1 = honest, 2 = state[0],3 = state[1], 4=state[2], 5 = alpha][s]
print matrix
fracReward = 0.01
adv = 30;
total = 100;
numSlots = 50; #number of time slots
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
  
   honestMatrix[0][s]= total*(adv/100.0);
   honestMatrix[1][s] = total*((100.0-adv)/100.0)
   honestMatrix[2][s] = 0;
   honestMatrix[3][s] = reward;
   honestMatrix[4][s] = 0;
   honestMatrix[5][s] = adv/100.0;

for m in range (0,numSlots):
   print (numSlots-m), " slots left"
     
   # [a,h, 0 =irrelevant/1=relevant/2=active]
   for s in range (0,numTrials):
      randNum = random()
      
      #adversary update phase
      adversary = matrix[0][s]   
      honest = matrix[1][s]
      a = matrix[2][s] #state[0]
      h = matrix[3][s] #state[1]
      state = [-1,-1,-1]
      
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

      #honest update phase
      adversary = honestMatrix[0][s]   
      honest = honestMatrix[1][s]
      a = honestMatrix[2][s] #state[0]
      h = honestMatrix[3][s] #state[1]
      state = [-1,-1,-1]
      alpha = adversary/(honest+adversary)
      reward = (adversary+honest)*fracReward
   
      if (randNum < alpha):
         adversary = adversary+1
      else:
         honest=honest+1
      honestMatrix[0][s] = adversary
      honestMatrix[1][s] = honest
      honestMatrix[5][s] = adversary / (adversary + honest)

   print matrix[0]
   print matrix[1]
   #tempX = tempX  + [m for i in range(numTrials)]
   #tempY = tempY + matrix[5]
   #animated_plot.set_xdata(tempX)
   #animated_plot.set_ydata(tempY)
   
   #testing doubled
   densityY = stats.gaussian_kde(honestMatrix[5])
   
   density = stats.gaussian_kde(matrix[5])

   nY, xY, _ = plt.hist(honestMatrix[5], bins = np.linspace(0,.5,200), histtype = u'step', normed = True)
   n, x, _ = plt.hist(matrix[5],bins = np.linspace(0,.5,200), histtype = u'step', normed = True)
   plt.clf()
   plt.cla()
   plt.close()
   plt.plot(xY, densityY(xY))
   plt.plot(x,density(x)) 
   plt.show()
   plt.pause(.1)
