# Upgrade do Cluster

## Conceitos Fundamentais

### Política de Versões

O Kubernetes suporta apenas as **3 últimas minor versions**. Upgrades devem ser feitos **uma minor version por vez**.

```plantuml,format=png
!include ../assets/diagrams/maintenance/cluster-upgrade-compatibilidade-de-versões.puml
```

### Regras de Upgrade

```plantuml,format=png
!include ../assets/diagrams/maintenance/cluster-upgrade-diagram-2.puml
```

---

## Ordem de Upgrade

```plantuml,format=png
!include ../assets/diagrams/maintenance/cluster-upgrade-ordem-de-upgrade.puml
```

### Fluxo Completo de Upgrade

O diagrama abaixo mostra o fluxo detalhado de upgrade, incluindo os comandos específicos para cada etapa:

```plantuml,format=png
!include ../assets/diagrams/maintenance/cluster-upgrade-fluxo-completo.puml
```

---

## Pré-Requisitos

### 1. Verificar Versão Atual

```bash
# Versão do cluster
kubectl version

# Versão dos nodes
kubectl get nodes

# Versão do kubeadm
kubeadm version
```

### 2. Fazer Backup do etcd

```bash
export ETCDCTL_API=3
etcdctl snapshot save /tmp/etcd-backup-pre-upgrade.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

### 3. Verificar Plano de Upgrade

```bash
# Ver versões disponíveis
sudo kubeadm upgrade plan
```

---

## Upgrade do Control Plane

### Passo 1: Atualizar Repositório (Ubuntu/Debian)

```bash
# Versão desejada
VERSION=1.30

# Adicionar repositório da nova versão
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v${VERSION}/deb/ /" | \
  sudo tee /etc/apt/sources.list.d/kubernetes.list

# Atualizar cache
sudo apt update

# Ver versões disponíveis
apt-cache madison kubeadm
```

### Passo 2: Atualizar kubeadm

```bash
# Desbloquear pacote
sudo apt-mark unhold kubeadm

# Atualizar kubeadm
sudo apt update && sudo apt install -y kubeadm=1.30.0-1.1

# Bloquear novamente
sudo apt-mark hold kubeadm

# Verificar versão
kubeadm version
```

### Passo 3: Verificar Plano de Upgrade

```bash
# Ver o que será atualizado
sudo kubeadm upgrade plan

# Output mostra:
# - Versão atual
# - Versão disponível
# - Componentes que serão atualizados
```

### Passo 4: Aplicar Upgrade (Primeiro Control Plane)

```bash
# Aplicar upgrade no primeiro master
sudo kubeadm upgrade apply v1.30.0

# Aguardar conclusão
# [upgrade/successful] SUCCESS! Your cluster was upgraded to "v1.30.0"
```

### Passo 5: Drain do Node

```bash
# Remover workloads do node (de outro terminal/node)
kubectl drain <control-plane-node> --ignore-daemonsets --delete-emptydir-data

# Ou se estiver no mesmo node
kubectl drain $(hostname) --ignore-daemonsets --delete-emptydir-data
```

### Passo 6: Atualizar kubelet e kubectl

```bash
# Desbloquear pacotes
sudo apt-mark unhold kubelet kubectl

# Atualizar
sudo apt update && sudo apt install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1

# Bloquear
sudo apt-mark hold kubelet kubectl

# Reiniciar kubelet
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

### Passo 7: Uncordon do Node

```bash
# Permitir scheduling novamente
kubectl uncordon <control-plane-node>

# Verificar status
kubectl get nodes
```

---

## Upgrade de Control Planes Adicionais

Para clusters HA, após atualizar o primeiro control plane:

```bash
# No segundo/terceiro control plane:

# 1. Atualizar kubeadm
sudo apt-mark unhold kubeadm
sudo apt update && sudo apt install -y kubeadm=1.30.0-1.1
sudo apt-mark hold kubeadm

# 2. Upgrade (usar "node" ao invés de "apply")
sudo kubeadm upgrade node

# 3. Drain
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# 4. Atualizar kubelet/kubectl
sudo apt-mark unhold kubelet kubectl
sudo apt update && sudo apt install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1
sudo apt-mark hold kubelet kubectl
sudo systemctl daemon-reload
sudo systemctl restart kubelet

# 5. Uncordon
kubectl uncordon <node-name>
```

---

## Upgrade dos Worker Nodes

### Passo 1: Drain do Worker

```bash
# Do control plane, drain o worker
kubectl drain <worker-node> --ignore-daemonsets --delete-emptydir-data
```

### Passo 2: No Worker - Atualizar kubeadm

```bash
# SSH no worker node
ssh <worker-node>

# Atualizar kubeadm
sudo apt-mark unhold kubeadm
sudo apt update && sudo apt install -y kubeadm=1.30.0-1.1
sudo apt-mark hold kubeadm
```

### Passo 3: Upgrade do Node

```bash
# Atualizar configuração do node
sudo kubeadm upgrade node
```

### Passo 4: Atualizar kubelet e kubectl

```bash
# Atualizar pacotes
sudo apt-mark unhold kubelet kubectl
sudo apt update && sudo apt install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1
sudo apt-mark hold kubelet kubectl

# Reiniciar kubelet
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

### Passo 5: Uncordon do Worker

```bash
# Do control plane
kubectl uncordon <worker-node>

# Verificar
kubectl get nodes
```

---

## Comandos Resumidos

### Control Plane Principal

```bash
# 1. kubeadm
apt-mark unhold kubeadm && apt install -y kubeadm=1.30.0-1.1 && apt-mark hold kubeadm

# 2. Verificar e aplicar
kubeadm upgrade plan
kubeadm upgrade apply v1.30.0

# 3. Drain
kubectl drain <node> --ignore-daemonsets

# 4. kubelet/kubectl
apt-mark unhold kubelet kubectl
apt install -y kubelet=1.30.0-1.1 kubectl=1.30.0-1.1
apt-mark hold kubelet kubectl
systemctl daemon-reload && systemctl restart kubelet

# 5. Uncordon
kubectl uncordon <node>
```

### Control Planes Adicionais / Workers

```bash
# 1. kubeadm
apt-mark unhold kubeadm && apt install -y kubeadm=1.30.0-1.1 && apt-mark hold kubeadm

# 2. Upgrade node (não apply!)
kubeadm upgrade node

# 3-5: Mesmo que acima (drain, kubelet, uncordon)
```

---

## Verificação Pós-Upgrade

```bash
# Verificar versões dos nodes
kubectl get nodes

# Verificar componentes do cluster
kubectl get pods -n kube-system

# Verificar versão do API server
kubectl version

# Testar funcionalidade
kubectl create deployment test --image=nginx
kubectl get pods
kubectl delete deployment test
```

---

## Troubleshooting

### kubelet Não Inicia Após Upgrade

```bash
# Ver status
systemctl status kubelet

# Ver logs
journalctl -u kubelet -f

# Verificar configuração
cat /var/lib/kubelet/config.yaml
```

### Pods Stuck em Terminating Após Drain

```bash
# Forçar delete
kubectl delete pod <pod-name> --grace-period=0 --force

# Ou ignorar pods com local storage
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --force
```

### Upgrade Falhou

```bash
# Ver logs do kubeadm
kubeadm upgrade apply v1.30.0 --v=5

# Resetar se necessário (CUIDADO!)
kubeadm reset

# Restaurar backup do etcd se necessário
```

---

## Dicas para o Exame CKA

```plantuml,format=png
!include ../assets/diagrams/maintenance/cluster-upgrade-diagram-4.puml
```

---

## Referências

- [Backup e Restore](backup-e-restore.md)
- [kubeadm](../tools/kubeadm.md)
- [kubelet](../cluster-components/kubelet.md)
- [OS Upgrade](os-upgrade.md)
- [High Availability](fundamentals/high-availability.md)
