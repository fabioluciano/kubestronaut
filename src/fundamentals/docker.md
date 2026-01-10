# Docker

> **Certificacoes**: KCNA (16%)

## Historia e Evolucao

### Origem do Docker

Docker foi lancado em 2013 pela dotCloud (posteriormente Docker Inc.) e revolucionou a forma como aplicacoes sao empacotadas e distribuidas.

```plantuml,format=png
../assets/diagrams/general/docker-evolucao-dos-containers.puml
```

### Marcos Importantes

| Ano | Evento |
|-----|--------|
| **2008** | LXC (Linux Containers) criado |
| **2013** | Docker lancado como projeto open source |
| **2014** | Docker Hub lancado |
| **2015** | OCI (Open Container Initiative) fundada |
| **2015** | Kubernetes 1.0 lancado |
| **2016** | containerd extraido do Docker |
| **2017** | containerd doado para CNCF |
| **2020** | Kubernetes deprecia Dockershim |
| **2022** | Kubernetes remove Dockershim (1.24) |

---

## Arquitetura do Docker

### Componentes Principais

```plantuml,format=png
../assets/diagrams/general/docker-arquitetura-docker.puml
```

### Componentes Detalhados

| Componente | Funcao | Descricao |
|------------|--------|-----------|
| **Docker CLI** | Cliente | Interface de linha de comando |
| **dockerd** | Daemon | Gerencia objetos Docker (imagens, containers) |
| **containerd** | Runtime | Gerencia lifecycle de containers |
| **runc** | Runtime OCI | Executa containers (namespaces, cgroups) |
| **Docker Registry** | Armazenamento | Armazena e distribui imagens |

### Fluxo de Execucao

```plantuml,format=png
../assets/diagrams/general/docker-fluxo-docker-run-nginx.puml
```

---

## Docker vs containerd

### Por que Kubernetes Removeu Docker?

```plantuml,format=png
../assets/diagrams/general/docker-kubernetes-docker-antes.puml
```

```plantuml,format=png
../assets/diagrams/general/docker-kubernetes-containerd-agora.puml
```

### Comparacao Docker vs containerd

| Aspecto | Docker | containerd |
|---------|--------|------------|
| **Escopo** | Plataforma completa | Runtime focado |
| **CLI** | `docker` | `ctr`, `crictl`, `nerdctl` |
| **Build** | Suporta Dockerfile | Nao suporta (use buildkit) |
| **Compose** | docker-compose | nerdctl compose |
| **Overhead** | Maior | Menor |
| **Kubernetes** | Via Dockershim (removido) | CRI nativo |

### O que Ainda Funciona

```admonish info title="Importante"
Imagens construidas com Docker continuam funcionando no Kubernetes. O padrao OCI garante compatibilidade. Apenas o runtime mudou, nao o formato de imagem.
```

---

## Dockerfile

### Estrutura Basica

```dockerfile
# Imagem base
FROM ubuntu:22.04

# Metadados
LABEL maintainer="dev@example.com"
LABEL version="1.0"

# Variaveis de ambiente
ENV APP_HOME=/app
ENV NODE_ENV=production

# Diretorio de trabalho
WORKDIR $APP_HOME

# Copiar arquivos
COPY package*.json ./
COPY src/ ./src/

# Executar comandos (cria nova layer)
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm ci --only=production && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Usuario nao-root
RUN useradd -r -u 1001 appuser
USER appuser

# Porta exposta (documentacao)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1

# Comando padrao
CMD ["node", "src/index.js"]
```

### Instrucoes do Dockerfile

| Instrucao | Descricao | Exemplo |
|-----------|-----------|---------|
| `FROM` | Imagem base | `FROM node:18-alpine` |
| `WORKDIR` | Diretorio de trabalho | `WORKDIR /app` |
| `COPY` | Copiar arquivos | `COPY . .` |
| `ADD` | Copiar + extrair + URL | `ADD app.tar.gz /app` |
| `RUN` | Executar comando (build) | `RUN npm install` |
| `ENV` | Variavel de ambiente | `ENV NODE_ENV=prod` |
| `ARG` | Argumento de build | `ARG VERSION=1.0` |
| `EXPOSE` | Documentar porta | `EXPOSE 8080` |
| `USER` | Usuario de execucao | `USER node` |
| `CMD` | Comando padrao | `CMD ["node", "app.js"]` |
| `ENTRYPOINT` | Ponto de entrada | `ENTRYPOINT ["python"]` |
| `VOLUME` | Ponto de montagem | `VOLUME /data` |
| `HEALTHCHECK` | Verificacao de saude | `HEALTHCHECK CMD curl...` |
| `LABEL` | Metadados | `LABEL version="1.0"` |

### CMD vs ENTRYPOINT

```plantuml,format=png
../assets/diagrams/general/docker-cmd-vs-entrypoint.puml
```

```dockerfile
# Exemplo 1: Apenas CMD (pode ser sobrescrito)
FROM ubuntu
CMD ["echo", "Hello World"]
# docker run image             -> "Hello World"
# docker run image echo "Bye"  -> "Bye"

# Exemplo 2: ENTRYPOINT + CMD (argumentos padrao)
FROM python:3.9
ENTRYPOINT ["python"]
CMD ["app.py"]
# docker run image           -> python app.py
# docker run image test.py   -> python test.py

# Exemplo 3: ENTRYPOINT fixo
FROM ubuntu
ENTRYPOINT ["echo"]
# docker run image Hello     -> "Hello"
```

---

## Multi-stage Builds

### Conceito

Multi-stage builds permitem usar multiplas instrucoes FROM para criar imagens menores e mais seguras.

```plantuml,format=png
../assets/diagrams/general/docker-multi-stage-build.puml
```

### Exemplo: Aplicacao Go

```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Dependencias primeiro (cache)
COPY go.mod go.sum ./
RUN go mod download

# Codigo fonte
COPY . .

# Compilar binario estatico
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Runtime
FROM scratch

# Certificados para HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Binario da stage anterior
COPY --from=builder /app/main /main

# Usuario nao-root
USER 1001

ENTRYPOINT ["/main"]
```

### Exemplo: Aplicacao Node.js

```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Runtime
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

USER nextjs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Exemplo: Aplicacao Java

```dockerfile
# Stage 1: Build com Maven
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline

COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runtime com JRE
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

RUN addgroup -g 1001 -S java && \
    adduser -S app -u 1001 -G java

COPY --from=builder /app/target/*.jar app.jar

USER app

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Beneficios do Multi-stage

| Beneficio | Descricao |
|-----------|-----------|
| **Imagens menores** | Nao inclui ferramentas de build |
| **Mais seguras** | Menos superficie de ataque |
| **Builds reproduziveis** | Tudo em um Dockerfile |
| **Cache eficiente** | Stages podem ser cacheados |

---

## Comandos Essenciais

### Gerenciamento de Imagens

```bash
# Construir imagem
docker build -t myapp:v1 .
docker build -t myapp:v1 -f Dockerfile.prod .

# Construir com argumentos
docker build --build-arg VERSION=1.0 -t myapp:v1 .

# Listar imagens
docker images
docker image ls

# Remover imagem
docker rmi myapp:v1
docker image rm myapp:v1

# Remover imagens nao utilizadas
docker image prune
docker image prune -a  # todas sem container

# Inspecionar imagem
docker image inspect myapp:v1

# Historico de layers
docker history myapp:v1

# Tag de imagem
docker tag myapp:v1 registry.example.com/myapp:v1

# Push para registry
docker push registry.example.com/myapp:v1

# Pull de registry
docker pull nginx:1.25
```

### Gerenciamento de Containers

```bash
# Criar e iniciar container
docker run nginx
docker run -d nginx                    # detached (background)
docker run -it ubuntu bash             # interativo + TTY
docker run --name web nginx            # nome especifico
docker run -p 8080:80 nginx            # mapear porta
docker run -v /data:/app/data nginx    # montar volume
docker run -e ENV=prod nginx           # variavel de ambiente
docker run --rm nginx                  # remover apos parar

# Listar containers
docker ps           # em execucao
docker ps -a        # todos

# Parar container
docker stop <id>
docker stop $(docker ps -q)  # parar todos

# Iniciar container parado
docker start <id>

# Remover container
docker rm <id>
docker rm -f <id>   # forcar (mesmo rodando)

# Remover todos containers parados
docker container prune

# Logs
docker logs <id>
docker logs -f <id>      # follow
docker logs --tail 100 <id>

# Executar comando em container
docker exec -it <id> bash
docker exec <id> ls /app

# Copiar arquivos
docker cp file.txt <id>:/app/
docker cp <id>:/app/file.txt .

# Inspecionar container
docker inspect <id>

# Stats de recursos
docker stats
docker stats <id>
```

### Gerenciamento de Volumes

```bash
# Criar volume
docker volume create mydata

# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect mydata

# Remover volume
docker volume rm mydata

# Remover volumes nao utilizados
docker volume prune

# Usar volume em container
docker run -v mydata:/app/data nginx

# Bind mount (diretorio do host)
docker run -v /host/path:/container/path nginx
docker run -v $(pwd):/app nginx  # diretorio atual
```

### Networking

```bash
# Criar rede
docker network create mynet

# Listar redes
docker network ls

# Conectar container a rede
docker network connect mynet <id>

# Desconectar
docker network disconnect mynet <id>

# Usar rede especifica
docker run --network mynet nginx

# Inspecionar rede
docker network inspect mynet
```

### Limpeza

```bash
# Remover tudo nao utilizado
docker system prune

# Remover tudo (incluindo volumes)
docker system prune -a --volumes

# Ver uso de disco
docker system df
```

---

## Boas Praticas

### Otimizacao de Dockerfile

```plantuml,format=png
../assets/diagrams/general/docker-boas-praticas-dockerfile.puml
```

### Exemplo de .dockerignore

```plaintext
# Controle de versao
.git
.gitignore

# Dependencias
node_modules
vendor
__pycache__

# Build artifacts
dist
build
*.pyc
*.class

# IDE
.idea
.vscode
*.swp

# Docker
Dockerfile*
docker-compose*
.docker

# Docs
README.md
docs

# Testes
test
tests
coverage
.coverage

# Seguranca
.env
*.pem
*.key
secrets
```

### Ordenacao de Instrucoes (Cache)

```dockerfile
# RUIM: Qualquer mudanca invalida cache de tudo
FROM node:18-alpine
COPY . .
RUN npm install
CMD ["node", "app.js"]

# BOM: Dependencias separadas (cache eficiente)
FROM node:18-alpine
WORKDIR /app

# 1. Dependencias (muda raramente)
COPY package*.json ./
RUN npm ci --only=production

# 2. Codigo (muda frequentemente)
COPY . .

CMD ["node", "app.js"]
```

### Combinar Comandos RUN

```dockerfile
# RUIM: Muitas layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get clean

# BOM: Uma layer, limpa no final
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

---

## Troubleshooting

### Problemas Comuns

| Problema | Causa | Solucao |
|----------|-------|---------|
| Build lento | Cache invalidado | Ordenar instrucoes por frequencia |
| Imagem grande | Muitas dependencias | Multi-stage, distroless |
| Container nao inicia | CMD/ENTRYPOINT errado | Verificar logs, testar comando |
| Permissao negada | Usuario sem acesso | Verificar permissoes, chown |
| Porta em uso | Conflito de portas | Usar -p com porta diferente |

### Debug de Build

```bash
# Build com output detalhado
docker build --progress=plain -t myapp .

# Build sem cache
docker build --no-cache -t myapp .

# Build ate stage especifica
docker build --target builder -t myapp:builder .

# Ver layers e tamanhos
docker history myapp:v1

# Inspecionar imagem
docker image inspect myapp:v1
```

### Debug de Container

```bash
# Ver logs
docker logs <id>
docker logs -f <id>  # follow

# Acessar shell
docker exec -it <id> sh
docker exec -it <id> bash

# Ver processos
docker top <id>

# Ver diferencas do filesystem
docker diff <id>

# Criar imagem do container atual
docker commit <id> debug:v1

# Inspecionar
docker inspect <id>
```

---

## Dicas para o Exame KCNA

```admonish tip title="Dicas KCNA - Docker"
1. **Entenda a historia**: Docker democratizou containers, OCI padronizou
2. **Saiba a arquitetura**: CLI -> daemon -> containerd -> runc
3. **Docker vs containerd**: Kubernetes usa containerd diretamente
4. **Imagens OCI**: Formato padrao, funciona em qualquer runtime
5. **Nao precisa saber comandos**: KCNA e conceitual
```

### Conceitos-Chave para Memorizar

| Conceito | Lembrar |
|----------|---------|
| **OCI** | Open Container Initiative - padroes |
| **containerd** | Runtime extraido do Docker, CNCF graduated |
| **Dockershim** | Removido do Kubernetes 1.24 |
| **Multi-stage** | Multiplos FROM, imagens menores |
| **Layer** | Cada instrucao cria uma layer |

---

## Referencias

### Documentacao Oficial

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Hub](https://hub.docker.com/)
- [containerd](https://containerd.io/)

### Arquivos Relacionados

- [Containers](fundamentals/containers.md) - Conceitos de containers
- [crictl](crictl.md) - CLI para CRI
- [Kubernetes Container Runtimes](cluster-components/node-components.md) - Componentes do node
- [Cloud Native](fundamentals/cloud-native.md) - Conceitos Cloud Native

