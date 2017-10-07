##UI.R
shinyUI(fluidPage(
  
  titlePanel("NBA Simulation","NBA Simulation"),
  
  sidebarLayout(
  
    sidebarPanel(
      
      
      helpText("Choose two different NBA teams to simulate a game!"),
      
      selectInput("team1",
                  label="Team 1:",
                  choices=list("Atlanta Hawks"=1, "Boston Celtics"=2, "Brooklyn Nets"=3, "Charlotte Hornets"=4, "Chicago Bulls"=5, "Cleveland Cavaliers"=6, "Dallas Mavericks"=7, "Denver Nuggets"=8, "Detroit Pistons"=9, "Golden State Warriors"=10, "Houston Rockets"=11, "Indiana Pacers"=12, "LA Clippers"=13, "LA Lakers"=14, "Memphis Grizzlies"=15, "Miami Heat"=16, "Milwaukee Bucks"=17, "Minnesota Timberwolves"=18, "New Orleans Pelicans"=19, "New York Knicks"=20, "OKC Thunder"=21, "Orlando Magic"=22, "Philadelphia 76ers"=23, "Phoenix Suns"=24, "Portland Trailblazers"=25, "Sacramento Kings"=26, "San Antonio Spurs"=27, "Toronto Raptors"=28, "Utah Jazz"=29, "Washington Wizards"=30),
                  selected=1),
      
      selectInput("team2",
                  label="Team 2:",
                  choices=list("Atlanta Hawks"=1, "Boston Celtics"=2, "Brooklyn Nets"=3, "Charlotte Hornets"=4, "Chicago Bulls"=5, "Cleveland Cavaliers"=6, "Dallas Mavericks"=7, "Denver Nuggets"=8, "Detroit Pistons"=9, "Golden State Warriors"=10, "Houston Rockets"=11, "Indiana Pacers"=12, "LA Clippers"=13, "LA Lakers"=14, "Memphis Grizzlies"=15, "Miami Heat"=16, "Milwaukee Bucks"=17, "Minnesota Timberwolves"=18, "New Orleans Pelicans"=19, "New York Knicks"=20, "OKC Thunder"=21, "Orlando Magic"=22, "Philadelphia 76ers"=23, "Phoenix Suns"=24, "Portland Trailblazers"=25, "Sacramento Kings"=26, "San Antonio Spurs"=27, "Toronto Raptors"=28, "Utah Jazz"=29, "Washington Wizards"=30),
                  selected=2),
      
      submitButton("Submit")
    ),
    
    mainPanel(
      h1("Final Result"),
      htmlOutput("simLogo1"),
      htmlOutput("simResult"),
      htmlOutput("simLogo2"),
      plotOutput("scrPlot")
    )
  
)
)
)