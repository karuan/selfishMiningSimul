from random import *
# current functionality: not able to perform match operation
for total in range(200,2000,200):
   print total  
   for adv in range (25,40,1): # adv = percentage of blocks initially given to adversary
      numSlots = 10000; #number of time slots
      count = 0; # used to count number of trials exceeding threshold
      numTrials = 100; # number of trials to get percentage
      for s in range (0,numTrials):
         adversary = total*(adv/100.0);
         honest = ((100.0-adv)/100.0)*total;
         state = [0,1,0]  #starting state is honest owning genesis block
         # [a,h, 0 =irrelevant/1=relevant/2=active]
         for m in range (0,numSlots):
            a = state[0]
            h = state[1]
            randNum = random()
            alpha = adversary/(honest+adversary)
            if (alpha >= 0.33): #use selfish mining strategy
               if (h>a): #adopt
                  #reward
                  honest=honest+h
                  #block generation
                  if (randNum< alpha):
                     state = [1,0,0]
                  else:
                     state = [0,1,0]
               #elif (a==1 and h==1 and state[2]==1) : #match (still needs to be implemented)
               elif (a>h): #override
                  #reward
                  adversary = adversary + h + 1   
                  #block generation
                  if (randNum < alpha):
                     state = [a-h,0,0]
                  else:      
                     state = [a-h-1,1,1]
               else: #wait
                  #block generation
                  if (randNum < alpha):
                     state = [a+1,h,0] 
                  else:
                     state = [a,h+1,1]
            else:
               if (randNum < alpha):
                  adversary=adversary+1
                  state=[1,0,0]
               else:
                  honest= honest+1
                  state=[0,1,0]
         if ((adversary/(honest+adversary)) >= 0.33):
            count = count + 1
      print (adv/100.0),",",((count*1.0)/(numTrials*1.0))
