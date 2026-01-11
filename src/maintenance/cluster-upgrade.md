# Upgrade do Cluster

## Conceitos Fundamentais

### Política de Versões

O Kubernetes suporta apenas as **3 últimas minor versions**. Upgrades devem ser feitos **uma minor version por vez**.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Monospaced

title COMPATIBILIDADE DE VERSÕES

map "Versão Relativa ao API Server" as vmap {
  kube-apiserver => X (base)
  kube-controller-manager => X ou X-1
  kube-scheduler => X ou X-1
  kubelet => X, X-1 ou X-2
  kube-proxy => X, X-1 ou X-2
  kubectl => X+1, X ou X-1
}

note bottom of vmap
  **Exemplo (API Server v1.30):**
  • controller-manager: v1.30 ou v1.29
  • scheduler: v1.30 ou v1.29
  • kubelet: v1.30, v1.29 ou v1.28
  • kubectl: v1.31, v1.30 ou v1.29
end note

@enduml
```

### Regras de Upgrade

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Monospaced

rectangle "REGRAS IMPORTANTES" as rules

note right of rules
  ✓ Upgrade uma minor version por vez
    (1.28 → 1.29 → 1.30, NÃO 1.28 → 1.30)
  ✓ Control plane primeiro, workers depois
  ✓ kubeadm não atualiza kubelet (manual)
  ✓ Fazer backup do etcd antes!
  ✓ Durante upgrade, workloads continuam rodando
    (mas API pode ficar indisponível brevemente)
end note
@enduml
```

---

## Ordem de Upgrade

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Monospaced

title ORDEM DE UPGRADE

rectangle "1. Control Plane (Master) - um node por vez" as cp
note right of cp
  a. kubeadm
  b. Componentes do control plane (via kubeadm)
  c. kubelet e kubectl
end note

rectangle "2. Worker Nodes - um node por vez" as wk
note right of wk
  a. Drain do node
  b. kubeadm upgrade node
  c. kubelet e kubectl
  d. Uncordon do node
end note

cp -down-> wk
@enduml
```

### Fluxo Completo de Upgrade

O diagrama abaixo mostra o fluxo detalhado de upgrade, incluindo os comandos específicos para cada etapa:

```plantuml,format=png
@startuml

skinparam monochrome true
skinparam backgroundColor white
skinparam defaultFontName monospace
skinparam defaultTextAlignment center

title Fluxo de Upgrade do Cluster Kubernetes

start

:Adiciona-se o repositório da nova \nversão a lista de repositórios\n disponíveis no sistema;
:Executa o comando\n\n ""apt-cache madison kubeadm"";\n\n para descrobrir qual a última versão\n disponível para atualização;
floating note left: Será apresentada uma lista\n de versões da ""minor"" selecionada.

partition #lightPink """kubeadm""" {
	:Descongela o pacote ""kubeadm""\n\n""apt-mark unhold kubeadm"";
	:Atualiza o pacote ""kubeadm""\n\n""apt upgrade -y kubeadm=$VERSION"";
	:Congela o pacote ""kubeadm""\n\n""apt-mark hold kubeadm"";
}

partition #lightGreen "Componentes do nó" {
	if (É o controlplane principal) then(controlplane principal)
		:Executa o comando para planejar a atualização\n\n""sudo kubeadm upgrade plan"";
		:Atualiza os componentes do controlplane\n\n""sudo kubeadm upgrade apply v1.x.x"";
	else (Controlplane secundário ou Worker)
		:Atualiza os componentes do controlplane\n\n""sudo kubeadm upgrade node"";
	endif
}

:Remove todos os pods do no e o coloca em manutenção\n\n""kubectl drain node --ignore-daemonsets"";

partition #lightSkyBlue """kubelet""" {
	:Descongela o pacote ""kubelet""\n\n""apt-mark unhold kubelet"";
	:Atualiza o pacote ""kubelet""\n\n""apt upgrade -y kubelet=$VERSION"";
	:Congela o pacote ""kubelet""\n\n""apt-mark hold kubelet"";
	:Atualiza a lista de serviços\n\n""systemctl daemon-reload"";
	:Reinicia o ""kubelet""\n\n""systemctl restart kubelet"";
}

:Desmarca a manutenção do nó\n\n""kubectl uncordon node"";

stop

@enduml

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
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Monospaced

rectangle "DICAS CKA - CLUSTER UPGRADE" {
  rectangle "SEQUÊNCIA CORRETA" {
    :1. apt-mark unhold kubeadm;
    :2. apt install kubeadm=X.X.X-1.1;
    :3. apt-mark hold kubeadm;
    :4. kubeadm upgrade plan (verificar);
    :5. kubeadm upgrade apply vX.X.X (primeiro master)\n   OU kubeadm upgrade node (outros nodes);
    :6. kubectl drain <node> --ignore-daemonsets;
    :7. apt-mark unhold kubelet kubectl;
    :8. apt install kubelet=X.X.X-1.1 kubectl=X.X.X-1.1;
    :9. apt-mark hold kubelet kubectl;
    :10. systemctl daemon-reload && systemctl restart kubelet;
    :11. kubectl uncordon <node>;
  }
  rectangle "LEMBRE-SE" {
    :• Control plane PRIMEIRO, workers DEPOIS;
    :• kubeadm upgrade apply = primeiro master;
    :• kubeadm upgrade node = outros nodes;
    :• Sempre drain antes de atualizar kubelet;
    :• Sempre uncordon depois;
  }
}
@enduml
```

---

## Referências

- [Backup e Restore](backup-e-restore.md)
- [kubeadm](../tools/kubeadm.md)
- [kubelet](../cluster-components/kubelet.md)
- [OS Upgrade](os-upgrade.md)
- [High Availability](fundamentals/high-availability.md)
