# Helm

## Conceitos Fundamentais

### O que é Helm?

Helm é o **gerenciador de pacotes** do Kubernetes, equivalente ao apt/yum para Linux ou npm para Node.js.

```plantuml,format=png
!include ../assets/diagrams/tools/helm-arquitetura-helm-1.puml
```

### Helm 3 vs Helm 2

| Característica | Helm 2 | Helm 3 |
|----------------|--------|--------|
| **Tiller** | Necessário (server-side) | Removido |
| **Segurança** | Tiller tinha permissões amplas | Usa kubeconfig do usuário |
| **Namespace** | Release global | Release por namespace |
| **CRDs** | Hooks | Pasta `crds/` dedicada |

---

## Comandos Essenciais

### Repositórios

```bash
# Adicionar repositório
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add stable https://charts.helm.sh/stable

# Listar repositórios
helm repo list

# Atualizar cache dos repositórios
helm repo update

# Remover repositório
helm repo remove bitnami

# Buscar charts
helm search repo nginx
helm search repo bitnami/nginx --versions
```

### Instalação e Gerenciamento

```bash
# Instalar chart
helm install my-nginx bitnami/nginx

# Instalar com namespace
helm install my-nginx bitnami/nginx -n web-apps --create-namespace

# Instalar com valores customizados
helm install my-nginx bitnami/nginx -f custom-values.yaml

# Instalar com valores inline
helm install my-nginx bitnami/nginx --set replicaCount=3

# Instalar versão específica
helm install my-nginx bitnami/nginx --version 15.0.0

# Dry-run (simular sem aplicar)
helm install my-nginx bitnami/nginx --dry-run

# Gerar manifests sem instalar
helm template my-nginx bitnami/nginx > manifests.yaml
```

### Upgrade e Rollback

```bash
# Upgrade de release
helm upgrade my-nginx bitnami/nginx

# Upgrade com novos valores
helm upgrade my-nginx bitnami/nginx -f new-values.yaml

# Upgrade ou instala se não existir
helm upgrade --install my-nginx bitnami/nginx

# Ver histórico de releases
helm history my-nginx

# Rollback para revisão anterior
helm rollback my-nginx 1

# Rollback para versão específica
helm rollback my-nginx 2
```

### Listagem e Informações

```bash
# Listar releases
helm list
helm list -A  # Todos namespaces
helm list -n my-namespace

# Ver valores de uma release
helm get values my-nginx

# Ver todos os valores (incluindo defaults)
helm get values my-nginx --all

# Ver manifests aplicados
helm get manifest my-nginx

# Ver informações completas
helm get all my-nginx

# Status da release
helm status my-nginx
```

### Remoção

```bash
# Desinstalar release
helm uninstall my-nginx

# Desinstalar mantendo histórico
helm uninstall my-nginx --keep-history
```

---

## Estrutura de um Chart

### Criando um Chart

```bash
# Criar chart básico
helm create my-chart

# Estrutura gerada:
# my-chart/
# ├── Chart.yaml          # Metadados
# ├── values.yaml         # Valores padrão
# ├── charts/             # Dependências
# ├── templates/          # Templates Kubernetes
# │   ├── deployment.yaml
# │   ├── service.yaml
# │   ├── ingress.yaml
# │   ├── hpa.yaml
# │   ├── serviceaccount.yaml
# │   ├── _helpers.tpl    # Funções auxiliares
# │   ├── NOTES.txt       # Mensagem pós-instalação
# │   └── tests/
# │       └── test-connection.yaml
# └── .helmignore         # Arquivos ignorados
```

### Chart.yaml

```yaml
{{#include ../assets/helm/chart-yaml.yaml}}
```

### values.yaml

```yaml
{{#include ../assets/helm/values-yaml.yaml}}
```

### templates/deployment.yaml

```yaml
{{#include ../assets/helm/deployment-template.yaml}}
```

### templates/_helpers.tpl

```yaml
{{#include ../assets/helm/helpers-tpl.yaml}}
```

---

## Sintaxe de Templates

### Objetos Built-in

```yaml
{{#include ../assets/helm/template-objects.yaml}}
```

### Funções Comuns

```yaml
{{#include ../assets/helm/template-functions.yaml}}
```

### Indentação

```yaml
{{#include ../assets/helm/template-indent.yaml}}
```

---

## Dependências (Subcharts)

### Adicionar Dependências

```yaml
{{#include ../assets/helm/dependencies-chart.yaml}}
```

```bash
# Baixar dependências
helm dependency update ./my-chart

# Build com dependências
helm dependency build ./my-chart

# Listar dependências
helm dependency list ./my-chart
```

### Configurar Subchart

```yaml
{{#include ../assets/helm/dependencies-values.yaml}}
```

---

## Hooks

### Tipos de Hooks

```yaml
{{#include ../assets/helm/hook-job.yaml}}
```

### Hooks Disponíveis

| Hook | Descrição |
|------|-----------|
| `pre-install` | Antes de qualquer recurso ser criado |
| `post-install` | Após todos recursos serem criados |
| `pre-upgrade` | Antes do upgrade |
| `post-upgrade` | Após upgrade |
| `pre-rollback` | Antes de rollback |
| `post-rollback` | Após rollback |
| `pre-delete` | Antes de deletar recursos |
| `post-delete` | Após deletar recursos |

---

## Troubleshooting

### Debug de Templates

```bash
# Ver template renderizado
helm template my-release ./my-chart

# Debug com valores
helm template my-release ./my-chart --debug

# Dry-run com debug
helm install my-release ./my-chart --dry-run --debug

# Lint do chart
helm lint ./my-chart
```

### Problemas Comuns

```bash
# Erro: "release not found"
helm list -A | grep my-release

# Ver status detalhado
helm status my-release

# Ver eventos do namespace
kubectl get events -n my-namespace --sort-by='.lastTimestamp'

# Verificar valores aplicados
helm get values my-release

# Comparar com valores default
helm show values bitnami/nginx
```

---

## Dicas para o Exame CKAD

```plantuml,format=png
!include ../assets/diagrams/tools/helm-dicas-ckad-helm-1.puml
```

---

## Referências

- [Kustomize](kustomize.md)
- [ConfigMap](../configuration/configmap.md)
- [Secrets](../configuration/secrets.md)
- [Deployment](../workloads/deployment.md)
- [Ingress](../networking/ingress.md)
