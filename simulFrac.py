from random import *
import math
# current functionality: not able to perform match operation
for total in range(200,2000,200):
   print total  
   for adv in range (25,40,1): # adv = percentage of blocks initially given to adversary
      numSlots = 10000; #number of time slots
      count = 0; # used to count number of trials exceeding threshold
      numTrials = 100; # number of trials to get percentage
      fraction = 0.005; #fraction of total blocks used as block reward
      for s in range (0,numTrials):
         adversary = total*(adv/100.0);
         honest = ((100.0-adv)/100.0)*total;
         reward = (math.pow((adversary+honest),1.1))*0.0001
         state = [0,reward,0]  #starting state is honest owning genesis block
         # [a,h, 0 =irrelevant/1=relevant/2=active]
         for m in range (0,numSlots):
            a = state[0]
            h = state[1]
            randNum = random()
            alpha = adversary/(honest+adversary)
            reward = math.pow((adversary+honest),1.1)*0.0001
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
         if ((adversary/(honest+adversary)) >= 0.33):
            count = count + 1
      print (adv/100.0),",",((count*1.0)/(numTrials*1.0))
