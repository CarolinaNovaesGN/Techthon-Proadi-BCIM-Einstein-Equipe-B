import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score

# Importando os dados -----------------------------------------------------
str_path = "./data-raw"

#filenames = glob.glob(os.path.join(str_path, "*.dbc"))

#db = pd.concat([read.dbc(filename) for filename in filenames], keys=tools.file_path_sans_ext(basename(filenames)))
db = pd.read_csv('hepatite_br.csv', encoding='ISO-8859-1').drop(columns='Unnamed: 0')

# Visualizando a estrutura dos dados --------------------------------------
print(db)
print(db.info())
print(db.describe())

# Organizando a base ------------------------------------------------------
tidy_db = db.copy()

tidy_db['EXPOSICAO'] = tidy_db.apply(
    lambda row: 1 if (row['SEXUAL'] == 1 or row['OUTRAS'] == 2) else (0 if (row['SEXUAL'] == 3 and row['OUTRAS'] == 3) else None),
    axis=1
)

tidy_db = tidy_db[['CS_SEXO', 'CS_RACA', 'CS_ESCOL_N', 'HEPATITE_N', 'HEPATITA', 'HEPATITB', 'HIV', 'OUTRA_DST', 'EXPOSICAO',
                   'ANTIHAVIGM','GEN_VHC', 'CLASSI_FIN', 'FORMA', 'CLAS_ETIOL']]

hepa_data = tidy_db[(tidy_db['HEPATITE_N'] == 2) & (tidy_db['CS_SEXO'] != "I") & (tidy_db['HEPATITA'] != 9) & 
                    (tidy_db['HEPATITB'] != 9) & (tidy_db['HIV'] != 9) & (tidy_db['OUTRA_DST'] != 9)].copy()

hepa_data = hepa_data[['CS_SEXO', 'HEPATITA', 'HEPATITB', 'HIV', 'OUTRA_DST', 'EXPOSICAO', 'ANTIHAVIGM', 'GEN_VHC', 'CLASSI_FIN']]

# Usando o encoder
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

hepa_data_copy = hepa_data.copy()
hepa_data_copy['CS_SEXO'] = label_encoder.fit_transform(hepa_data_copy['CS_SEXO'])

# Fill na
hepa_data_copy = hepa_data_copy.fillna(0)
# Dividindo o conjunto de dados em treinamento e teste
X = hepa_data_copy.drop(columns=['CLASSI_FIN'])
y = hepa_data_copy['CLASSI_FIN']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

# randomForest ------------------------------------------------------------
# Criando modelo de classificação
rf_model = RandomForestClassifier(random_state=123)
rf_model.fit(X_train, y_train)


#Serializando o modelo para o deploy
with open('model.joblib', 'wb') as f:
    joblib.dump(rf_model,f)
