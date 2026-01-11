# crictl

> **Certificação**: CKA (Troubleshooting - 30%)

## 📖 Conceitos

### O que é

`crictl` é a CLI para interagir com container runtimes compatíveis com CRI (Container Runtime Interface). Essencial para troubleshooting diretamente no node.

### Diferenças entre ferramentas

| Ferramenta | Escopo | Quando usar |
|------------|--------|-------------|
| **kubectl** | Kubernetes API | Operações normais no cluster |
| **crictl** | Container Runtime | Debug no node, containers travados |
| **docker** | Docker daemon | Legado (se ainda usar Docker) |

## 🔧 Comandos Essenciais

### Configuração do Endpoint

```bash
# Para containerd
crictl config runtime-endpoint unix:///run/containerd/containerd.sock

# Para CRI-O
crictl config runtime-endpoint unix:///var/run/crio/crio.sock

# Verificar configuração atual
crictl config --get runtime-endpoint
```

### Listar Recursos

```bash
# Containers rodando
crictl ps

# TODOS containers (incluindo parados)
crictl ps -a

# Pods/sandboxes
crictl pods

# Imagens disponíveis
crictl images

# Uso de recursos
crictl stats
```

### Debugging de Containers

```bash
# Ver logs
crictl logs <container-id>

# Follow logs (tempo real)
crictl logs -f <container-id>

# Últimas N linhas
crictl logs --tail 100 <container-id>

# Detalhes do container (JSON)
crictl inspect <container-id>

# Detalhes do pod
crictl inspectp <pod-id>

# Shell interativo
crictl exec -it <container-id> sh
crictl exec -it <container-id> /bin/bash
```

### Gerenciamento

```bash
# Parar container
crictl stop <container-id>

# Remover container
crictl rm <container-id>

# Parar pod
crictl stopp <pod-id>

# Remover pod
crictl rmp <pod-id>

# Baixar imagem
crictl pull nginx:1.20

# Remover imagem
crictl rmi nginx:1.20

# Limpar imagens não usadas
crictl rmi --prune
```

### Informações do Sistema

```bash
# Versão do runtime
crictl version

# Info do runtime
crictl info
```

## 💻 Exemplos Práticos

### Exemplo 1: Debugar CrashLoopBackOff

```bash
# 1. Identificar em qual node o pod está
kubectl get pods -o wide

# 2. SSH no node
ssh node-01

# 3. Listar containers (incluindo os que crasharam)
crictl ps -a | grep <nome-do-pod>

# 4. Ver logs do container que crashou
crictl logs <container-id>

# 5. Inspecionar detalhes do erro
crictl inspect <container-id> | jq '.status'
```

### Exemplo 2: Investigar ImagePullBackOff

```bash
# No node, tentar pull manual para ver erro detalhado
crictl pull registry.example.com/app:v1

# Verificar imagens disponíveis localmente
crictl images | grep app

# Inspecionar detalhes da imagem
crictl inspecti <image-id>
```

### Exemplo 3: Ver todos containers de um Pod

```bash
# Listar pods
crictl pods

# Ver containers do pod específico (incluindo pause)
crictl ps -a --pod <pod-id>
```

## 🐛 Troubleshooting

### Problema: connection refused

**Causa**: Runtime não está rodando ou endpoint incorreto

```bash
# Verificar se containerd está rodando
systemctl status containerd

# Verificar se socket existe
ls -la /run/containerd/containerd.sock

# Configurar endpoint correto
crictl config runtime-endpoint unix:///run/containerd/containerd.sock
```

### Problema: crictl stop não funciona permanentemente

**Explicação**: Kubernetes vai recriar o container automaticamente.

**Solução**: Use `kubectl delete pod` para parar permanentemente.

### Problema: Container não aparece no crictl

**Causa**: O container pode estar em outro node.

```bash
# Verificar node correto
kubectl get pods <pod-name> -o wide

# SSH no node correto
ssh <node-name>
crictl ps -a
```

### Arquivo de Configuração

```yaml
{{#include ../assets/nodes-components/crictl.yaml}}
```

## 🎓 Dicas para o Exame CKA

### Top 5 Comandos para Memorizar

```bash
crictl ps -a              # Ver todos containers
crictl logs <id>          # Ver logs
crictl inspect <id>       # Detalhes JSON
crictl exec -it <id> sh   # Shell no container
crictl pods               # Ver sandboxes
```

### Workflow de Troubleshooting no Exame

1. `kubectl get pods -o wide` → identificar node
2. `ssh <node>` → conectar no node
3. `crictl ps -a` → listar containers
4. `crictl logs <id>` → investigar logs
5. Voltar ao kubectl para correções

## 🔗 Referências

### Documentação
- [CRI tools - GitHub](https://github.com/kubernetes-sigs/cri-tools)
- [Kubernetes CRI](https://kubernetes.io/docs/concepts/architecture/cri/)

### Arquivos Relacionados
- [kubelet](../cluster-components/kubelet.md) - Componente que interage com runtime
- [ContainerD](../cluster-components/containerd.md) - Runtime padrão
- [Troubleshooting](../maintenance/troubleshooting.md) - Guia geral de troubleshooting
