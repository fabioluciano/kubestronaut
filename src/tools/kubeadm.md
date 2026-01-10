# kubeadm

```admonish info title="Certificações"
CKA (25%), CKS (10%)
```

## 📖 Conceitos

### O que é

`kubeadm` é a ferramenta oficial para bootstrapping de clusters Kubernetes. Automatiza instalação e configuração do control plane e worker nodes.

### Quando usar
- Criar clusters do zero
- Adicionar nodes ao cluster
- Fazer upgrade de versões
- Gerenciar certificados

## 🔧 Comandos Essenciais

### Inicializar Cluster (Control Plane)

```bash
# Básico
sudo kubeadm init

# Com CIDR para pod network (necessário para CNI)
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Com IP específico do API server
sudo kubeadm init \
  --apiserver-advertise-address=192.168.1.10 \
  --pod-network-cidr=10.244.0.0/16

# Para HA com endpoint externo
sudo kubeadm init \
  --control-plane-endpoint "lb.example.com:6443" \
  --upload-certs \
  --pod-network-cidr=10.244.0.0/16

# Com arquivo de configuração
sudo kubeadm init --config kubeadm-config.yaml
```

### Após o init - Configurar kubectl

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### Juntar Nodes ao Cluster

```bash
# Worker node (comando fornecido pelo init)
sudo kubeadm join 192.168.1.10:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:xxx

# Control plane adicional (HA)
sudo kubeadm join 192.168.1.10:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:xxx \
  --control-plane \
  --certificate-key yyy
```

### Gerenciar Tokens

```bash
# Listar tokens existentes
kubeadm token list

# Criar novo token (expira em 24h)
kubeadm token create

# Criar token sem expiração
kubeadm token create --ttl 0

# Criar e imprimir comando join completo
kubeadm token create --print-join-command

# Deletar token
kubeadm token delete <token>
```

### Upgrade do Cluster

```bash
# 1. Ver plano de upgrade
sudo kubeadm upgrade plan

# 2. Aplicar upgrade no primeiro control plane
sudo kubeadm upgrade apply v1.29.0

# 3. Upgrade dos outros control planes
sudo kubeadm upgrade node

# 4. Upgrade dos workers (após atualizar pacotes)
sudo kubeadm upgrade node
```

### Workflow Completo de Upgrade

```bash
# === CONTROL PLANE (primeiro node) ===

# Atualizar kubeadm
sudo apt-mark unhold kubeadm
sudo apt-get update && sudo apt-get install -y kubeadm=1.29.0-00
sudo apt-mark hold kubeadm

# Ver plano e aplicar
sudo kubeadm upgrade plan
sudo kubeadm upgrade apply v1.29.0

# Atualizar kubelet e kubectl
sudo apt-mark unhold kubelet kubectl
sudo apt-get install -y kubelet=1.29.0-00 kubectl=1.29.0-00
sudo apt-mark hold kubelet kubectl

# Reiniciar kubelet
sudo systemctl daemon-reload
sudo systemctl restart kubelet

# === WORKERS (cada node) ===

# No control plane: drenar o node
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# No worker: atualizar pacotes
sudo apt-mark unhold kubeadm kubelet kubectl
sudo apt-get update
sudo apt-get install -y kubeadm=1.29.0-00 kubelet=1.29.0-00 kubectl=1.29.0-00
sudo apt-mark hold kubeadm kubelet kubectl

# Upgrade config
sudo kubeadm upgrade node

# Reiniciar
sudo systemctl daemon-reload
sudo systemctl restart kubelet

# No control plane: liberar node
kubectl uncordon <node-name>
```

### Gerenciar Certificados

```bash
# Ver expiração de todos certificados
sudo kubeadm certs check-expiration

# Renovar todos certificados
sudo kubeadm certs renew all

# Renovar certificado específico
sudo kubeadm certs renew apiserver
sudo kubeadm certs renew apiserver-kubelet-client
```

### Reset (Limpar Node)

```bash
# Remover configuração do cluster
sudo kubeadm reset

# Limpar iptables
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X

# Remover diretórios
sudo rm -rf /etc/kubernetes/
sudo rm -rf /var/lib/etcd/
sudo rm -rf $HOME/.kube/
```

### Configuração

```bash
# Imprimir config padrão de init
kubeadm config print init-defaults

# Imprimir config padrão de join
kubeadm config print join-defaults

# Listar imagens necessárias
kubeadm config images list

# Baixar imagens antecipadamente
kubeadm config images pull
```

## 💻 Exemplos Práticos

### Exemplo 1: Cluster Simples (1 master + 2 workers)

```bash
# No control plane
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Configurar kubectl
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Instalar CNI (Flannel)
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

# Pegar comando join
kubeadm token create --print-join-command

# Nos workers, executar o comando join
sudo kubeadm join 192.168.1.10:6443 --token xxx --discovery-token-ca-cert-hash sha256:yyy
```

### Exemplo 2: Arquivo de Configuração

```yaml
{{#include ../assets/kubeadm/kubeadm-config.yaml}}
```

```bash
sudo kubeadm init --config kubeadm-config.yaml
```

## 🐛 Troubleshooting

### Problema: Port 6443 is in use

**Causa**: Instalação anterior não foi limpa

```bash
sudo kubeadm reset
sudo rm -rf /etc/kubernetes/ /var/lib/etcd/
```

### Problema: Container runtime not running

```bash
sudo systemctl status containerd
sudo systemctl start containerd
sudo systemctl enable containerd
```

### Problema: Token expirado

```bash
# Criar novo token com comando join
kubeadm token create --print-join-command
```

### Problema: Nodes NotReady

**Causa**: CNI não instalado

```bash
# Instalar CNI (Calico, Flannel, Weave, etc)
kubectl apply -f <cni-manifest-url>

# Verificar pods do kube-system
kubectl get pods -n kube-system
```

## 🎓 Dicas para o Exame CKA

### Comandos Mais Usados

```bash
# Join rápido
kubeadm token create --print-join-command

# Ver plano de upgrade
kubeadm upgrade plan

# Aplicar upgrade
kubeadm upgrade apply v1.29.0

# Reset node
kubeadm reset
```

### Workflow de Upgrade (MEMORIZAR!)

1. Drenar: `kubectl drain <node> --ignore-daemonsets`
2. Atualizar pacotes (apt/yum)
3. `kubeadm upgrade apply` (control plane) ou `kubeadm upgrade node` (outros)
4. Reiniciar: `systemctl restart kubelet`
5. Liberar: `kubectl uncordon <node>`

## 🔗 Referências

### Documentação
- [kubeadm docs](https://kubernetes.io/docs/reference/setup-tools/kubeadm/)
- [Creating cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- [Upgrading clusters](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)

### Arquivos Relacionados
- [Install](../maintenance/install.md) - Instalação do cluster
- [Cluster Upgrade](../maintenance/cluster-upgrade.md) - Detalhes de upgrade
- [High Availability](fundamentals/high-availability.md) - Configuração HA
- [etcd](../cluster-components/etcd.md) - Backend do cluster
