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
    menuItem("Formulário",
             tabName = "form",
             icon = icon("user")
    ),
    menuItem("Sobre",
      tabName = "Sobre",
      icon = icon("info-circle")
    )
  )
)

dash_body <- dashboardBody(
  tags$head(
    tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")
  ),
  tabItems(
    tabItem(
      tabName = "form",
      fluidRow(
        box(
          title = "Formulário",
          selectInput("sexo", "Sexo:", choices = c("1-Masculino", "2-Feminino")),
          selectInput("hepatita", "Vacina para Hepatite A:",
                      choices = c("1-Completa", "2-Incompleta", "3-Não vacinado")),
          selectInput("hepatitb", "Vacina para Hepatite B:",
                      choices = c("1-Completa", "2-Incompleta", "3-Não vacinado"))
        )
      )
    )
  )
)

ui <- dashboardPage(header  = dash_header,
                    sidebar = dash_sidebar,
                    body    = dash_body,
                    skin = 'blue')


server <- function(input, output) {
}

shinyApp(ui = ui, server = server)