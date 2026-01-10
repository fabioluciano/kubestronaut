# Arquitetura do Kubernetes

> **Certificacoes**: CKA (25%), KCNA (22%), CKS (10%) - Conhecimento essencial para todas as provas

## Conceitos Fundamentais

O Kubernetes e uma plataforma de orquestracao de containers de codigo aberto que automatiza a implantacao, escalonamento e gerenciamento de aplicacoes containerizadas. Sua arquitetura foi projetada para ser altamente escalavel, resiliente e extensivel.

### Por que entender a Arquitetura?

| Certificacao | Importancia |
|--------------|-------------|
| **CKA** | Essencial para troubleshooting e administracao do cluster |
| **KCNA** | Fundamento para entender conceitos cloud native |
| **CKS** | Necessario para entender superficie de ataque e hardening |
| **CKAD** | Util para entender como aplicacoes sao executadas |

---

## Visao Geral

### Arquitetura Geral do Kubernetes

O Kubernetes segue uma arquitetura master-worker (Control Plane + Worker Nodes) com comunicacao centralizada atraves do API Server.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-arquitetura-do-kubernetes.puml
```

### Principios de Design

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-principios-de-design-do-kubernetes.puml
```

---

## Control Plane

O Control Plane e responsavel pelas decisoes globais do cluster e pela deteccao e resposta a eventos.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-componentes-do-control-plane.puml
```

### kube-apiserver

O API Server e o frontend do Control Plane. Todas as operacoes passam por ele.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-kube-apiserver-fluxo-de-requisicao.puml
```

**Caracteristicas principais:**

| Aspecto | Descricao |
|---------|-----------|
| **Porta** | 6443 (HTTPS) |
| **Protocolo** | REST/JSON |
| **Stateless** | Pode ter multiplas replicas |
| **Autenticacao** | Certificados, tokens, OIDC |
| **Autorizacao** | RBAC, ABAC, Webhook |

**Flags importantes (CKA/CKS):**

```bash
# Ver configuracao do API Server
cat /etc/kubernetes/manifests/kube-apiserver.yaml

# Flags de seguranca importantes:
--anonymous-auth=false                    # Desabilita acesso anonimo
--enable-admission-plugins=...            # Admission controllers
--authorization-mode=RBAC,Node            # Modos de autorizacao
--tls-cert-file=/path/to/cert.pem         # Certificado TLS
--tls-private-key-file=/path/to/key.pem   # Chave privada
--client-ca-file=/path/to/ca.pem          # CA para clientes
--etcd-servers=https://127.0.0.1:2379     # Conexao com etcd
--audit-log-path=/var/log/audit.log       # Log de auditoria
```

### etcd

Banco de dados key-value que armazena todo o estado do cluster.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-etcd-armazenamento-de-estado.puml
```

**Caracteristicas:**

| Aspecto | Descricao |
|---------|-----------|
| **Porta** | 2379 (client), 2380 (peer) |
| **Consenso** | Algoritmo Raft |
| **Consistencia** | Forte (linearizavel) |
| **Dados** | Key-value hierarquico |

**Comandos etcdctl (CKA/CKS):**

```bash
# Variaveis necessarias
export ETCDCTL_API=3
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key

# Verificar saude do cluster
etcdctl endpoint health
etcdctl endpoint status --write-out=table

# Listar membros
etcdctl member list

# Backup do etcd (MUITO IMPORTANTE para CKA)
etcdctl snapshot save /tmp/etcd-backup.db

# Verificar backup
etcdctl snapshot status /tmp/etcd-backup.db --write-out=table

# Restore do etcd
etcdctl snapshot restore /tmp/etcd-backup.db \
  --data-dir=/var/lib/etcd-restored
```

### kube-scheduler

Responsavel por decidir em qual node cada pod vai executar.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-kube-scheduler-processo-de-scheduling.puml
```

**Fatores considerados no scheduling:**

| Fator | Descricao |
|-------|-----------|
| **Resources** | CPU e memoria requisitados vs disponiveis |
| **NodeSelector** | Labels obrigatorias do node |
| **NodeAffinity** | Preferencias de node |
| **PodAffinity/AntiAffinity** | Co-localizacao de pods |
| **Taints/Tolerations** | Restricoes de nodes |
| **Topology Spread** | Distribuicao entre zonas |

### kube-controller-manager

Executa os controllers que reconciliam o estado do cluster.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-kube-controller-manager.puml
```

**Controllers principais:**

| Controller | Responsabilidade |
|------------|------------------|
| **Node Controller** | Detectar e responder quando nodes ficam down |
| **Replication Controller** | Manter numero correto de pods |
| **Endpoints Controller** | Popular objeto Endpoints |
| **ServiceAccount Controller** | Criar SA default em namespaces |
| **Deployment Controller** | Gerenciar ReplicaSets e updates |
| **StatefulSet Controller** | Gerenciar StatefulSets |
| **DaemonSet Controller** | Garantir pod em cada node |
| **Job Controller** | Gerenciar Jobs |
| **CronJob Controller** | Criar Jobs por schedule |

---

## Worker Nodes

Os Worker Nodes sao as maquinas que executam os containers das aplicacoes.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-componentes-do-worker-node.puml
```

### kubelet

Agente que roda em cada node e garante que os containers estejam rodando.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-kubelet-funcoes.puml
```

**Responsabilidades do kubelet:**

| Funcao | Descricao |
|--------|-----------|
| **Pod Lifecycle** | Criar, atualizar, deletar pods |
| **Volume Management** | Montar/desmontar volumes |
| **Probes** | Executar health checks |
| **Resource Monitoring** | cAdvisor integrado |
| **Status Reporting** | Reportar status do node e pods |
| **Static Pods** | Gerenciar pods de manifests locais |

**Arquivos importantes:**

```bash
# Configuracao do kubelet
/var/lib/kubelet/config.yaml

# Diretorio de static pods
/etc/kubernetes/manifests/

# Logs do kubelet
journalctl -u kubelet -f
```

### kube-proxy

Implementa a abstraccao de Service no node.

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-kube-proxy-modos-de-operacao.puml
```

**Algoritmos de Load Balancing (IPVS):**

| Algoritmo | Descricao |
|-----------|-----------|
| rr | Round Robin |
| lc | Least Connections |
| dh | Destination Hashing |
| sh | Source Hashing |
| sed | Shortest Expected Delay |
| nq | Never Queue |

### Container Runtime

Interface para executar containers (CRI - Container Runtime Interface).

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-container-runtime-interface-cri.puml
```

---

## Fluxo de Criacao de Pod

### Diagrama de Sequencia

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-fluxo-de-criacao-de-pod.puml
```

### Detalhamento das Etapas

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-etapas-da-criacao-de-pod.puml
```

---

## Alta Disponibilidade

### Arquitetura HA do Control Plane

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-alta-disponibilidade-control-plane.puml
```

### Topologias de etcd

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-topologias-de-etcd.puml
```

### Recomendacoes de HA

| Componente | Minimo | Recomendado | Notas |
|------------|--------|-------------|-------|
| **Control Plane Nodes** | 3 | 3 ou 5 | Numeros impares para quorum |
| **etcd** | 3 | 3 ou 5 | Tolera (n-1)/2 falhas |
| **Worker Nodes** | 1 | 3+ | Depende da carga |
| **Load Balancer** | 1 | 2 (HA) | Para API Server |

---

## Comunicacao entre Componentes

### Diagrama de Comunicacao

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-comunicacao-entre-componentes.puml
```

### Portas Importantes (para firewall)

| Componente | Porta | Protocolo | Uso |
|------------|-------|-----------|-----|
| **API Server** | 6443 | TCP | API HTTPS |
| **etcd** | 2379 | TCP | Client requests |
| **etcd** | 2380 | TCP | Peer communication |
| **kubelet** | 10250 | TCP | API |
| **kube-scheduler** | 10259 | TCP | Secure port |
| **controller-manager** | 10257 | TCP | Secure port |
| **kube-proxy** | 10256 | TCP | Health check |
| **NodePort Services** | 30000-32767 | TCP | Servicos externos |

---

## Dicas para o Exame

### CKA - Pontos Importantes

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-dicas-cka-arquitetura.puml
```

### KCNA - Conceitos Chave

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-kcna-conceitos-arquitetura.puml
```

### Comandos Uteis para Troubleshooting

```bash
# Ver componentes do control plane
kubectl get pods -n kube-system

# Ver status dos nodes
kubectl get nodes -o wide
kubectl describe node <node-name>

# Ver logs dos componentes (kubeadm)
kubectl logs -n kube-system kube-apiserver-<node>
kubectl logs -n kube-system kube-scheduler-<node>
kubectl logs -n kube-system kube-controller-manager-<node>
kubectl logs -n kube-system etcd-<node>

# Logs do kubelet
journalctl -u kubelet -f

# Verificar certificados
kubeadm certs check-expiration
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout

# Verificar conectividade
kubectl get --raw='/healthz'
kubectl get --raw='/readyz'
curl -k https://localhost:6443/healthz

# Ver eventos do cluster
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -A --sort-by='.lastTimestamp'
```

---

## Referencias

### Links Internos

- [Componentes dos Nos](cluster-components/node-components.md) - Detalhes de cada componente
- [kube-apiserver](cluster-components/kube-apiserver.md)
- [etcd](cluster-components/etcd.md)
- [kube-scheduler](cluster-components/kube-scheduler.md)
- [kube-controller-manager](cluster-components/kube-controller-manager.md)
- [kubelet](cluster-components/kubelet.md)
- [kube-proxy](cluster-components/kube-proxy.md)
- [Alta Disponibilidade](fundamentals/high-availability.md)
- [Backup e Restore](maintenance/backup-e-restore.md)

### Documentacao Oficial

- [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- [Cluster Architecture](https://kubernetes.io/docs/concepts/architecture/)
- [Communication between Nodes](https://kubernetes.io/docs/concepts/architecture/control-plane-node-communication/)
- [etcd](https://etcd.io/docs/)
- [High Availability](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)

---

## Best Practices

### Arquitetura de Producao

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-best-practices-arquitetura.puml
```

### Recomendacoes por Componente

| Componente | Best Practice |
|------------|---------------|
| **API Server** | Multiplas replicas, rate limiting, audit logs |
| **etcd** | 3 ou 5 nodes, SSD, backups frequentes |
| **Scheduler** | Configurar priorities corretamente |
| **Controller Manager** | Monitorar logs para erros de reconciliacao |
| **kubelet** | Reservar recursos para sistema |
| **kube-proxy** | Considerar IPVS para clusters grandes |

### Dimensionamento

| Tamanho do Cluster | Control Plane | Workers | etcd |
|-------------------|---------------|---------|------|
| **Pequeno** (<50 pods) | 1 | 1-3 | 1 |
| **Medio** (50-500 pods) | 3 | 3-10 | 3 |
| **Grande** (500-5000 pods) | 3-5 | 10-100 | 5 |
| **Muito Grande** (5000+ pods) | 5+ | 100+ | 5-7 |

---

## Troubleshooting Arquitetural

### Problemas Comuns

```plantuml,format=png
../assets/diagrams/architecture/arquitetura-troubleshooting-problemas-comuns.puml
```

### Comandos de Diagnostico

```bash
# API Server
kubectl get --raw='/healthz?verbose'
curl -k https://localhost:6443/healthz

# etcd
etcdctl endpoint health --cluster
etcdctl endpoint status --write-out=table

# Scheduler e Controller Manager
kubectl get lease -n kube-system
kubectl logs -n kube-system kube-scheduler-<node>

# kubelet
systemctl status kubelet
journalctl -u kubelet -f --since "10 minutes ago"

# Rede
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl run test --image=busybox --rm -it -- wget -qO- kubernetes
```

---

> **Resumo**: O Kubernetes tem arquitetura Control Plane + Worker Nodes. O Control Plane (API Server, etcd, Scheduler, Controller Manager) toma decisoes globais. Os Worker Nodes (kubelet, kube-proxy, container runtime) executam containers. Toda comunicacao passa pelo API Server. O etcd armazena todo estado (fazer backup!). Para HA, use 3+ control plane nodes com etcd em quorum.
