<h1 align="center">Análise de Sentimentos com Docker, FastAPI, Prometheus e Grafana :tada:</h1>

Esta é uma configuração que deve ser realizada para monitorar o sua aplicação.

## Instalação

Existem apenas dois pré-requisitos:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker-compose](https://docs.docker.com/compose/install/)

Tendo ambos, será necessário clonar o repositório:

``` bash
git clone https://
```

## Como utilizar

É necessário executar os containers docker:

``` bash
docker-compose up
```

Agora você terá acesso a três containers e suas respectivas portas:

* Prometheus: http://localhost:9090/
* Grafana: http://localhost:3000/
* FastAPI: http://localhost:8000/

Como foi testado?
passamos como parâmetro as frases abaixo:

* Frase 1: "Eu amo Python!"
* Frase 2: "Este filme foi péssimo."
* Frase 3: "A comida do restaurante era deliciosa."
* Frase 4: "O atendimento da loja foi horrível."
* Frase 5: "Python é ótimo para Machine Learning"

Na FastAPI, além de analise_sentimento você poderá acessar o endpoint `/metrics` para ver os dados que o Prometheus está extraindo da aplicação.
## References

* [Prometheus FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
* [Visualizando as Métricas de Nossa API](https://johnfercher.medium.com/go-grafana-2b1419f7a99d)
* [Monitorando Modelos de Aprendizado de Máquina em Produção](https://estevestoni.medium.com/monitorando-modelos-de-aprendizado-de-m%C3%A1quina-em-produ%C3%A7%C3%A3o-9d4f83a3dbfa)