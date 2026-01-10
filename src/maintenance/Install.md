# Instalacao do Cluster Kubernetes

> **Certificacoes**: CKA (25%)

## Conceitos

A instalacao de um cluster Kubernetes envolve diversos componentes que precisam ser configurados corretamente para garantir o funcionamento adequado. O `kubeadm` e a ferramenta oficial para bootstrap de clusters Kubernetes, simplificando significativamente o processo de instalacao.

```plantuml,format=png
!include ../assets/diagrams/maintenance/install-arquitetura-de-um-cluster-kubernetes.puml
```

### Fluxo de Instalação

```plantuml,format=png
!include ../assets/diagrams/maintenance/install-fluxo-instalacao.puml
```

### Componentes Necessarios

| Componente | Funcao | Obrigatorio |
|------------|--------|-------------|
| Container Runtime | Executa os containers (containerd, CRI-O) | Sim |
| kubeadm | Bootstrap do cluster | Sim |
| kubelet | Agente que roda em cada node | Sim |
| kubectl | CLI para interagir com o cluster | Sim |
| CNI Plugin | Rede entre pods (Calico, Flannel, Cilium) | Sim |

## Pre-requisitos

### Requisitos de Hardware

```admonish info title="Requisitos Minimos"
**Control Plane:**
- 2 CPUs
- 2 GB RAM
- 20 GB disco

**Worker Nodes:**
- 1 CPU
- 1 GB RAM
- 10 GB disco
```

### Requisitos de Sistema Operacional

```bash
# Verificar versao do SO (Ubuntu/Debian recomendado)
cat /etc/os-release

# Verificar arquitetura
uname -m
# Esperado: x86_64 ou aarch64
```

### Configuracoes de Rede

```bash
# 1. Verificar conectividade entre nodes
ping <ip-do-outro-node>

# 2. Verificar portas necessarias
# Control Plane
# - 6443: API Server
# - 2379-2380: etcd
# - 10250: Kubelet API
# - 10259: kube-scheduler
# - 10257: kube-controller-manager

# Worker Nodes
# - 10250: Kubelet API
# - 30000-32767: NodePort Services
```

### Desabilitar Swap

```bash
# Desabilitar swap temporariamente
sudo swapoff -a

# Desabilitar swap permanentemente
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# Verificar se swap esta desabilitado
free -h
# Swap deve mostrar 0
```

### Configurar Modulos do Kernel

```bash
# Carregar modulos necessarios
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Verificar se modulos estao carregados
lsmod | grep br_netfilter
lsmod | grep overlay
```

### Configurar Parametros de Rede do Kernel

```bash
# Configurar sysctl
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# Aplicar configuracoes
sudo sysctl --system

# Verificar configuracoes
sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward
```

## Instalacao do Container Runtime (containerd)

```plantuml,format=png
!include ../assets/diagrams/maintenance/install-fluxo-de-instalacao-do-container-runtime.puml
```

### Instalar containerd

```bash
# 1. Instalar dependencias
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# 2. Adicionar chave GPG do Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 3. Adicionar repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Instalar containerd
sudo apt-get update
sudo apt-get install -y containerd.io
```

### Configurar containerd

```bash
# Gerar configuracao padrao
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

# Configurar SystemdCgroup (IMPORTANTE!)
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml

# Reiniciar containerd
sudo systemctl restart containerd
sudo systemctl enable containerd

# Verificar status
sudo systemctl status containerd
```

```admonish warning title="Atencao"
A configuracao `SystemdCgroup = true` e **obrigatoria** para que o kubelet funcione corretamente com o containerd. Sem essa configuracao, os pods podem entrar em CrashLoopBackOff.
```

## Instalacao do kubeadm, kubelet e kubectl

```bash
# 1. Adicionar chave GPG do Kubernetes
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# 2. Adicionar repositorio
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

# 3. Instalar kubeadm, kubelet e kubectl
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

# 4. Fixar versao para evitar upgrades automaticos
sudo apt-mark hold kubelet kubeadm kubectl

# 5. Verificar versoes instaladas
kubeadm version
kubelet --version
kubectl version --client
```

## Inicializacao do Cluster (Control Plane)

```plantuml,format=png
!include ../assets/diagrams/maintenance/install-fluxo-de-inicializacao-com-kubeadm.puml
```

### kubeadm init - Opcoes Importantes

```bash
# Inicializacao basica
sudo kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --apiserver-advertise-address=192.168.1.10

# Com arquivo de configuracao (recomendado)
sudo kubeadm init --config=kubeadm-config.yaml

# Com upload de certificados (HA)
sudo kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --control-plane-endpoint="k8s.example.com:6443" \
  --upload-certs
```

### Arquivo de Configuracao kubeadm

```yaml
{{#include ../assets/kubeadm/kubeadm-config.yaml}}
```

### Flags Importantes do kubeadm init

| Flag | Descricao | Exemplo |
|------|-----------|---------|
| `--pod-network-cidr` | CIDR para rede de pods | `10.244.0.0/16` (Flannel) |
| `--service-cidr` | CIDR para services | `10.96.0.0/12` |
| `--apiserver-advertise-address` | IP do API Server | `192.168.1.10` |
| `--control-plane-endpoint` | Endpoint para HA | `k8s.example.com:6443` |
| `--upload-certs` | Upload de certs para join de control planes | - |
| `--cri-socket` | Socket do container runtime | `unix:///run/containerd/containerd.sock` |
| `--kubernetes-version` | Versao do Kubernetes | `v1.29.0` |
| `--config` | Arquivo de configuracao | `kubeadm-config.yaml` |
| `--dry-run` | Simular sem executar | - |

### Configurar kubectl apos init

```bash
# Criar diretorio .kube
mkdir -p $HOME/.kube

# Copiar arquivo de configuracao
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

# Ajustar permissoes
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Verificar conexao
kubectl cluster-info
kubectl get nodes
```

## Instalacao do CNI Plugin

```admonish note title="Redes de Pods"
O CNI (Container Network Interface) e responsavel pela comunicacao entre pods em diferentes nodes. Sem um CNI plugin instalado, os pods ficarao em estado `Pending`.
```

### Calico (Recomendado para producao)

```bash
# Instalar Calico
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/calico.yaml

# Verificar instalacao
kubectl get pods -n kube-system | grep calico
```

### Flannel (Simples e leve)

```bash
# Instalar Flannel
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml

# Verificar instalacao
kubectl get pods -n kube-flannel
```

### Cilium (Recursos avancados)

```bash
# Instalar Cilium CLI
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz

# Instalar Cilium no cluster
cilium install

# Verificar instalacao
cilium status
```

### Comparacao de CNI Plugins

| Plugin | Complexidade | NetworkPolicy | Performance | Uso |
|--------|--------------|---------------|-------------|-----|
| Calico | Media | Sim | Alta | Producao |
| Flannel | Baixa | Nao | Media | Dev/Test |
| Cilium | Alta | Sim (L7) | Alta | Producao avancada |
| Weave | Baixa | Sim | Media | Pequenos clusters |

## Adicionar Worker Nodes

### Obter Comando de Join

```bash
# No control plane, gerar novo token e comando de join
kubeadm token create --print-join-command

# Saida esperada:
# kubeadm join 192.168.1.10:6443 --token abcdef.0123456789abcdef \
#   --discovery-token-ca-cert-hash sha256:...
```

### Executar Join no Worker Node

```bash
# No worker node (como root)
sudo kubeadm join 192.168.1.10:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:...

# Verificar no control plane
kubectl get nodes
```

### Join de Control Plane Adicional (HA)

```bash
# Se usou --upload-certs durante init
sudo kubeadm join 192.168.1.10:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:... \
  --control-plane \
  --certificate-key <certificate-key>
```

## Verificacao Pos-Instalacao

```plantuml,format=png
!include ../assets/diagrams/maintenance/install-checklist-de-verificacao.puml
```

### Verificar Status dos Nodes

```bash
# Listar nodes
kubectl get nodes -o wide

# Todos devem estar Ready
# NAME           STATUS   ROLES           AGE   VERSION
# control-plane  Ready    control-plane   10m   v1.29.0
# worker-1       Ready    <none>          5m    v1.29.0
# worker-2       Ready    <none>          5m    v1.29.0
```

### Verificar Pods do Sistema

```bash
# Listar pods do kube-system
kubectl get pods -n kube-system

# Todos devem estar Running ou Completed
# NAME                                       READY   STATUS    RESTARTS   AGE
# coredns-5d78c9869d-xxxxx                   1/1     Running   0          10m
# coredns-5d78c9869d-yyyyy                   1/1     Running   0          10m
# etcd-control-plane                         1/1     Running   0          10m
# kube-apiserver-control-plane               1/1     Running   0          10m
# kube-controller-manager-control-plane      1/1     Running   0          10m
# kube-proxy-xxxxx                           1/1     Running   0          10m
# kube-scheduler-control-plane               1/1     Running   0          10m
```

### Testar DNS

```bash
# Criar pod de teste
kubectl run test-dns --image=busybox:1.28 --rm -it --restart=Never -- nslookup kubernetes

# Saida esperada:
# Server:    10.96.0.10
# Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local
#
# Name:      kubernetes
# Address 1: 10.96.0.1 kubernetes.default.svc.cluster.local
```

### Testar Comunicacao entre Pods

```bash
# Criar dois pods em nodes diferentes
kubectl run test-pod-1 --image=nginx --labels="app=test"
kubectl run test-pod-2 --image=busybox --rm -it --restart=Never -- wget -qO- test-pod-1

# Limpar
kubectl delete pod test-pod-1
```

## Comandos Uteis

### Gerenciamento de Tokens

```bash
# Listar tokens existentes
kubeadm token list

# Criar novo token
kubeadm token create

# Criar token com comando de join completo
kubeadm token create --print-join-command

# Remover token
kubeadm token delete <token>
```

### Verificar Configuracao

```bash
# Ver configuracao atual do cluster
kubectl cluster-info dump

# Ver configuracao do kubeadm
kubectl -n kube-system get cm kubeadm-config -o yaml

# Ver certificados
kubeadm certs check-expiration
```

### Reset do Cluster

```bash
# Reset completo (em todos os nodes)
sudo kubeadm reset -f

# Limpar configuracoes residuais
sudo rm -rf /etc/cni/net.d
sudo rm -rf $HOME/.kube/config
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X
```

## Troubleshooting de Instalacao

### Node NotReady

```bash
# Verificar status do kubelet
sudo systemctl status kubelet
sudo journalctl -u kubelet -f

# Verificar status do containerd
sudo systemctl status containerd
sudo journalctl -u containerd -f

# Causas comuns:
# - CNI nao instalado
# - containerd nao configurado corretamente
# - Swap habilitado
```

### Pods Pending

```bash
# Verificar eventos
kubectl describe pod <pod-name>

# Causas comuns:
# - CNI nao instalado (Pods de sistema)
# - Recursos insuficientes
# - Taints nos nodes
```

### CoreDNS CrashLoopBackOff

```bash
# Verificar logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Causas comuns:
# - Loop de DNS no host
# - Configuracao de rede incorreta

# Solucao: Editar ConfigMap do CoreDNS
kubectl edit cm coredns -n kube-system
# Adicionar na secao forward:
# forward . /etc/resolv.conf {
#   max_concurrent 1000
# }
```

### Erro de Certificado

```bash
# Regenerar certificados
sudo kubeadm certs renew all

# Verificar certificados
sudo kubeadm certs check-expiration
```

### Conexao Recusada ao API Server

```bash
# Verificar se apiserver esta rodando
sudo crictl ps | grep kube-apiserver

# Verificar logs
sudo crictl logs <container-id>

# Verificar manifesto
cat /etc/kubernetes/manifests/kube-apiserver.yaml
```

## Dicas para o Exame CKA

```admonish tip title="Dicas Importantes"
1. **Memorize os pre-requisitos**: swap off, modulos do kernel, sysctl
2. **Conheca as flags do kubeadm init**: --pod-network-cidr e essencial
3. **Saiba instalar CNI**: Calico e Flannel sao os mais comuns
4. **Pratique o troubleshooting**: kubelet e containerd sao pontos de falha comuns
5. **Conheca o kubeadm token**: criar e listar tokens
6. **Saiba fazer reset**: kubeadm reset para comecar do zero
```

## Referencias

- [Documentacao Oficial - Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- [Documentacao Oficial - Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- [Container Runtime Interface](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)
- [CNI Plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
