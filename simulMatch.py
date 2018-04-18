from random import *
# current functionality: not able to perform match operation
# incorrect: should use honest strategy when alpha <0.33
for total in range(200,2000,200):
   print total  
   for adv in range (25,40,1): # adv = percentage of blocks initially given to adversary
      numSlots = 100; #number of time slots
      count = 0; # used to count number of trials exceeding threshold
      numTrials = 10000; # number of trials to get percentage
      gamma = 0.2;
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
            if (h>a): #adopt
               #reward
               honest=honest+h
               #block generation
               if (randNum< alpha):
                  state = [1,0,0]
               else:
                  state = [0,1,0]
            elif (state[2]==2 or (a==1 and h==1 and state[2]==1 and state[2]==1)): 
               if (randNum<alpha):
                  state=[a+1,h,2]
               elif (randNum<alpha+(gamma*(1-alpha))):
                  state=[a-h,1,1]
                  adversary = adversary+h
               else:
                  state=[a,h+1,1]
            elif (h==(a-1) and (a-1)>=1): #override
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
         if ((adversary/(honest+adversary)) >= 0.33):
            count = count + 1
      print (adv/100.0),",",((count*1.0)/(numTrials*1.0))
