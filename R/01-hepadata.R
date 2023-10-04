# Carregando pacotes necessários ------------------------------------------
library(dplyr)
library(caret)
library(randomForest)
library(class)
library(e1071)

# Importando os dados -----------------------------------------------------

str_path <- "./data-raw"

filenames <- list.files(
  path = str_path,
  full.names = TRUE
)

db <- purrr::map(filenames, \(filename){
  read.dbc::read.dbc(filename)
},
.progress = TRUE
)

names(db) <- tools::file_path_sans_ext(basename(filenames))

db <- purrr::list_rbind(db, names_to = "ID")

# Visualizando a estrutura dos dados --------------------------------------

db |> View()
str(db)
summary(db)

# Organizando a base ------------------------------------------------------

tidy.db <- db  %>% 
  dplyr::mutate(
    EXPOSICAO = dplyr::case_when(
      rowSums(dplyr::select(., SEXUAL:OUTRAS) == c(1,2)) > 0 ~ 1,
      rowSums(dplyr::select(., SEXUAL:OUTRAS) == 3) > 0 ~ 0,
      TRUE ~ NA_integer_
    )
  ) 

tidy.db <- tidy.db |>
  dplyr::relocate(EXPOSICAO, .before = SEXUAL)

tidy.db <- tidy.db |>
  dplyr::select(
    CS_SEXO, CS_RACA, CS_ESCOL_N,
    #CS_GESTANT, 
    HEPATITE_N, HEPATITA, HEPATITB, HIV,
    OUTRA_DST, EXPOSICAO,
    #SEXUAL:OUTRAS,
    ANTIHAVIGM:GEN_VHC, 
    CLASSI_FIN, FORMA, CLAS_ETIOL
  )

hepa.data <- tidy.db |> 
  filter(HEPATITE_N == 2,# suspeita inicial de hepatite B/C
         CS_SEXO != "I", # removendo observação quando o SEXO é ignorada
         HEPATITA == 9, # removendo observação quando o HEPATITA é ignorada
         HEPATITB == 9, 
         HIV == 9, 
         OUTRA_DST == 9) |> 
  dplyr::select(
    CS_SEXO,
    HEPATITA, HEPATITB, HIV,
    OUTRA_DST, EXPOSICAO,
    ANTIHAVIGM:GEN_VHC, 
    CLASSI_FIN
  ) |> 
  tidyr::drop_na() |> 
  dplyr::mutate( 
    CS_SEXO = as.character(CS_SEXO) |> 
      as.factor(),
    CLASSI_FIN = as.character(CLASSI_FIN), 
                CLASSI_FIN_NOME = dplyr::case_when(
                  CLASSI_FIN == 1 ~ "confirmacao laboratorial",
                  CLASSI_FIN == 2 ~ "confirmacao clinico-epidemiologica",
                  CLASSI_FIN == 3 ~ "descartado", 
                  CLASSI_FIN == 4 ~ "cicatriz sorologica",
                  CLASSI_FIN == 8 ~ "inconclusivo"
                ) |> as.factor()) |> 
  dplyr::select(!CLASSI_FIN)


# randomForest ------------------------------------------------------------

# Dividindo o conjunto de dados em treinamento e teste
set.seed(123)  
index <- createDataPartition(hepa.data$CLASSI_FIN_NOME, p = 0.8, list = FALSE)
train_data <- hepa.data[index, ]
test_data <- hepa.data[-index, ]

# Criando modelo de classificação
model <- randomForest(CLASSI_FIN_NOME ~ ., data = train_data)

# Fazendo previsões no conjunto de testes
predictions <- predict(model, newdata = test_data)

# Avaliando o desempenho do modelo
confusion_matrix <- table(predictions, test_data$CLASSI_FIN_NOME)
confusion_matrix

accuracy <- sum(diag(confusion_matrix)) / sum(confusion_matrix)
accuracy

# naiveBayes --------------------------------------------------------------

# Dividindo o conjunto de dados em treinamento e teste
set.seed(123)  # Defina uma semente para a reproducibilidade
index <- createDataPartition(hepa.data$CLASSI_FIN_NOME, p = 0.8, list = FALSE)
train_data <- hepa.data[index, ]
test_data <- hepa.data[-index, ]

# Criando modelo de classificação Naïve Bayes
model <- e1071::naiveBayes(CLASSI_FIN_NOME ~ ., data = train_data)

# Fazendo previsões no conjunto de testes
predictions <- predict(model, newdata = test_data)

# Avaliando o desempenho do modelo
confusion_matrix <- table(predictions, test_data$CLASSI_FIN_NOME)
confusion_matrix

accuracy <- sum(diag(confusion_matrix)) / sum(confusion_matrix)
accuracy

