# Hardening do Cluster

> **Certificacoes**: CKS (Cluster Hardening - 15%), CKA (Cluster Architecture)

## Conceitos Fundamentais

Hardening e o processo de reduzir a superficie de ataque de um sistema, eliminando vulnerabilidades e configurando componentes de forma segura. No Kubernetes, isso envolve proteger todos os componentes do cluster: desde a infraestrutura de rede ate os containers em execucao.

```admonish info title="Principio do Least Privilege"
Conceda apenas as permissoes minimas necessarias para que um componente, usuario ou workload funcione. Este principio e a base de toda estrategia de hardening.
```

```plantuml,format=png
!include ../assets/diagrams/security/hardening-camadas-de-hardening-no-kubernetes-1.puml
```

## Checklist Completo de Hardening

### Sistema Operacional

| Item | Acao | Prioridade | CIS Benchmark |
|------|------|------------|---------------|
| Pacotes desnecessarios | Remover | Alta | 1.1.1 |
| Servicos desnecessarios | Desabilitar | Alta | 1.1.2 |
| Atualizacoes de seguranca | Aplicar regularmente | Critica | 1.1.3 |
| Firewall | Configurar regras | Alta | 1.1.4 |
| SELinux/AppArmor | Habilitar | Media | 1.1.5 |
| Kernel modules | Restringir | Media | 1.1.6 |
| Filesystem permissions | Verificar | Alta | 1.1.7 |
| Usuarios/Grupos | Auditoria | Media | 1.1.8 |
| SSH hardening | Configurar | Alta | 1.1.9 |
| Logs centralizados | Configurar | Alta | 1.1.10 |

### Control Plane

| Item | Acao | Prioridade | CIS Benchmark |
|------|------|------------|---------------|
| API Server anonymous auth | Desabilitar | Critica | 1.2.1 |
| RBAC | Habilitar | Critica | 1.2.2 |
| Audit logging | Habilitar | Alta | 1.2.22 |
| Encryption at rest | Configurar | Alta | 1.2.31 |
| TLS | Versao minima 1.2 | Alta | 1.2.30 |
| Profiling | Desabilitar | Media | 1.2.21 |
| Admission Controllers | Configurar | Alta | 1.2.10-16 |
| Service Account tokens | Rotacionar | Media | 1.2.24 |
| etcd encryption | Habilitar | Critica | 1.2.31 |
| API rate limiting | Configurar | Media | 1.2.9 |

### Worker Nodes

| Item | Acao | Prioridade | CIS Benchmark |
|------|------|------------|---------------|
| Kubelet anonymous auth | Desabilitar | Critica | 4.2.1 |
| Read-only port | Desabilitar (porta 10255) | Alta | 4.2.4 |
| Protect kernel defaults | Habilitar | Media | 4.2.6 |
| Certificate rotation | Habilitar | Alta | 4.2.11 |
| Streaming timeout | Configurar | Media | 4.2.5 |
| Event record QPS | Limitar | Baixa | 4.2.9 |
| Make IPTables | Habilitar | Alta | 4.2.7 |
| Hostname override | Evitar | Baixa | 4.2.8 |
| Node authorization | Habilitar | Alta | 4.2.2 |

### etcd

| Item | Acao | Prioridade | CIS Benchmark |
|------|------|------------|---------------|
| Client cert auth | Habilitar | Critica | 2.1 |
| Auto TLS | Desabilitar | Alta | 2.2 |
| Peer client cert auth | Habilitar | Critica | 2.3 |
| Peer auto TLS | Desabilitar | Alta | 2.4 |
| Unique CA | Usar | Alta | 2.5 |
| Access restricted | Apenas control plane | Critica | 2.6 |
| File permissions | 600/700 | Alta | 2.7 |

## Hardening do Sistema Operacional

### Remover Pacotes Desnecessarios

```bash
# Listar pacotes instalados
dpkg --list   # Debian/Ubuntu
rpm -qa       # RHEL/CentOS

# Remover pacotes desnecessarios
apt remove <package>   # Debian/Ubuntu
yum remove <package>   # RHEL/CentOS

# Pacotes comuns para remover em nodes K8s
apt remove --purge telnet ftp rsh-client rsh-redone-client
apt remove --purge build-essential gcc make
apt remove --purge wireless-tools wpasupplicant

# Limpar pacotes orfaos
apt autoremove --purge
```

### Desabilitar Servicos Desnecessarios

```bash
# Listar servicos ativos
systemctl list-units --type=service --state=running

# Servicos comuns para desabilitar em nodes K8s
systemctl stop cups && systemctl disable cups
systemctl stop avahi-daemon && systemctl disable avahi-daemon
systemctl stop bluetooth && systemctl disable bluetooth
systemctl stop ModemManager && systemctl disable ModemManager
systemctl stop NetworkManager-wait-online && systemctl disable NetworkManager-wait-online

# Desabilitar servicos de impressao
systemctl mask cups.service cups-browsed.service

# Verificar servicos em escuta
systemctl list-sockets --state=listening
```

### Hardening do Kernel

```bash
# /etc/sysctl.d/99-kubernetes-hardening.conf

# Desabilitar IP forwarding apenas quando necessario
# (Kubernetes PRECISA de IP forwarding, nao desabilitar!)
# net.ipv4.ip_forward = 1

# Desabilitar source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Ignorar ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Nao enviar ICMP redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Protecao contra IP spoofing
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignorar broadcast ICMP
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Protecao contra SYN flood
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2

# Desabilitar IPv6 se nao usado
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1

# Restringir dmesg
kernel.dmesg_restrict = 1

# Restringir kernel pointers
kernel.kptr_restrict = 2

# Restringir perf events
kernel.perf_event_paranoid = 3

# Aplicar mudancas
# sysctl -p /etc/sysctl.d/99-kubernetes-hardening.conf
```

### Desabilitar Kernel Modules Perigosos

```bash
# /etc/modprobe.d/kubernetes-hardening.conf

# Desabilitar filesystems nao necessarios
install cramfs /bin/true
install freevxfs /bin/true
install jffs2 /bin/true
install hfs /bin/true
install hfsplus /bin/true
install squashfs /bin/true
install udf /bin/true
install vfat /bin/true

# Desabilitar protocolos de rede nao usados
install dccp /bin/true
install sctp /bin/true
install rds /bin/true
install tipc /bin/true

# Desabilitar USB storage (se nao necessario)
install usb-storage /bin/true

# Desabilitar Bluetooth
install bluetooth /bin/true
install btusb /bin/true
```

### Verificar Portas Abertas

```bash
# Listar portas em escuta
sudo netstat -tulpn | grep LISTEN

# Ou usando ss (mais moderno)
sudo ss -tulpn | grep LISTEN

# Verificar processos por porta
sudo lsof -i :6443

# Verificar com nmap (de outra maquina)
nmap -sT -p 1-65535 <node-ip>
```

### Portas do Kubernetes

| Componente | Porta | Protocolo | Deve estar exposta? |
|------------|-------|-----------|---------------------|
| API Server | 6443 | TCP | Sim (clientes autorizados) |
| etcd | 2379-2380 | TCP | **NAO** (apenas control plane) |
| Kubelet | 10250 | TCP | Sim (API Server) |
| Kubelet (read-only) | 10255 | TCP | **NAO** (desabilitar) |
| Kube Scheduler | 10259 | TCP | Nao (apenas localhost) |
| Kube Controller | 10257 | TCP | Nao (apenas localhost) |
| NodePort Services | 30000-32767 | TCP | Depende |
| Flannel VXLAN | 8472 | UDP | Entre nodes |
| Calico BGP | 179 | TCP | Entre nodes |
| Calico VXLAN | 4789 | UDP | Entre nodes |
| CoreDNS | 53 | TCP/UDP | Interno cluster |

```plantuml,format=png
!include ../assets/diagrams/security/hardening-portas-do-kubernetes-visao-geral-1.puml
```

## Hardening SSH

### Configuracao Segura

```bash
# /etc/ssh/sshd_config

# Desabilitar login root
PermitRootLogin no

# Desabilitar autenticacao por senha
PasswordAuthentication no

# Usar apenas chaves SSH
PubkeyAuthentication yes

# Limitar usuarios que podem fazer SSH
AllowUsers admin deploy kubernetes

# Limitar grupos
AllowGroups ssh-users wheel

# Desabilitar protocolo antigo
Protocol 2

# Timeout de sessao
ClientAliveInterval 300
ClientAliveCountMax 2

# Desabilitar X11 forwarding
X11Forwarding no

# Desabilitar TCP forwarding (se nao necessario)
AllowTcpForwarding no

# Desabilitar agent forwarding
AllowAgentForwarding no

# Usar somente algoritmos fortes
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org

# Banner de aviso
Banner /etc/issue.net

# Log level
LogLevel VERBOSE

# Max auth tries
MaxAuthTries 3

# Max sessions
MaxSessions 2
```

```bash
# Aplicar mudancas
sudo systemctl restart sshd

# Verificar configuracao
sudo sshd -t

# Testar login antes de fechar sessao atual!
ssh -v user@node
```

## Hardening do Control Plane

### Hardening do API Server

```yaml
{{#include ../assets/security/hardening/kube-apiserver-hardening.yaml}}
```

### Flags de Seguranca Completas do API Server

| Flag | Valor Recomendado | Descricao | CIS |
|------|-------------------|-----------|-----|
| `--anonymous-auth` | `false` | Desabilita acesso anonimo | 1.2.1 |
| `--authorization-mode` | `Node,RBAC` | Habilita RBAC e Node authz | 1.2.7-8 |
| `--enable-admission-plugins` | Ver lista | Admission controllers | 1.2.10-16 |
| `--profiling` | `false` | Desabilita profiling | 1.2.21 |
| `--audit-log-path` | `/var/log/audit.log` | Habilita auditoria | 1.2.22 |
| `--audit-log-maxage` | `30` | Retencao de logs | 1.2.23 |
| `--audit-log-maxbackup` | `10` | Backup de logs | 1.2.24 |
| `--audit-log-maxsize` | `100` | Tamanho max log (MB) | 1.2.25 |
| `--tls-min-version` | `VersionTLS12` | TLS minimo 1.2 | 1.2.30 |
| `--tls-cipher-suites` | Ver lista | Ciphers seguros | 1.2.31 |
| `--insecure-port` | `0` | Desabilita porta insegura | Removido |
| `--kubelet-certificate-authority` | CA path | Verifica cert kubelet | 1.2.5 |
| `--kubelet-client-certificate` | Cert path | Cert para kubelet | 1.2.4 |
| `--kubelet-client-key` | Key path | Key para kubelet | 1.2.4 |
| `--service-account-lookup` | `true` | Valida SA tokens | 1.2.26 |
| `--encryption-provider-config` | Config path | Encryption at rest | 1.2.33 |

### Configuracao Completa do API Server

```yaml
{{#include ../assets/security/hardening/kube-apiserver-complete.yaml}}
```

### Hardening do Controller Manager

```yaml
{{#include ../assets/security/hardening/kube-controller-manager-hardening.yaml}}
```

### Hardening do Scheduler

```yaml
{{#include ../assets/security/hardening/kube-scheduler-hardening.yaml}}
```

### Hardening do etcd

```yaml
{{#include ../assets/security/hardening/etcd-hardening.yaml}}
```

## Hardening dos Worker Nodes

### Configuracao do Kubelet

```yaml
{{#include ../assets/security/hardening/kubelet-config.yaml}}
```

### Configuracao Completa do Kubelet

```yaml
{{#include ../assets/security/hardening/kubelet-config-complete.yaml}}
```

### Verificar Configuracao do Kubelet

```bash
# Ver configuracao atual via API
kubectl get --raw /api/v1/nodes/<node-name>/proxy/configz | jq

# Ou no node
cat /var/lib/kubelet/config.yaml

# Ver flags do processo
ps aux | grep kubelet

# Verificar anonymous auth
curl -sk https://localhost:10250/pods
# Deve retornar 401 Unauthorized

# Verificar read-only port (deve falhar)
curl -s http://localhost:10255/pods
# Connection refused = correto
```

### Flags Importantes do Kubelet

| Flag | Valor Recomendado | Descricao | CIS |
|------|-------------------|-----------|-----|
| `--anonymous-auth` | `false` | Desabilita acesso anonimo | 4.2.1 |
| `--authorization-mode` | `Webhook` | Authz via API Server | 4.2.2 |
| `--client-ca-file` | CA path | Verifica certs clients | 4.2.3 |
| `--read-only-port` | `0` | Desabilita porta 10255 | 4.2.4 |
| `--streaming-connection-idle-timeout` | `5m` | Timeout de streaming | 4.2.5 |
| `--protect-kernel-defaults` | `true` | Protege sysctl | 4.2.6 |
| `--make-iptables-util-chains` | `true` | Cria chains iptables | 4.2.7 |
| `--event-qps` | `0` | Limita eventos | 4.2.9 |
| `--rotate-certificates` | `true` | Rotacao de certs | 4.2.11 |
| `--tls-cipher-suites` | Ver lista | Ciphers seguros | 4.2.13 |

## Hardening de Pods e Containers

### Pod Seguro (Hardened)

```yaml
{{#include ../assets/security/hardening/hardened-pod.yaml}}
```

### Pod com Todas Restricoes de Seguranca

```yaml
{{#include ../assets/security/hardening/pod-maximum-security.yaml}}
```

```plantuml,format=png
!include ../assets/diagrams/security/hardening-checklist-de-seguranca-de-pod-1.puml
```

### Campos de Seguranca do Pod

| Campo | Valor Seguro | Descricao |
|-------|--------------|-----------|
| `securityContext.runAsNonRoot` | `true` | Impede execucao como root |
| `securityContext.runAsUser` | `>= 10000` | UID especifico non-root |
| `securityContext.runAsGroup` | `>= 10000` | GID especifico |
| `securityContext.fsGroup` | `>= 10000` | GID para volumes |
| `securityContext.readOnlyRootFilesystem` | `true` | Filesystem read-only |
| `securityContext.allowPrivilegeEscalation` | `false` | Impede escalacao |
| `securityContext.privileged` | `false` | Impede modo privilegiado |
| `securityContext.capabilities.drop` | `["ALL"]` | Remove todas capabilities |
| `securityContext.seccompProfile.type` | `RuntimeDefault` | Profile seccomp |
| `hostNetwork` | `false` | Impede uso da rede do host |
| `hostPID` | `false` | Impede acesso a PIDs do host |
| `hostIPC` | `false` | Impede acesso a IPC do host |
| `automountServiceAccountToken` | `false` | Nao monta token SA |

## Network Policies

### Default Deny All

```yaml
{{#include ../assets/security/hardening/networkpolicy-default-deny.yaml}}
```

### NetworkPolicy Default Deny - Namespace Completo

```yaml
{{#include ../assets/security/hardening/networkpolicy-default-deny-all.yaml}}
```

```admonish warning title="Importante"
Aplique uma policy de default deny em TODOS os namespaces de producao. Depois, crie policies especificas para permitir apenas o trafego necessario.
```

### NetworkPolicy Allow Especifica

```yaml
{{#include ../assets/security/hardening/networkpolicy-allow-specific.yaml}}
```

## Encryption at Rest

### Configurar Criptografia de Secrets

```yaml
{{#include ../assets/security/hardening/encryption-config.yaml}}
```

### Configuracao Completa de Encryption

```yaml
{{#include ../assets/security/hardening/encryption-config-complete.yaml}}
```

### Gerar Chave de Criptografia

```bash
# Gerar chave de 32 bytes
head -c 32 /dev/urandom | base64

# Exemplo de output:
# Ywx5VnBQSjdMcTJpSzZxM3U4dTNGSDZpMnF5N2hJRkE=

# Criar diretorio
mkdir -p /etc/kubernetes/enc

# Criar arquivo de configuracao
cat > /etc/kubernetes/enc/encryption-config.yaml << 'EOF'
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: <sua-chave-base64>
      - identity: {}
EOF

# Ajustar permissoes
chmod 600 /etc/kubernetes/enc/encryption-config.yaml
```

### Ativar no API Server

```yaml
{{#include ../assets/security/hardening-example-1.yaml}}
```

### Verificar Criptografia

```bash
# Verificar se secrets estao criptografados
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/mysecret | hexdump -C

# Se criptografado, vera "k8s:enc:aescbc:v1:key1" no inicio
# Se nao criptografado, vera o conteudo em texto plano

# Re-criptografar secrets existentes
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
```

## Audit Logging

### Policy de Auditoria

```yaml
{{#include ../assets/security/hardening/audit-policy.yaml}}
```

### Policy de Auditoria Completa

```yaml
{{#include ../assets/security/hardening/audit-policy-complete.yaml}}
```

### Habilitar no API Server

```yaml
{{#include ../assets/security/hardening-example-2.yaml}}
```

### Configuracao Completa de Audit

```yaml
{{#include ../assets/security/hardening/kube-apiserver-audit.yaml}}
```

### Analisar Logs de Auditoria

```bash
# Ver ultimos eventos
tail -100 /var/log/kubernetes/audit.log | jq

# Filtrar por usuario
cat /var/log/kubernetes/audit.log | jq 'select(.user.username=="admin")'

# Filtrar por verbo
cat /var/log/kubernetes/audit.log | jq 'select(.verb=="delete")'

# Filtrar por recurso
cat /var/log/kubernetes/audit.log | jq 'select(.objectRef.resource=="secrets")'

# Eventos de falha de autorizacao
cat /var/log/kubernetes/audit.log | jq 'select(.responseStatus.code >= 400)'
```

## Admission Controllers

### Controllers Recomendados

```yaml
{{#include ../assets/security/hardening-example-3.yaml}}
```

### Descricao dos Admission Controllers

| Controller | Funcao | Recomendado |
|------------|--------|-------------|
| `NodeRestriction` | Limita o que nodes podem modificar | **Sim** |
| `PodSecurity` | Enforces Pod Security Standards | **Sim** |
| `ServiceAccount` | Auto-monta tokens de SA | Sim |
| `LimitRanger` | Aplica limites de recursos | Sim |
| `ResourceQuota` | Enforces quotas de namespace | Sim |
| `DefaultStorageClass` | Define StorageClass padrao | Sim |
| `MutatingAdmissionWebhook` | Webhooks de mutacao | Sim |
| `ValidatingAdmissionWebhook` | Webhooks de validacao | Sim |
| `AlwaysPullImages` | Forca pull de imagens | Opcional |
| `DenyServiceExternalIPs` | Bloqueia external IPs | Producao |

### Validating Webhook Configuration

```yaml
{{#include ../assets/security/hardening/validating-webhook-config.yaml}}
```

### Mutating Webhook Configuration

```yaml
{{#include ../assets/security/hardening/mutating-webhook-config.yaml}}
```

## CIS Benchmarks

O CIS (Center for Internet Security) publica benchmarks de seguranca para Kubernetes.

```plantuml,format=png
!include ../assets/diagrams/security/hardening-cis-kubernetes-benchmark-categorias-1.puml
```

### Ferramentas de Verificacao

#### kube-bench

```bash
# Instalacao
curl -L https://github.com/aquasecurity/kube-bench/releases/download/v0.7.0/kube-bench_0.7.0_linux_amd64.tar.gz | tar xz

# Executar no control plane
./kube-bench run --targets master

# Executar nos workers
./kube-bench run --targets node

# Executar todos os testes
./kube-bench run

# Output JSON
./kube-bench run --json > results.json

# Executar como Pod no cluster
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs -l app=kube-bench
```

#### Executar kube-bench como Job

```yaml
{{#include ../assets/security/hardening/kube-bench-job.yaml}}
```

### Categorias CIS

| ID | Categoria | Escopo | Quantidade |
|----|-----------|--------|------------|
| 1 | Control Plane Components | API Server, Scheduler, Controller Manager | ~100 checks |
| 2 | etcd | Configuracao do etcd | ~10 checks |
| 3 | Control Plane Configuration | Autenticacao, Logging | ~10 checks |
| 4 | Worker Nodes | Kubelet, arquivos de config | ~30 checks |
| 5 | Policies | Network, Pod Security, RBAC | ~40 checks |

### Exemplo de Output kube-bench

```
[INFO] 1 Control Plane Security Configuration
[INFO] 1.1 Control Plane Node Configuration Files
[PASS] 1.1.1 Ensure that the API server pod specification file permissions are set to 644 or more restrictive
[PASS] 1.1.2 Ensure that the API server pod specification file ownership is set to root:root
[FAIL] 1.1.3 Ensure that the controller manager pod specification file permissions are set to 644 or more restrictive
[WARN] 1.1.4 Ensure that the scheduler pod specification file permissions are set to 644 or more restrictive
...

[INFO] 1.2 API Server
[PASS] 1.2.1 Ensure that the --anonymous-auth argument is set to false
[FAIL] 1.2.2 Ensure that the --token-auth-file parameter is not set
...

== Summary ==
45 checks PASS
10 checks FAIL
5 checks WARN
0 checks INFO
```

### Remediar Falhas Comuns

```bash
# 1.1.3 - Permissoes de arquivo do controller manager
chmod 644 /etc/kubernetes/manifests/kube-controller-manager.yaml
chown root:root /etc/kubernetes/manifests/kube-controller-manager.yaml

# 1.2.1 - Anonymous auth
# Adicionar ao kube-apiserver.yaml:
# --anonymous-auth=false

# 1.2.2 - Token auth file (remover se existir)
# Remover flag --token-auth-file do API Server

# 4.2.4 - Read-only port do kubelet
# Adicionar ao config.yaml do kubelet:
# readOnlyPort: 0

# 4.2.6 - Protect kernel defaults
# Adicionar ao config.yaml do kubelet:
# protectKernelDefaults: true
```

## Comandos Uteis de Verificacao

```bash
# === API Server ===
# Verificar anonymous auth do API Server
kubectl auth can-i --list --as system:anonymous

# Verificar RBAC habilitado
kubectl api-versions | grep rbac

# Ver admission plugins habilitados (dentro do container)
kubectl exec -n kube-system kube-apiserver-<node> -- \
  kube-apiserver --help 2>&1 | grep enable-admission-plugins

# Verificar TLS do API Server
openssl s_client -connect <api-server>:6443 </dev/null 2>/dev/null | \
  openssl x509 -text -noout | grep -A2 "Subject:"

# Verificar versao TLS minima
openssl s_client -connect <api-server>:6443 -tls1_1 </dev/null
# Deve falhar se --tls-min-version=VersionTLS12

# === Kubelet ===
# Verificar configuracao do kubelet
kubectl get --raw /api/v1/nodes/<node>/proxy/configz | jq

# Testar anonymous auth do kubelet
curl -sk https://<node-ip>:10250/pods
# Deve retornar 401

# Testar read-only port (deve falhar)
curl -s http://<node-ip>:10255/pods
# Connection refused = bom

# === NetworkPolicy ===
# Testar conectividade
kubectl run test --image=busybox --rm -it --restart=Never -- \
  wget -qO- --timeout=2 http://service.namespace.svc.cluster.local

# === Secrets ===
# Verificar se secrets estao criptografados
ETCDCTL_API=3 etcdctl get /registry/secrets/default/mysecret \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key | hexdump -C | head

# === Audit ===
# Ver logs de auditoria
tail -f /var/log/kubernetes/audit.log | jq '.verb + " " + .objectRef.resource'

# === Geral ===
# Verificar permissoes de arquivos criticos
ls -la /etc/kubernetes/manifests/
ls -la /etc/kubernetes/pki/
ls -la /var/lib/kubelet/config.yaml
```

## Troubleshooting

### API Server Nao Inicia

```admonish failure title="Erro: Unable to start kube-apiserver"
**Causas comuns**:
1. Certificados invalidos ou expirados
2. Flags de configuracao incorretas
3. etcd inacessivel
4. Permissoes de arquivo incorretas

**Solucao**:
1. Verificar logs: `journalctl -u kubelet -f`
2. Verificar manifesto: `/etc/kubernetes/manifests/kube-apiserver.yaml`
3. Validar certificados: `openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -text`
4. Verificar etcd: `ETCDCTL_API=3 etcdctl endpoint health`
```

### Kubelet Anonymous Auth

```bash
# Verificar se anonymous auth esta habilitado
curl -sk https://localhost:10250/pods
# Se retornar dados, anonymous auth esta habilitado (INSEGURO)

# Deve retornar 401 Unauthorized
```

```admonish failure title="Kubelet retornando dados sem autenticacao"
**Solucao**:
1. Editar `/var/lib/kubelet/config.yaml`
2. Adicionar:
   ```yaml
{{#include ../assets/security/hardening-example-4.yaml}}
```
3. Reiniciar kubelet: `systemctl restart kubelet`
```

### NetworkPolicy Nao Funciona

```admonish failure title="NetworkPolicy sem efeito"
**Causa**: CNI nao suporta NetworkPolicy

**Solucao**:
1. Verificar se CNI suporta NetworkPolicy (Calico, Cilium, Weave)
2. Flannel padrao NAO suporta NetworkPolicy
3. Migrar para CNI compativel
```

### Secrets Nao Criptografados

```bash
# Verificar se encryption esta ativo
kubectl get secrets -A -o json | kubectl replace -f -

# Se erro, verificar:
# 1. Flag --encryption-provider-config no API Server
# 2. Arquivo de configuracao existe e tem permissoes corretas
# 3. Chave e valida (32 bytes base64)
```

### Audit Logs Nao Gerados

```admonish failure title="Audit logs vazios ou inexistentes"
**Verificar**:
1. Flags no API Server:
   - `--audit-log-path=/var/log/kubernetes/audit.log`
   - `--audit-policy-file=/etc/kubernetes/audit-policy.yaml`
2. Diretorio existe: `mkdir -p /var/log/kubernetes`
3. Policy file existe e e valido
4. Volume montado corretamente no Pod
```

## Dicas para o Exame CKS

```admonish tip title="Dicas CKS"
1. **kube-bench**: Saiba interpretar e corrigir falhas - muito cobrado!
2. **API Server flags**: Memorize flags de seguranca principais
3. **Kubelet config**: Saiba onde fica (`/var/lib/kubelet/config.yaml`)
4. **NetworkPolicy**: Pratique criar policies de deny-all
5. **Admission Controllers**: Saiba habilitar NodeRestriction
6. **Audit logs**: Saiba configurar auditoria basica
7. **Encryption at rest**: Saiba configurar e verificar
8. **Permissoes de arquivo**: Saiba os valores corretos (644, 600)
9. **Certificados**: Saiba onde ficam e como verificar
10. **systemctl**: Saiba reiniciar servicos apos mudancas
```

```admonish warning title="Locais Importantes no Exame"
- `/etc/kubernetes/manifests/` - Static pods do control plane
- `/etc/kubernetes/pki/` - Certificados
- `/var/lib/kubelet/config.yaml` - Config do kubelet
- `/etc/kubernetes/admin.conf` - kubeconfig do admin
- `/var/log/kubernetes/` - Logs (audit, etc)
```

## Arquitetura de Seguranca - Defense in Depth

```plantuml,format=png
!include ../assets/diagrams/security/hardening-defense-in-depth-kubernetes-1.puml
```

## Best Practices

### Prioridade Alta (Fazer Imediatamente)

1. **Desabilitar anonymous auth** - API Server e Kubelet
2. **Habilitar RBAC** - Nao use ABAC
3. **Configurar NetworkPolicies** - Default deny em producao
4. **Habilitar Audit Logging** - Registre todas as acoes
5. **Criptografar secrets at rest** - Obrigatorio em producao
6. **Desabilitar read-only port** - Kubelet porta 10255
7. **Usar TLS 1.2+** - Em todas as comunicacoes
8. **Executar como non-root** - Todos os pods
9. **Limitar recursos** - CPU e memoria em todos os pods
10. **Usar imagens minimas** - Distroless ou scratch

### Prioridade Media (Planejar)

1. **Implementar Pod Security Standards** - Restricted level
2. **Configurar admission controllers** - NodeRestriction obrigatorio
3. **Habilitar certificate rotation** - Kubelet e API Server
4. **Restringir acesso ao etcd** - Apenas control plane
5. **Remover pacotes desnecessarios** - Nos nodes
6. **Desabilitar servicos desnecessarios** - Nos nodes
7. **Hardening SSH** - Desabilitar senha, usar chaves
8. **Configurar sysctl** - Kernel hardening
9. **Implementar image scanning** - No CI/CD
10. **Monitorar logs de auditoria** - Alertas automaticos

### Prioridade Baixa (Melhoria Continua)

1. **Implementar service mesh** - mTLS automatico
2. **Usar runtime classes** - gVisor/Kata para workloads nao confiaveis
3. **Configurar SELinux/AppArmor** - Profiles customizados
4. **Implementar OPA/Gatekeeper** - Policies avancadas
5. **Usar Vault** - Para secrets management
6. **Implementar SIEM** - Agregacao de logs
7. **Fazer pentests** - Regularmente
8. **Disaster recovery** - Testes regulares
9. **Compliance** - CIS, SOC2, PCI-DSS
10. **Security training** - Para toda equipe

## Recursos Adicionais

- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NSA Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
- [kube-bench](https://github.com/aquasecurity/kube-bench)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/security-best-practices/)
- [OWASP Kubernetes Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)
