# Cluster Kubernetes

> **Certificacoes**: CKA (25%), KCNA (22%), CKS (10%)

## Conceitos Fundamentais

### O que e um Cluster Kubernetes?

Um cluster Kubernetes e um conjunto de maquinas (nodes) que executam aplicacoes containerizadas gerenciadas pelo Kubernetes. O cluster fornece abstracao sobre a infraestrutura, permitindo que voce trate multiplas maquinas como um unico sistema.

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-o-que-e-um-cluster-kubernetes.puml
```

### Beneficios de um Cluster

| Beneficio | Descricao |
|-----------|-----------|
| **Alta Disponibilidade** | Pods redistribuidos se nodes falham |
| **Escalabilidade** | Adicione nodes conforme demanda |
| **Isolamento** | Namespaces e Network Policies |
| **Self-Healing** | Containers reiniciados automaticamente |
| **Load Balancing** | Distribuicao de carga automatica |
| **Rolling Updates** | Atualizacoes sem downtime |

---

## Tipos de Clusters

### Por Ambiente

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-tipos-de-clusters-por-ambiente.puml
```

### Comparacao de Opcoes de Desenvolvimento

| Ferramenta | Nodes | Velocidade | Recursos | Uso |
|------------|-------|------------|----------|-----|
| **Minikube** | 1+ | Media | Medio | Aprendizado, dev |
| **Kind** | 1+ | Rapido | Baixo | CI/CD, testes |
| **k3d** | 1+ | Rapido | Baixo | Dev, edge |
| **Docker Desktop** | 1 | Medio | Alto | Dev local |

### Comparacao de Opcoes Managed

| Servico | Provider | Vantagens | Desvantagens |
|---------|----------|-----------|--------------|
| **EKS** | AWS | Integracao AWS, Fargate | Custo, complexidade |
| **GKE** | Google | Autopilot, melhor K8s | Vendor lock-in |
| **AKS** | Azure | Integracao Azure AD | Menos maduro |
| **DOKS** | Digital Ocean | Simples, custo baixo | Menos features |

---

## Componentes do Cluster

### Visao Geral

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-componentes-do-cluster.puml
```

### Componentes Obrigatorios

| Componente | Localizacao | Funcao |
|------------|-------------|--------|
| **kube-apiserver** | Control Plane | Frontend da API, ponto central |
| **etcd** | Control Plane | Armazenamento de estado |
| **kube-scheduler** | Control Plane | Agenda pods em nodes |
| **kube-controller-manager** | Control Plane | Executa controllers |
| **kubelet** | Cada Node | Agente que gerencia pods |
| **kube-proxy** | Cada Node | Networking de Services |
| **Container Runtime** | Cada Node | Executa containers |

### Add-ons Comuns

| Add-on | Funcao | Obrigatorio? |
|--------|--------|--------------|
| **CoreDNS** | DNS interno do cluster | Sim (na pratica) |
| **CNI Plugin** | Rede entre pods | Sim |
| **Ingress Controller** | Roteamento HTTP externo | Nao (mas comum) |
| **Metrics Server** | Metricas para HPA | Nao (mas comum) |
| **Dashboard** | UI web | Nao |

---

## Nodes

### O que e um Node?

Um node e uma maquina (fisica ou virtual) que faz parte do cluster e executa pods.

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-anatomia-de-um-node.puml
```

### Tipos de Nodes

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-tipos-de-nodes.puml
```

### Comandos de Gerenciamento de Nodes

```bash
# Listar nodes
kubectl get nodes
kubectl get nodes -o wide

# Ver detalhes de um node
kubectl describe node <node-name>

# Ver capacidade e alocacao
kubectl describe node <node-name> | grep -A 10 "Allocated resources"

# Labels de um node
kubectl get nodes --show-labels
kubectl label node <node-name> disktype=ssd
kubectl label node <node-name> disktype-  # remove label

# Taints
kubectl taint nodes <node-name> key=value:NoSchedule
kubectl taint nodes <node-name> key=value:NoSchedule-  # remove

# Cordon (impede novos pods)
kubectl cordon <node-name>

# Uncordon (permite novos pods)
kubectl uncordon <node-name>

# Drain (remove pods para manutencao)
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Ver recursos do node
kubectl top node
kubectl top node <node-name>
```

### Node Conditions

| Condition | Significado |
|-----------|-------------|
| **Ready** | Node saudavel e pronto para pods |
| **MemoryPressure** | Memoria baixa |
| **DiskPressure** | Disco baixo |
| **PIDPressure** | Muitos processos |
| **NetworkUnavailable** | Rede nao configurada |

---

## Namespaces

### O que sao Namespaces?

Namespaces sao clusters virtuais dentro do cluster fisico, usados para isolamento logico.

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-namespaces-isolamento-logico.puml
```

### Namespaces Padrao

| Namespace | Uso |
|-----------|-----|
| **default** | Recursos sem namespace especificado |
| **kube-system** | Componentes do sistema Kubernetes |
| **kube-public** | Recursos publicos (legiveis por todos) |
| **kube-node-lease** | Leases de heartbeat dos nodes |

### Comandos de Namespace

```bash
# Listar namespaces
kubectl get namespaces
kubectl get ns

# Criar namespace
kubectl create namespace dev
kubectl create ns prod

# Definir namespace padrao no contexto
kubectl config set-context --current --namespace=dev

# Ver namespace atual
kubectl config view --minify | grep namespace

# Recursos em um namespace especifico
kubectl get pods -n kube-system
kubectl get all -n production

# Recursos em todos namespaces
kubectl get pods -A
kubectl get pods --all-namespaces

# Deletar namespace (deleta tudo dentro!)
kubectl delete namespace dev
```

### Exemplo de ResourceQuota por Namespace

```yaml
../assets/resource-quota/resourcequota-compute-quota.yaml}}
```

---

## Contextos e kubeconfig

### Estrutura do kubeconfig

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-estrutura-do-kubeconfig.puml
```

### Exemplo de kubeconfig

```yaml
../assets/cluster-components/config-kubernetes-1.yaml}}
```

### Comandos de Contexto

```bash
# Ver configuracao atual
kubectl config view
kubectl config view --minify

# Listar contextos
kubectl config get-contexts

# Ver contexto atual
kubectl config current-context

# Mudar contexto
kubectl config use-context dev-context

# Criar novo contexto
kubectl config set-context my-context \
  --cluster=kubernetes \
  --user=developer \
  --namespace=dev

# Usar kubeconfig diferente
kubectl --kubeconfig=/path/to/config get pods
export KUBECONFIG=/path/to/config

# Merge de kubeconfigs
export KUBECONFIG=~/.kube/config:~/.kube/config-dev
kubectl config view --flatten > ~/.kube/config-merged
```

---

## Verificacao do Cluster

### Comandos de Verificacao

```bash
# Informacoes basicas do cluster
kubectl cluster-info
kubectl cluster-info dump

# Versao do servidor e cliente
kubectl version
kubectl version --short

# Ver todos os recursos em todos namespaces
kubectl get all -A

# Status dos nodes
kubectl get nodes
kubectl describe nodes

# Componentes do control plane
kubectl get pods -n kube-system
kubectl get componentstatuses  # Legado, pode nao funcionar

# Verificar API Server
kubectl get --raw='/healthz'
kubectl get --raw='/readyz'
kubectl get --raw='/livez'

# Verificar ETCD (se acessivel)
kubectl get --raw='/healthz/etcd'

# Verificar DNS
kubectl run test-dns --image=busybox:1.28 --rm -it --restart=Never -- nslookup kubernetes
```

### Checklist de Saude do Cluster

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-checklist-de-saude-do-cluster.puml
```

### Script de Verificacao

```bash
#!/bin/bash
# Verificacao rapida do cluster

echo "=== Versao do Cluster ==="
kubectl version --short

echo ""
echo "=== Status dos Nodes ==="
kubectl get nodes

echo ""
echo "=== Pods do Sistema ==="
kubectl get pods -n kube-system

echo ""
echo "=== Componentes ==="
kubectl get pods -n kube-system -o wide | grep -E "etcd|apiserver|scheduler|controller"

echo ""
echo "=== Eventos Recentes ==="
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20

echo ""
echo "=== Recursos dos Nodes ==="
kubectl top nodes 2>/dev/null || echo "Metrics server nao disponivel"
```

---

## Criacao de Cluster

### Com kubeadm (CKA)

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-criacao-de-cluster-com-kubeadm.puml
```

```bash
# No Control Plane
sudo kubeadm init \
  --apiserver-advertise-address=192.168.1.10 \
  --pod-network-cidr=10.244.0.0/16

# Configurar kubectl
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Instalar CNI (Calico exemplo)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Nos Workers (comando fornecido pelo kubeadm init)
sudo kubeadm join 192.168.1.10:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:...
```

### Com Kind (Desenvolvimento)

```bash
# Instalar kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/

# Criar cluster simples
kind create cluster --name dev

# Criar cluster multi-node
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
EOF

# Listar clusters
kind get clusters

# Deletar cluster
kind delete cluster --name dev
```

### Com Minikube (Desenvolvimento)

```bash
# Instalar minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Criar cluster
minikube start

# Com opcoes
minikube start \
  --driver=docker \
  --cpus=4 \
  --memory=8g \
  --nodes=3

# Status
minikube status

# Dashboard
minikube dashboard

# Deletar
minikube delete
```

---

## Dicas para o Exame

### CKA - Cluster Management

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-dicas-cka-cluster.puml
```

### KCNA - Conceitos

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-kcna-conceitos-cluster.puml
```

---

## Referencias

### Links Internos

- [Arquitetura](fundamentals/arquitetura.md) - Detalhes da arquitetura
- [Instalacao](maintenance/install.md) - Instalacao do cluster
- [Alta Disponibilidade](fundamentals/high-availability.md) - Clusters HA
- [kubeadm](tools/kubeadm.md) - Ferramenta de bootstrap
- [Backup e Restore](maintenance/backup-e-restore.md) - Backup do cluster
- [Troubleshooting](maintenance/troubleshooting.md) - Resolucao de problemas

### Documentacao Oficial

- [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- [Nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)
- [Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- [Configure Access to Multiple Clusters](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)

---

## Best Practices

### Planejamento de Cluster

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-best-practices-cluster.puml
```

### Configuracao de Namespaces

| Padrao | Descricao |
|--------|-----------|
| **Por ambiente** | dev, staging, prod em namespaces diferentes |
| **Por time** | team-a, team-b para isolamento de times |
| **Por aplicacao** | app-frontend, app-backend para grandes sistemas |
| **Hibrido** | prod-team-a, dev-team-b combinando criterios |

### Limites e Quotas

```yaml
../assets/limit-range/limitrange-default-limits.yaml}}
```

---

## Troubleshooting de Cluster

### Arvore de Decisao

```plantuml,format=png
../assets/diagrams/cluster-components/cluster-troubleshooting-arvore-de-decisao.puml
```

### Problemas e Solucoes

| Problema | Causa Provavel | Solucao |
|----------|----------------|---------|
| **kubectl timeout** | API Server down ou rede | Verificar API Server e firewall |
| **Node NotReady** | kubelet ou runtime com problema | `journalctl -u kubelet` |
| **Pods Pending** | Recursos insuficientes ou taints | `kubectl describe pod` |
| **CrashLoopBackOff** | Aplicacao com erro | `kubectl logs pod` |
| **ImagePullBackOff** | Imagem nao encontrada | Verificar nome da imagem e credenciais |
| **DNS nao resolve** | CoreDNS com problema | `kubectl get pods -n kube-system -l k8s-app=kube-dns` |

### Comandos de Emergencia

```bash
# === DIAGNOSTICO RAPIDO ===

# Cluster acessivel?
kubectl cluster-info
kubectl get --raw='/healthz'

# Nodes saudaveis?
kubectl get nodes
kubectl top nodes

# Sistema OK?
kubectl get pods -n kube-system
kubectl get events -n kube-system --sort-by='.lastTimestamp'

# === NO NODE COM PROBLEMA ===

# kubelet rodando?
systemctl status kubelet
journalctl -u kubelet -f --since "5 minutes ago"

# Container runtime OK?
crictl info
crictl ps
systemctl status containerd

# Disco e memoria?
df -h
free -m

# === REDE ===

# Testar DNS
kubectl run test-dns --image=busybox --rm -it -- nslookup kubernetes.default

# Testar conectividade entre pods
kubectl run test-net --image=nicolaka/netshoot --rm -it -- bash

# === ETCD ===

# Saude do etcd
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health
```

---

## Comandos Rapidos

```bash
# === INFORMACOES ===
kubectl cluster-info
kubectl get nodes -o wide
kubectl version --short

# === NODES ===
kubectl get nodes
kubectl describe node <node>
kubectl top node
kubectl cordon <node>
kubectl uncordon <node>
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data

# === NAMESPACES ===
kubectl get ns
kubectl create ns <name>
kubectl config set-context --current --namespace=<name>
kubectl get all -n <namespace>
kubectl delete ns <name>

# === CONTEXTOS ===
kubectl config get-contexts
kubectl config current-context
kubectl config use-context <context>

# === SAUDE ===
kubectl get --raw='/healthz'
kubectl get --raw='/readyz'
kubectl get events -A --sort-by='.lastTimestamp'
kubectl get pods -n kube-system

# === CRIACAO ===
kubeadm init --pod-network-cidr=10.244.0.0/16
kubeadm join <master>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
kubeadm token create --print-join-command
```

---

> **Resumo**: Um cluster Kubernetes consiste em Control Plane (API Server, etcd, Scheduler, Controller Manager) e Worker Nodes (kubelet, kube-proxy, container runtime). Namespaces fornecem isolamento logico. Contextos no kubeconfig permitem gerenciar multiplos clusters. Para producao, use clusters managed (EKS, GKE, AKS) ou kubeadm com HA. Para desenvolvimento, use Kind, Minikube ou k3d. Sempre tenha backup do etcd e monitoramento ativo.
