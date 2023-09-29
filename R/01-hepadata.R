# Carregando pacotes necessários ------------------------------------------
library(dplyr)

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

tidy.db |>
  dplyr::select(
    CS_SEXO, CS_RACA,
    HEPATITE_N, HEPATITA, HEPATITB, SEXUAL:OUTRAS, EXPOSICAO
  ) |>
  View()

tidy.db <- tidy.db |>
  dplyr::select(
    CS_SEXO, CS_GESTANT, CS_RACA, CS_ESCOL_N,
    HEPATITE_N, HEPATITA, HEPATITB, HIV,
    OUTRA_DST, EXPOSICAO, ANTIHAVIGM:ANTIHDV,
    CLASSI_FIN, FORMA, CLAS_ETIOL
  )