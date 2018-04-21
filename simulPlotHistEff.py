from random import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# current functionality: not able to perform match operation
numTrials = 20;
tempX = []
tempY = []

matrix = [[[0 for i in range(numTrials)] for j in range(6)] for k in range(4)]  #adversary matrix
# i = number of Trials
# j = amount of information per trial
# k = number of different strategies/initial setups per trial (if k is even, use honest, else SM1 hybrid)


honestMatrix = [[0 for i in range(numTrials)] for j in range(6)]


plt.ion()

#matrix[0 = adversary, 1 = honest, 2 = state[0],3 = state[1], 4=state[2], 5 = alpha][s]
print matrix
fracReward = 0.01
adv = 30;
numSlots = 200; #number of time slots
count = 0; # used to count number of trials exceeding threshold
#initialize matrix
for s in range (0, numTrials):
   total = 50;
   reward = 1;
   for t in range (0, 2):
      matrix[t][0][s]= total*(adv/100.0);
      matrix[t][1][s] = total*((100.0-adv)/100.0)
      matrix[t][2][s] = 0;
      matrix[t][3][s] = reward;
      matrix[t][4][s] = 0;
      matrix[t][5][s] = adv/100.0;
   total = 200;
   reward = 1; #(total)*fracReward
   for t in range (2, 4):
      matrix[t][0][s]= total*(adv/100.0);
      matrix[t][1][s] = total*((100.0-adv)/100.0)
      matrix[t][2][s] = 0;
      matrix[t][3][s] = reward;
      matrix[t][4][s] = 0;
      matrix[t][5][s] = adv/100.0;

for m in range (0,numSlots):
   print (numSlots-m), " slots left"
     
   # [a,h, 0 =irrelevant/1=relevant/2=active]
   for s in range (0,numTrials):
      randNum = random()
     
      for t in range(0,4):
        
         #adversary update phase
         adversary = matrix[t][0][s]   
         honest = matrix[t][1][s]
         a = matrix[t][2][s] #state[0]
         h = matrix[t][3][s] #state[1]
         state = [-1,-1,-1]
         alpha = adversary/(honest+adversary)
         reward = 1; #(adversary+honest)*fracReward
        
         if (t%2 == 1): # adversary 
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
         else: #honest
            if (randNum < alpha):
               adversary = adversary+1
            else:
               honest=honest+1
         matrix[t][0][s] = adversary
         matrix[t][1][s] = honest
         matrix[t][2][s] = state[0]
         matrix[t][3][s] = state[1]
         matrix[t][4][s] = state[2]
         matrix[t][5][s] = adversary / (adversary + honest)
   #tempX = tempX  + [m for i in range(numTrials)]
   #tempY = tempY + matrix[5]
   #animated_plot.set_xdata(tempX)
   #animated_plot.set_ydata(tempY)
   
   #testing for multiple data sets
   
   #density = stats.gaussian_kde(matrix[5])  
   density0 = stats.gaussian_kde(matrix[0][5])
   density1 = stats.gaussian_kde(matrix[1][5])
   density2 = stats.gaussian_kde(matrix[2][5])
   density3 = stats.gaussian_kde(matrix[3][5])
   
   #n, x, _ = plt.hist(matrix[5],bins = np.linspace(0,.5,200), histtype = u'step', normed = True)
   n0, x0, _ = plt.hist(matrix[0][5],bins = np.linspace(0,.5,200), histtype = u'step', normed = True)
   n1, x1, _ = plt.hist(matrix[1][5],bins = np.linspace(0,.5,200), histtype = u'step', normed = True)
   n2, x2, _ = plt.hist(matrix[2][5],bins = np.linspace(0,.5,200), histtype = u'step', normed = True)
   n3, x3, _ = plt.hist(matrix[3][5],bins = np.linspace(0,.5,200), histtype = u'step', normed = True)
   
   plt.clf()
   plt.cla()
   plt.close()
  
   #plt.plot(x,density(x)) 
   plt.plot(x0, density0(x0), color ='blue')
   plt.plot(x2, density2(x2), color = 'green')
   plt.plot(x3, density3(x3), color= 'red')
   plt.plot(x1, density1(x1), color = 'orange')
  

   plt.show()
   plt.pause(.001)
