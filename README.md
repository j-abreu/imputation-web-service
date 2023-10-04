# Serviço Web para Imputação de Dados em Séries Temporais Univariadas
Autor: Jeremias Lima Abreu <br>
Orientador: Glauco Estácio Gonçalves

Trabalho de Conclusão de Curso apresentado à Faculdade de Computação e Telecomunicações da Universidade Federal do Pará, como requisito parcial para a obtenção do Grau de Bacharel em Engenharia da Computação.

UFPA / ITEC / FCT <br>
Campus Universitário do Guamá <br>
Belém – Pará – Brasil <br>
2022 <br>

## Resumo
Este trabalho apresenta o desenvolvimento de um serviço web para realização de imputação de dados em séries temporais univariadas, permitindo que uma aplicação cliente solicite imputações, verifique o status do processamento e recupere os dados através de requisições HTTP com respostas de baixa latência. A aplicação proposta foi desenvolvida usando tecnologias Python, seguindo padrões de projetos para serviços web previamente documentados na literatura e possui dois componentes principais: o Imputation Creator and Retriever, responsável por receber as requisições de criação de imputação e recuperação dos dados imputados; e o Imputation Processor, responsável por realizar a imputação nas séries temporais fornecidas. A aplicação foi submetidas a testes fatoriais de desempenho levando em consideração o número de usuários fazendo requisições HTTP e o algoritmo escolhido para imputação, evidenciando a variação do tempo médio de resposta nos cenários avaliados. Os algoritmos para imputação também passaram por uma avaliação, a partir da qual foi possível apresentar o erro médio absoluto e o tempo médio de execução para uma série temporal de temperatura média diária registrada pelo Instituto Nacional de Meteorologia.

<b>Palavras-chave</b>: Serviços RESTful, Arquitetura de Sistemas, Lacunas de dados, Padrões de Projeto.

## Abstract
This work presents the development of a web service to carry out data imputation in univariate time series, allowing a client application to request imputations, checks the processing status and retrieve data through HTTP requests with low latency responses. The proposed application was developed using Python technologies, following web services design patterns previously documented in the literature and has two main components: the Imputation Creator and Retriever, responsible for receive requests for creation of imputation and recovery of imputed data; and the Imputation Processor, responsible for imputing the time series provided. The application was subjected to factorial performance tests taking into account the number of users making HTTP requests and the algorithm chosen for imputation, showing the variation in the average response time in the evaluated scenarios. The imputation algorithms also underwent evaluation experiments, where it was possible to present the mean absolute error and the mean execution time for a time series of average daily temperature recorded by the National Institute of Meteorology.

<b>Keywords</b>: RESTful services, Software Architecture, Missing Data, Service Design
Patterns.
