# Desafio Docker – Flask + PostgreSQL

## Como rodar

### 1. Criar contêiner do PostgreSQL
```bash
docker run -d --name meu-banco \
  -e POSTGRES_USER=usuario \
  -e POSTGRES_PASSWORD=senha123 \
  -e POSTGRES_DB=mensagensdb \
  postgres:15

git bash:

docker network create minha-rede

docker network connect minha-rede meu-banco

docker build -t flask-db-app .

docker run -d --name minha-api --network minha-rede -p 5000:5000 flask-db-app

$ curl -X POST http://localhost:5000/mensagem \
     -H "Content-Type: application/json" \
     -d "{\"texto\":\"Ola Docker\"}"
