# Techthon-Proadi-BCIM-Einstein

Projeto realizado pela equipe B to Techthon-Proadi-BCIM-Einstein: Ariana Caral, Carolina Novaes, Lays Azevedo, Luana Nunes e Mariana Marques.
Esse projeto contém modelos de Machine Learning sobre a hepatite e scripts de implementação do modelo no ambiente Sagemaker da Amazon Web Services. Foi utilizada uma imagem docker do framework scikit-learn pre-built disponiilizada pela AWS. Para mais informações, consulte a documentação oficial da AWS.

## Sumário

- [Base de dados]

A base de dados utilizada para a implementação da solução foi a [**SINAN**](http://portalsinan.saude.gov.br/o-sinan) (Sistema de Informação de Agravos de Notificação) do DATASUS que apresenta, dentre outros dados epidemiológicos, notificações das hepatites virais B e C.

A base contempla variáveis demográficas (como sexo, raça/cor, idade) e clínicas (como potenciais exposições aos vírus das hepatites, resultados sorológicos/virológicos e classificação diagnóstica) que são importantes para traçar o perfil dos indivíduos infectados e possibilitam a implementação de modelos de classificação diagnóstica, cuja descrição detalhada encontra-se detalhada na [documentação](https://github.com/CarolinaNovaesGN/Techthon-Proadi-BCIM-Einstein/tree/main/dictionary) do SINAN.

Para a modelagem, foi considerado apenas os dados de hepatite B e C, não sendo considerados observações faltantes ou ignoradas durante o preenchimento da notificação.

- [Recursos]

Registro do modelo do arquivo train.py no ambiente da AWS para online serving e batch predictions. Após rodar o script deploy_model será criado um artefato do modelo serializado em um bucket do S3, um modelo registrado no sagemaker e um endpoint com o modelo implantado para predições. 

O script inference.py será compactado junto ao modelo serializado. Ele está estruturado de acordo com os requisitos da AWS para realizar a integração de um modelo customizado com um container para previsões. Esse código pode ser customizado desde que mantenha essa estrutura e nomenclatura de funções.

- [Pré-requisitos]

Name: boto3 (python package)
Version: 1.28.62

Name: sagemaker (python package)
Version: 2.191.0

Name: scikit-learn (python package)
Version: 1.0.2

Name: aws-cli
Version: 2.13.25 

Name: Python
Version: 3.11.

- [Contribuição]

Contribuições são bem-vindas! Para contribuir com Techthon-Proadi-BCIM-Einstein, siga estas etapas:

Fork do repositório
Crie uma nova branch (git checkout -b feature/nova-funcionalidade)
Faça commit de suas alterações (git commit -am 'Adicionei uma nova funcionalidade')
Envie suas alterações (git push origin feature/nova-funcionalidade)
Abra uma solicitação de pull

- [Licença]

Este projeto está licenciado sob a licença MIT.
