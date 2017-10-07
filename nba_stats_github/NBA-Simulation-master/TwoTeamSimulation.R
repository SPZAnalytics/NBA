##TwoTeamSimulation.R
Stats<-NBA.Stats
Stats

library(ggplot2)

simgame<-function(team1,team2){
  #assign variables
  team1name<<-Stats[team1,1]
  team2name<<-Stats[team2,1]
  #find total attempts
  totalAtt1<-Stats[team1,3]+Stats[team1,5]+(Stats[team1,7]/2)+Stats[team1,8]+Stats[team1,9]
  #Find the probability of attempting a 2 pt, 3 pt, ft, and turnover.
  twoPtP1<-Stats[team1,3]/totalAtt1
  threePtP1<-Stats[team1,5]/totalAtt1
  FtP1<-(Stats[team1,7]/2)/totalAtt1
  TOP1<-Stats[team1,8]/totalAtt1
  ORB1<-Stats[team1,9]/totalAtt1
  #set team1 points to 0
  team1pt<-0
  #set team1 possession counter
  i1<-0
  #create score progression
  t1sp<-c()
  #Now we start to run through the simulation
  while(i1 <= 100){
    #Randomly select what action is taken
    action<-sample(1:4, 1, prob=c(twoPtP1, threePtP1, FtP1, TOP1))
    #Action = 1? Two Point Attempt
    if(action==1){
      #1 = Make, 2= Miss
      twoMake1<-sample(1:2,1,prob=c(Stats[team1,2],(1-Stats[team1,2])))
      if(twoMake1==1){
        team1pt<-team1pt+2
        t1sp <- c(team1pt,t1sp)
        i1<-i1+1
      }
      if(twoMake1==2){
        oreb21<-sample(1:2,1,prob=c(ORB1,(1-ORB1)))
        if(oreb21==1){
          i1<-i1
        }
        if(oreb21==2){
          t1sp <- c(team1pt,t1sp)
          i1<-i1+1
        }
      }
    }
    #Action = 2? Three Point Attempt
    if(action==2){
      #1 = Make, 2= Miss
      threeMake1<-sample(1:2,1,prob=c(Stats[team1,4],(1-Stats[team1,4])))
      if(threeMake1==1){
        team1pt<-team1pt+3
        t1sp <- c(team1pt,t1sp)
        i1<-i1+1
      }
      if(threeMake1==2){
        oreb31<-sample(1:2,1,prob=c(ORB1,(1-ORB1)))
        if(oreb31==1){
          i1<-i1
        }
        if(oreb31==2){
          t1sp <- c(team1pt,t1sp)
          i1<-i1+1
        }
      }
    }
    #Action = 3? Free Throw Attempt
    if(action==3){
      #free throw 1 and 2
      ft11<-sample(1:2,1,prob=c(Stats[team1,6],(1-Stats[team1,6])))
      ft21<-sample(1:2,1,prob=c(Stats[team1,6],(1-Stats[team1,6])))
      if(ft11==1 & ft21==1){ #Makes both
        team1pt<-team1pt+2
        t1sp <- c(team1pt,t1sp)
        i1<-i1+1
      }
      if(ft11==1 & ft21==2){ #Makes first, misses second
        team1pt<-team1pt+1
        t1sp <- c(team1pt,t1sp)
        i1<-i1+1
      }
      if(ft11==2 & ft21==1){ #Misses first, makes second
        team1pt<-team1pt+1
        t1sp <- c(team1pt,t1sp)
        i1<-i1+1
      }
      if(ft11==2 & ft21==2){ #Misses both
        t1sp <- c(team1pt,t1sp)
        i1<-i1+1
      }
    }
    if(action==4){ #Turnover so nothing happens besides them losing a possesion
      t1sp <- c(team1pt,t1sp)
      i1<-i1+1
    }
  }
  #find total attempts
  totalAtt2<-Stats[team2,3]+Stats[team2,5]+(Stats[team2,7]/2)+Stats[team2,8]+Stats[team2,9]
  #Find the probability of attempting a 2 pt, 3 pt, ft, and turnover.
  twoPtP2<-Stats[team2,3]/totalAtt2
  threePtP2<-Stats[team2,5]/totalAtt2
  FtP2<-(Stats[team2,7]/2)/totalAtt2
  TOP2<-Stats[team2,8]/totalAtt2
  ORB2<-Stats[team2,9]/totalAtt2
  #set team1 points to 0
  team2pt<-0
  #set team1 possession counter
  i2<-0
  #set team2 score progression
  t2sp<-c()
  #Now we start to run through the simulation
  while(i2 <= 100){
    #Randomly select what action is taken
    action<-sample(1:4, 1, prob=c(twoPtP2, threePtP2, FtP2, TOP2))
    #Action = 1? Two Point Attempt
    if(action==1){
      #1 = Make, 2= Miss
      twoMake2<-sample(1:2,1,prob=c(Stats[team2,2],(1-Stats[team2,2])))
      if(twoMake2==1){
        team2pt<-team2pt+2
        t2sp <- c(team2pt,t2sp)
        i2<-i2+1
      }
      if(twoMake2==2){
        oreb22<-sample(1:2,1,prob=c(ORB2,(1-ORB2)))
        if(oreb22==1){
          i2<-i2
        }
        if(oreb22==2){
          t2sp <- c(team2pt,t2sp)
          i2<-i2+1
        }
      }
    }
    #Action = 2? Three Point Attempt
    if(action==2){
      #1 = Make, 2= Miss
      threeMake2<-sample(1:2,1,prob=c(Stats[team2,4],(1-Stats[team2,4])))
      if(threeMake2==1){
        team2pt<-team2pt+3
        t2sp <- c(team2pt,t2sp)
        i2<-i2+1
      }
      if(threeMake2==2){
        oreb32<-sample(1:2,1,prob=c(ORB2,(1-ORB2)))
        if(oreb32==1){
          i2<-i2
        }
        if(oreb32==2){
          t2sp <- c(team2pt,t2sp)
          i2<-i2+1
        }
      }
    }
    #Action = 3? Free Throw Attempt
    if(action==3){
      #free throw 1 and 2
      ft12<-sample(1:2,1,prob=c(Stats[team2,6],(1-Stats[team2,6])))
      ft22<-sample(1:2,1,prob=c(Stats[team2,6],(1-Stats[team2,6])))
      if(ft12==1 & ft22==1){ #Makes both
        team2pt<-team2pt+2
        t2sp <- c(team2pt,t2sp)
        i2<-i2+1
      }
      if(ft12==1 & ft22==2){ #Makes first, misses second
        team2pt<-team2pt+1
        t2sp <- c(team2pt,t2sp)
        i2<-i2+1
      }
      if(ft12==2 & ft22==1){ #Misses first, makes second
        team2pt<-team2pt+1
        t2sp <- c(team2pt,t2sp)
        i2<-i2+1
      }
      if(ft12==2 & ft22==2){ #Misses both
        t2sp <- c(team2pt,t2sp)
        i2<-i2+1
      }
    }
    if(action==4){ #Turnover so nothing happens besides them losing a possesion
      t2sp <- c(team2pt,t2sp)
      i2<-i2+1
    }
    
  }
  
  if(team1pt==team2pt){
    team1pt<-team1pt+1
  }
  
  result1<-sprintf("<h4><strong> %s Final: </h4></strong> %s", Stats[team1,1],team1pt)
  result2<-sprintf("<h4><strong> %s Final: </h4></strong> %s", Stats[team2,1],team2pt)
  team1sp <<- rev(t1sp)
  team2sp <<- rev(t2sp)
  gamescore <<- cbind(team1sp,team2sp)
  paste(result1, result2, sep="<br>")
}

simgame(2,7)



#GRAPHING
comsc<-c(team1sp,team2sp) 

teamid <- c(rep("Team 1", length(team1sp)), rep("Team 2", length(team2sp)))

scoringprog <- data.frame(pos=rep(1:101, 2), score=comsc, team=teamid)
scoringprog

graphsp <- ggplot(data=scoringprog, aes(x=pos, y=comsc, group=team)) +
  geom_line(aes(color=team))+
  geom_point(aes(color=team))+
  xlab("Possesion")+
  ylab("Score")+
  ggtitle("Scoring Progression")+
  labs(color="Team Name")

