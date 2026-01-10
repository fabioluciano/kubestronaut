# High Availability (HA) no Kubernetes

## Conceitos Fundamentais

### O que é Alta Disponibilidade?

Alta Disponibilidade (HA) é a capacidade de um sistema continuar operando mesmo quando componentes falham. No Kubernetes, isso envolve redundância em múltiplas camadas.

```plantuml,format=png
../assets/diagrams/general/high-availability-diagram-1.puml
```

---

## Arquitetura HA do Control Plane

### Topologia Stacked (etcd junto)

```plantuml,format=png
../assets/diagrams/general/high-availability-stacked-topology.puml
```

### Topologia External etcd

```plantuml,format=png
../assets/diagrams/general/high-availability-external-etcd-topology.puml
```

---

## etcd em Alta Disponibilidade

### Quorum e Tolerância a Falhas

```plantuml,format=png
../assets/diagrams/general/high-availability-quorum-do-etcd.puml
```

### Leader Election

```plantuml,format=png
../assets/diagrams/general/high-availability-raft-consensus-etcd.puml
```

### Comandos etcd

```bash
# Verificar status do cluster
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key \
  endpoint status --write-out=table

# Ver membros
etcdctl member list --write-out=table

# Verificar saúde
etcdctl endpoint health --write-out=table
```

---

## Control Plane HA

### kube-apiserver

```plantuml,format=png
../assets/diagrams/general/high-availability-api-server-é-stateless-pode-rodar-múltiplas-instân.puml
```

### kube-scheduler e controller-manager

```plantuml,format=png
../assets/diagrams/general/high-availability-scheduler-e-controller-manager-são-stateful-requer.puml
```

### Verificar Leader

```bash
# Ver quem é o leader do scheduler
kubectl get lease -n kube-system kube-scheduler -o yaml

# Ver quem é o leader do controller-manager
kubectl get lease -n kube-system kube-controller-manager -o yaml

# Exemplo de saída
# holderIdentity: master-1_xxxxx
```

---

## Configuração kubeadm HA

### Inicializar Primeiro Master

```yaml
../assets/high-availability/kubeadm-ha-config.yaml}}
```

```bash
# Criar arquivo de configuração
# kubeadm-config.yaml com o conteúdo acima

# Inicializar
sudo kubeadm init --config=kubeadm-config.yaml --upload-certs

# Guarde os comandos de join que aparecem!
```

### Adicionar Control Plane Nodes

```bash
# Comando gerado pelo init (exemplo)
sudo kubeadm join LOAD_BALANCER_IP:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane \
  --certificate-key <cert-key>
```

### Load Balancer (HAProxy)

```bash
# /etc/haproxy/haproxy.cfg
frontend kubernetes-frontend
    bind *:6443
    mode tcp
    option tcplog
    default_backend kubernetes-backend

backend kubernetes-backend
    mode tcp
    option tcp-check
    balance roundrobin
    server master-1 192.168.1.10:6443 check fall 3 rise 2
    server master-2 192.168.1.11:6443 check fall 3 rise 2
    server master-3 192.168.1.12:6443 check fall 3 rise 2
```

---

## HA de Aplicações

### Deployment com Réplicas

```yaml
../assets/high-availability/deployment-replicas.yaml}}
```

### Pod Anti-Affinity (Distribuir em Nodes)

```yaml
../assets/high-availability/deployment-anti-affinity.yaml}}
```

### Topology Spread Constraints

```yaml
../assets/high-availability/deployment-topology-spread.yaml}}
```

### PodDisruptionBudget

```yaml
../assets/high-availability/poddisruptionbudget.yaml}}
```

---

## Comportamento em Falhas

### Quando Master Falha (Single Master)

```plantuml,format=png
../assets/diagrams/general/high-availability-o-que-acontece-sem-master-single.puml
```

### Quando Worker Node Falha

```plantuml,format=png
../assets/diagrams/general/high-availability-o-que-acontece-quando-worker-falha.puml
```

---

## Troubleshooting HA

### Verificar Status do Cluster

```bash
# Status dos nodes
kubectl get nodes

# Status dos componentes
kubectl get componentstatuses  # deprecated mas ainda funciona
kubectl get --raw='/healthz?verbose'

# Verificar etcd
kubectl -n kube-system exec -it etcd-master-1 -- \
  etcdctl endpoint health --cluster

# Verificar leaders
kubectl get lease -n kube-system
```

### Problemas Comuns

```bash
# etcd não forma quorum
# - Verificar conectividade entre members
# - Verificar certificados
# - Ver logs: kubectl logs -n kube-system etcd-<node>

# API Server inacessível
# - Verificar Load Balancer
# - Verificar certificados
# - Verificar firewall (porta 6443)

# Scheduler/Controller não elegem leader
# - Verificar leases
# - Verificar logs
# - Reiniciar pods
```

---

## Dicas para o Exame CKA

```plantuml,format=png
../assets/diagrams/general/high-availability-dicas-cka-ha.puml
```

---

## Referências

- [kubeadm](tools/kubeadm.md)
- [etcd](cluster-components/etcd.md)
- [ETCDCTL](security/etcdctl.md)
- [Backup e Restore](maintenance/backup-e-restore.md)
- [Scheduling](workloads/scheduling.md)
- [Cluster Upgrade](maintenance/cluster-upgrade.md)
