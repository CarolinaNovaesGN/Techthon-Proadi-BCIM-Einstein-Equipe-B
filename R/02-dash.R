library(shiny)
library(data.table)
library(dplyr)
library(lubridate)
library(ggplot2)
library(plotly)
library(shinyWidgets)
library(shinydashboard)
library(DT)

dash_header <- dashboardHeader(title = "HepatiCARE")

dash_sidebar <- dashboardSidebar(

  width = "230px",
  
  sidebarMenu(
    menuItem("Sobre",
      tabName = "Sobre",
      icon = icon("info-circle")
    ),
    
    menuItem("Diagnóstico",
             tabName = "diagnostico",
             icon = icon("heartbeat")
    )
  )
)

dash_body <- dashboardBody(
  tags$head(
    tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
  )
)

ui <- dashboardPage(header  = dash_header,
                    sidebar = dash_sidebar,
                    body    = dash_body,
                    skin = 'blue')


server <- function(input, output) {
}

shinyApp(ui = ui, server = server)