source("TwoTeamSimulation.R")
counter<-1
shinyServer(function(input, output,session) {
  
    output$simResult <- renderText({
      team1 <- input$team1
      team2<- input$team2
      simgame(team1,team2)
    })
    
    output$simLogo1 <- renderText({
      team1 <- input$team1
      sprintf('<img src="%s.jpg" height="150" width="350"/>', team1)
    })
    
    output$simLogo2 <- renderText({
      team2 <- input$team2
      sprintf('<img src="%s.jpg" height="150" width="350"/>', team2)
    })
    
    reactPlot<-reactive({
      team1<-input$team1
      team2<-input$team2
      
      if(counter<101){
        invalidateLater(100,session)
      }
      if(counter==101){
        counter<-1
      }
      
      teamid <- c(rep("Team 1", length(team1sp)), rep("Team 2", length(team2sp)))
      counter<<-counter+1
      part<-c(1:counter,102:(101+counter))
      scoringprog <- data.frame(pos=rep(1:101, 2), score=comsc, team=teamid)
      print(scoringprog[part,])
      
      graphsp <- ggplot(data=scoringprog[part,], aes(x=pos, y=score, color=team)) +
        geom_line(aes(color=team))+
        geom_point(aes(color=team))+
        scale_x_continuous(limits=c(1,101))+
        scale_y_continuous(limits=c(1,140))+
        xlab("Possesion")+
        ylab("Score")+
        ggtitle("Scoring Progression")+
        scale_color_discrete(name="Team Name", 
                             breaks=c("Team 1", "Team 2"), 
                             labels=c(as.character(team1name), as.character(team2name)))
      graphsp
    })
    
    output$scrPlot <- renderPlot({
      return(reactPlot())
    })
  })