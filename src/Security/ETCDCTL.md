# ETCDCTL

> **Certificacoes**: CKA (Cluster Architecture - 25%), CKS (Cluster Setup - 10%)

O `etcdctl` e a ferramenta de linha de comando para interagir com o etcd, o banco de dados chave-valor distribuido que armazena todo o estado do cluster Kubernetes.

```plantuml,format=png
!include ../assets/diagrams/security/etcdctl-etcdctl-ferramenta-de-gerenciamento-do-etcd-1.puml
```

---

## Conceitos Fundamentais

### O que e o etcdctl?

O `etcdctl` e o cliente CLI oficial do etcd. No contexto Kubernetes, e usado principalmente para:

- **Backup e Restore**: Criar e restaurar snapshots do cluster
- **Health Check**: Verificar saude do cluster etcd
- **Troubleshooting**: Diagnosticar problemas de conectividade e performance
- **Gerenciamento**: Adicionar/remover membros do cluster etcd

### Versoes da API

```plantuml,format=png
!include ../assets/diagrams/security/etcdctl-diagram-2-1.puml
```

---

## Variaveis de Ambiente

### Configuracao Essencial

```bash
# OBRIGATORIO: Definir versao da API
export ETCDCTL_API=3

# Verificar versao do etcdctl
etcdctl version
```

### Variaveis de Certificados

```bash
# Certificados para conexao TLS com etcd
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key

# Endpoint do etcd
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
```

### Script de Configuracao Completa

```bash
#!/bin/bash
# setup-etcdctl-env.sh

export ETCDCTL_API=3
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379

echo "Variaveis de ambiente configuradas!"
echo "Testando conexao..."
etcdctl endpoint health
```

### Encontrar Certificados no Cluster

```bash
# Em clusters kubeadm, verificar manifesto do etcd
cat /etc/kubernetes/manifests/etcd.yaml | grep -E "cert-file|key-file|trusted-ca-file"

# Saida tipica:
# --cert-file=/etc/kubernetes/pki/etcd/server.crt
# --key-file=/etc/kubernetes/pki/etcd/server.key
# --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
```

---

## Health Check do Cluster

### Verificar Saude dos Endpoints

```bash
# Com variaveis de ambiente configuradas
etcdctl endpoint health

# Com certificados inline
etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Saida esperada:
# https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 1.234ms
```

### Status Detalhado dos Endpoints

```bash
# Ver status em formato tabela
etcdctl endpoint status --write-out=table

# Saida exemplo:
# +---------------------------+------------------+---------+---------+-----------+...
# |         ENDPOINT          |        ID        | VERSION | DB SIZE | IS LEADER |...
# +---------------------------+------------------+---------+---------+-----------+...
# | https://127.0.0.1:2379    | 8e9e05c52164694d |  3.5.9  |  4.5 MB |   true    |...
# +---------------------------+------------------+---------+---------+-----------+
```

### Listar Membros do Cluster

```bash
# Listar todos os membros
etcdctl member list

# Com formato tabela
etcdctl member list --write-out=table

# Saida exemplo (cluster HA com 3 nos):
# +------------------+---------+--------+---------------------------+---------------------------+
# |        ID        | STATUS  |  NAME  |        PEER ADDRS         |       CLIENT ADDRS        |
# +------------------+---------+--------+---------------------------+---------------------------+
# | 8e9e05c52164694d | started | etcd-0 | https://10.0.1.10:2380    | https://10.0.1.10:2379    |
# | 91bc3c398fb3c146 | started | etcd-1 | https://10.0.1.11:2380    | https://10.0.1.11:2379    |
# | fd422379fda50e48 | started | etcd-2 | https://10.0.1.12:2380    | https://10.0.1.12:2379    |
# +------------------+---------+--------+---------------------------+---------------------------+
```

### Verificar Performance

```bash
# Teste de performance de escrita
etcdctl check perf

# Verificar alarmes ativos
etcdctl alarm list

# Desativar alarmes (apos resolver problema)
etcdctl alarm disarm
```

---

## Backup do etcd

### Fluxo de Backup

```plantuml,format=png
!include ../assets/diagrams/security/etcdctl-fluxo-de-backup-do-etcd-1.puml
```

### Criar Snapshot

```bash
# Definir variaveis
export ETCDCTL_API=3

# Criar snapshot
etcdctl snapshot save /backup/etcd-snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Saida:
# Snapshot saved at /backup/etcd-snapshot.db
```

### Verificar Snapshot

```bash
# Verificar integridade do snapshot
etcdctl snapshot status /backup/etcd-snapshot.db

# Com formato tabela (mais detalhado)
etcdctl snapshot status /backup/etcd-snapshot.db --write-out=table

# Saida exemplo:
# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# +----------+----------+------------+------------+
# | 6d3a8b2c |    45678 |       2345 |     4.5 MB |
# +----------+----------+------------+------------+
```

### Script de Backup Automatizado

```bash
#!/bin/bash
# etcd-backup.sh - Script de backup automatizado

set -e

# Configuracoes
BACKUP_DIR="/backup/etcd"
RETENTION_DAYS=7
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/etcd-snapshot-${TIMESTAMP}.db"

# Variaveis de ambiente
export ETCDCTL_API=3
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379

# Criar diretorio de backup
mkdir -p ${BACKUP_DIR}

# Executar backup
echo "[$(date)] Iniciando backup do etcd..."
etcdctl snapshot save ${BACKUP_FILE}

# Verificar integridade
if etcdctl snapshot status ${BACKUP_FILE} > /dev/null 2>&1; then
    echo "[$(date)] Backup criado com sucesso: ${BACKUP_FILE}"
    etcdctl snapshot status ${BACKUP_FILE} --write-out=table
else
    echo "[$(date)] ERRO: Backup falhou!"
    exit 1
fi

# Limpar backups antigos
echo "[$(date)] Removendo backups com mais de ${RETENTION_DAYS} dias..."
find ${BACKUP_DIR} -name "etcd-snapshot-*.db" -mtime +${RETENTION_DAYS} -delete

echo "[$(date)] Backup concluido!"
```

---

## Restore do etcd

### Fluxo de Restore

```plantuml,format=png
!include ../assets/diagrams/security/etcdctl-fluxo-de-restore-do-etcd-1.puml
```

### Executar Restore

```admonish important title="Importante"
O restore **NÃO** precisa de certificados, pois não conecta ao servidor etcd - ele apenas restaura os dados localmente.
```

```bash
export ETCDCTL_API=3

# Restore para NOVO diretorio
etcdctl snapshot restore /backup/etcd-snapshot.db \
  --data-dir=/var/lib/etcd-from-backup

# Saida:
# 2024-01-09 10:00:00.000000 I | mvcc: restore compact to 45678
# 2024-01-09 10:00:00.100000 I | etcdserver/membership: added member ...
```

### Restore Completo em Cluster kubeadm

```bash
# Passo 1: Parar kube-apiserver
mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/

# Aguardar parar
sleep 10
crictl ps | grep kube-apiserver  # Nao deve retornar nada

# Passo 2: Executar restore
export ETCDCTL_API=3
etcdctl snapshot restore /backup/etcd-snapshot.db \
  --data-dir=/var/lib/etcd-from-backup

# Passo 3: Atualizar manifesto do etcd
# Editar /etc/kubernetes/manifests/etcd.yaml
# Alterar:
#   --data-dir=/var/lib/etcd
# Para:
#   --data-dir=/var/lib/etcd-from-backup

# Passo 4: Atualizar volume hostPath
# No mesmo arquivo, alterar:
#   volumes:
#   - hostPath:
#       path: /var/lib/etcd
# Para:
#       path: /var/lib/etcd-from-backup

# Passo 5: Aguardar etcd reiniciar
sleep 30
crictl ps | grep etcd

# Se nao reiniciar automaticamente:
systemctl restart kubelet

# Passo 6: Restaurar kube-apiserver
mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/

# Passo 7: Verificar cluster
sleep 30
kubectl get nodes
kubectl get pods -A
```

---

## Consultas ao etcd

### Listar Chaves

```bash
# Listar todas as chaves (CUIDADO: pode ser muito output)
etcdctl get / --prefix --keys-only

# Listar chaves de um namespace especifico
etcdctl get /registry/pods/default --prefix --keys-only

# Listar chaves de secrets
etcdctl get /registry/secrets --prefix --keys-only

# Contar chaves
etcdctl get / --prefix --keys-only | wc -l
```

### Consultar Valores

```bash
# Obter valor de uma chave especifica
etcdctl get /registry/pods/default/my-pod

# Obter todos os pods de um namespace
etcdctl get /registry/pods/kube-system --prefix

# Obter com formato JSON (mais legivel)
etcdctl get /registry/namespaces/default -w json | jq .
```

### Estrutura das Chaves no Kubernetes

```plantuml,format=png
!include ../assets/diagrams/security/etcdctl-diagram-5-1.puml
```

---

## Gerenciamento de Membros

### Adicionar Novo Membro

```bash
# Adicionar novo membro ao cluster
etcdctl member add etcd-3 \
  --peer-urls=https://10.0.1.13:2380

# Saida com instrucoes para iniciar o novo membro
```

### Remover Membro

```bash
# Listar membros para obter ID
etcdctl member list

# Remover membro pelo ID
etcdctl member remove 8e9e05c52164694d
```

### Atualizar URLs de Membro

```bash
# Atualizar peer URLs
etcdctl member update 8e9e05c52164694d \
  --peer-urls=https://10.0.1.10:2380
```

---

## Troubleshooting

### Problemas Comuns

```plantuml,format=png
!include ../assets/diagrams/security/etcdctl-diagram-6-1.puml
```

### Debug de Conectividade

```bash
# Verificar se etcd esta rodando
crictl ps | grep etcd

# Verificar logs do etcd
crictl logs $(crictl ps | grep etcd | awk '{print $1}')

# Testar conectividade basica
curl -k https://127.0.0.1:2379/health

# Testar com certificados
curl --cacert /etc/kubernetes/pki/etcd/ca.crt \
     --cert /etc/kubernetes/pki/etcd/server.crt \
     --key /etc/kubernetes/pki/etcd/server.key \
     https://127.0.0.1:2379/health
```

### Verificar Certificados

```bash
# Ver detalhes do certificado
openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -text -noout

# Verificar data de expiracao
openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -noout -enddate

# Verificar se certificado corresponde a chave
openssl x509 -noout -modulus -in /etc/kubernetes/pki/etcd/server.crt | md5sum
openssl rsa -noout -modulus -in /etc/kubernetes/pki/etcd/server.key | md5sum
# Os hashes devem ser iguais
```

### Erros de Restore

```bash
# Erro: "permission denied" no restore
# Solucao: Verificar permissoes do diretorio destino
ls -la /var/lib/
chown -R root:root /var/lib/etcd-from-backup

# Erro: etcd nao inicia apos restore
# Verificar logs
journalctl -u kubelet | grep etcd

# Verificar se data-dir foi atualizado no manifesto
grep "data-dir" /etc/kubernetes/manifests/etcd.yaml

# Verificar se volume hostPath foi atualizado
grep -A5 "hostPath" /etc/kubernetes/manifests/etcd.yaml
```

---

## Comandos Essenciais - Resumo

| Operacao | Comando |
|----------|---------|
| **Definir API** | `export ETCDCTL_API=3` |
| **Health check** | `etcdctl endpoint health` |
| **Status endpoints** | `etcdctl endpoint status --write-out=table` |
| **Listar membros** | `etcdctl member list` |
| **Criar snapshot** | `etcdctl snapshot save <arquivo>` |
| **Verificar snapshot** | `etcdctl snapshot status <arquivo>` |
| **Restaurar snapshot** | `etcdctl snapshot restore <arquivo> --data-dir=<path>` |
| **Listar chaves** | `etcdctl get / --prefix --keys-only` |
| **Verificar alarmes** | `etcdctl alarm list` |

---

## Dicas para os Exames

```plantuml,format=png
!include ../assets/diagrams/security/etcdctl-diagram-7-1.puml
```

---

## Seguranca do etcd

### Criptografia de Secrets em Repouso

O etcd pode armazenar Secrets criptografados. Veja a configuracao em [etcd - Criptografia](etcd.md).

### Boas Praticas

```plantuml,format=png
!include ../assets/diagrams/security/etcdctl-diagram-8-1.puml
```

---

## Referencias

- [Backup e Restore](../maintenance/backup-e-restore.md)
- [etcd - Criptografia](etcd.md)
- [kube-apiserver](../cluster-components/kube-apiserver.md)
- [High Availability](fundamentals/high-availability.md)
- [TLS](TLS.md)
- [Documentacao Oficial etcd](https://etcd.io/docs/)
- [Kubernetes - Operating etcd](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/)
