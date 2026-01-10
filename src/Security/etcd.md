# Seguranca do etcd

> **Certificacoes**: CKS (Cluster Hardening), CKA (Cluster Architecture)

## Conceitos Fundamentais

O **etcd** e o banco de dados distribuido key-value que armazena todo o estado do cluster Kubernetes. Como contem informacoes sensiveis (Secrets, ConfigMaps, dados de autenticacao), sua seguranca e critica.

```admonish warning title="Importancia do etcd"
Acesso ao etcd significa acesso TOTAL ao cluster. Um atacante com acesso ao etcd pode:
- Ler todos os Secrets (incluindo tokens de ServiceAccount)
- Modificar configuracoes do cluster
- Criar usuarios admin
- Deletar recursos
```

```plantuml,format=png
!include ../assets/diagrams/security/etcd-etcd-no-kubernetes-1.puml
```

## Arquitetura de Seguranca

```plantuml,format=png
!include ../assets/diagrams/security/etcd-camadas-de-seguranca-do-etcd-1.puml
```

## TLS para Comunicacao

O etcd requer TLS para duas comunicacoes:

| Tipo | Descricao | Certificados |
|------|-----------|--------------|
| **Client-to-Server** | API Server -> etcd | etcd-ca, apiserver-etcd-client |
| **Peer-to-Peer** | etcd -> etcd (cluster) | etcd-ca, etcd-peer |

### Certificados do etcd

```bash
# Estrutura em /etc/kubernetes/pki/etcd/
/etc/kubernetes/pki/etcd/
├── ca.crt                    # CA do etcd
├── ca.key                    # Chave privada da CA
├── server.crt                # Certificado do servidor etcd
├── server.key                # Chave do servidor
├── peer.crt                  # Certificado peer (cluster)
├── peer.key                  # Chave peer
├── healthcheck-client.crt    # Cliente para health checks
└── healthcheck-client.key
```

### Configuracao TLS no etcd

```yaml
{{#include ../assets/security/etcd-example-1.yaml}}
```

## Criptografia em Repouso (Encryption at Rest)

Por padrao, os dados no etcd sao armazenados em texto plano. A criptografia em repouso protege os dados mesmo se o disco for comprometido.

### Providers de Criptografia

| Provider | Descricao | Uso |
|----------|-----------|-----|
| `identity` | Sem criptografia | Default, nao usar em producao |
| `aescbc` | AES-CBC com PKCS#7 padding | Recomendado |
| `aesgcm` | AES-GCM | Requer rotacao frequente |
| `kms` | External KMS | Melhor para producao |
| `secretbox` | XSalsa20 + Poly1305 | Alternativa ao AES |

### Configuracao Basica

```yaml
{{#include ../assets/security/etcd/encryption-config.yaml}}
```

### Configuracao com Multiplos Recursos

```yaml
{{#include ../assets/security/etcd/encryption-config-multiple.yaml}}
```

### Habilitar no API Server

```yaml
{{#include ../assets/security/etcd/kube-apiserver-encryption.yaml}}
```

### Processo Completo

```plantuml,format=png
!include ../assets/diagrams/security/etcd-habilitando-encryption-at-rest-1.puml
```

### Gerar Chave de Criptografia

```bash
# Gerar chave de 32 bytes em base64
head -c 32 /dev/urandom | base64

# Exemplo de output:
# c2VjcmV0a2V5MTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0
```

### Re-criptografar Dados Existentes

Apos habilitar encryption, dados antigos permanecem nao criptografados. Para criptografa-los:

```bash
# Re-criptografar todos os secrets
kubectl get secrets --all-namespaces -o json | kubectl replace -f -

# Re-criptografar todos os configmaps
kubectl get configmaps --all-namespaces -o json | kubectl replace -f -
```

### Verificar se Dados Estao Criptografados

```bash
# Usar etcdctl para ler diretamente
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/mysecret | hexdump -C

# Se criptografado, vera algo como:
# k8s:enc:aescbc:v1:key1:...dados binarios...

# Se NAO criptografado, vera os dados em texto:
# /registry/secrets/default/mysecret
# {"apiVersion":"v1","data":{"password":"...
```

## Rotacao de Chaves

A rotacao de chaves e uma pratica de seguranca importante.

### Processo de Rotacao

```yaml
{{#include ../assets/security/etcd/encryption-key-rotation.yaml}}
```

### Passos para Rotacao

```bash
# 1. Adicionar nova chave como PRIMEIRA no array
# (editar enc.yaml conforme exemplo acima)

# 2. Reiniciar API Server
mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/
sleep 30
mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/

# 3. Re-criptografar todos os secrets com nova chave
kubectl get secrets --all-namespaces -o json | kubectl replace -f -

# 4. (Opcional) Remover chave antiga apos verificar
# Editar enc.yaml removendo key1

# 5. Reiniciar API Server novamente
```

## KMS Provider

Para ambientes de producao, use um KMS externo (AWS KMS, Azure Key Vault, HashiCorp Vault).

```yaml
{{#include ../assets/security/etcd/kms-provider.yaml}}
```

```admonish info title="Vantagens do KMS"
- Chaves nunca ficam no disco do cluster
- Rotacao de chaves gerenciada externamente
- Audit logging do KMS
- Compliance (FIPS, PCI-DSS)
```

## RBAC do etcd

O etcd possui seu proprio sistema de controle de acesso.

### Habilitar Autenticacao

```bash
# No cluster etcd
etcdctl user add root
etcdctl auth enable

# Criar usuario para API Server
etcdctl user add apiserver
etcdctl user grant-role apiserver root
```

```admonish warning title="Kubernetes e RBAC do etcd"
O Kubernetes geralmente NAO usa o RBAC nativo do etcd. Em vez disso, confia nos certificados TLS para autenticacao. O RBAC do etcd e mais relevante quando etcd e compartilhado entre aplicacoes.
```

## Backup Seguro

### Criar Snapshot

```bash
# Backup do etcd
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Verificar snapshot
ETCDCTL_API=3 etcdctl snapshot status snapshot.db
```

### Criptografar Backup

```bash
# Criptografar com GPG
gpg --symmetric --cipher-algo AES256 snapshot.db
# Gera: snapshot.db.gpg

# Ou com OpenSSL
openssl enc -aes-256-cbc -salt -in snapshot.db -out snapshot.db.enc
```

### Restore do Backup

```bash
# Restaurar snapshot
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
  --data-dir=/var/lib/etcd-restored \
  --name=master \
  --initial-cluster=master=https://127.0.0.1:2380 \
  --initial-advertise-peer-urls=https://127.0.0.1:2380
```

## Comandos ETCDCTL

```bash
# Variaveis de ambiente para ETCDCTL
export ETCDCTL_API=3
export ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key

# Health check
etcdctl endpoint health

# Status do cluster
etcdctl endpoint status --write-out=table

# Listar membros
etcdctl member list

# Ver todas as chaves (CUIDADO em producao!)
etcdctl get "" --prefix --keys-only | head

# Ver um secret especifico
etcdctl get /registry/secrets/default/mysecret

# Contar recursos
etcdctl get /registry/pods --prefix --keys-only | wc -l

# Backup
etcdctl snapshot save /backup/etcd-snapshot.db

# Status do snapshot
etcdctl snapshot status /backup/etcd-snapshot.db --write-out=table

# Defragmentar (recuperar espaco)
etcdctl defrag
```

## Hardening do etcd

### Checklist

| Item | Acao | Status |
|------|------|--------|
| TLS Client | Certificados obrigatorios | Obrigatorio |
| TLS Peer | Certificados para cluster | Obrigatorio |
| Encryption at Rest | Criptografia de secrets | Recomendado |
| Porta 2379 | Nao expor externamente | Obrigatorio |
| Backup | Automatizado e criptografado | Obrigatorio |
| Acesso Filesystem | Restrito (permissoes 700) | Obrigatorio |

### Permissoes de Arquivos

```bash
# Verificar permissoes
ls -la /var/lib/etcd
# Deve ser: drwx------ (700) root:root

# Corrigir se necessario
chmod 700 /var/lib/etcd
chown -R root:root /var/lib/etcd

# Certificados
chmod 600 /etc/kubernetes/pki/etcd/*.key
chmod 644 /etc/kubernetes/pki/etcd/*.crt
```

### Isolamento de Rede

```bash
# etcd NAO deve ser acessivel externamente
# Apenas o API Server deve conseguir conectar

# Verificar se porta esta exposta
ss -tlnp | grep 2379
# Deve mostrar apenas 127.0.0.1:2379 ou IP interno
```

## Troubleshooting

### etcd Nao Inicia

```admonish failure title="Erro: etcd cluster is unavailable or misconfigured"
**Causas comuns**:
1. Certificados invalidos ou expirados
2. Data directory corrompido
3. Configuracao de cluster incorreta

**Solucao**:
1. Verificar logs: `journalctl -u etcd` ou `crictl logs <etcd-container>`
2. Verificar certificados: `openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -noout -dates`
3. Restaurar de backup se necessario
```

### Erro de Criptografia

```admonish failure title="Erro: decryption failed"
**Causa**: Chave de criptografia incorreta ou removida.

**Solucao**:
1. Verificar EncryptionConfiguration
2. Garantir que a chave antiga ainda existe (se rotacionando)
3. Restaurar de backup nao criptografado
```

### Verificar Health

```bash
# Via etcdctl
etcdctl endpoint health

# Via kubectl (se cluster funciona)
kubectl get componentstatuses

# Via API direta
curl -k --cert /etc/kubernetes/pki/etcd/server.crt \
  --key /etc/kubernetes/pki/etcd/server.key \
  https://127.0.0.1:2379/health
```

## Dicas para o Exame CKS

```admonish tip title="Dicas CKS"
1. **Encryption at Rest**: Saiba configurar do zero
2. **etcdctl**: Memorize comandos com certificados
3. **Backup**: `etcdctl snapshot save`
4. **Verificar criptografia**: Use `etcdctl get` + hexdump
5. **Localizacao**: Certificados em `/etc/kubernetes/pki/etcd/`
```

## Fluxo de Seguranca

```plantuml,format=png
!include ../assets/diagrams/security/etcd-fluxo-de-dados-seguros-no-etcd-1.puml
```

## Best Practices

1. **Sempre use TLS** - Nunca execute etcd sem TLS
2. **Habilite encryption at rest** - Obrigatorio para producao
3. **Isole a rede** - etcd so acessivel pelo API Server
4. **Backups regulares** - Automatize e criptografe
5. **Rotacione chaves** - Pelo menos anualmente
6. **Monitore** - Alertas para health e espaco em disco
7. **Use KMS em producao** - Melhor gerenciamento de chaves
8. **Permissoes restritivas** - 700 para diretorio de dados
9. **Nao exponha externamente** - Porta 2379 apenas interna
10. **Documente procedimentos** - Runbook de recuperacao

## Recursos Adicionais

- [etcd Security](https://etcd.io/docs/v3.5/op-guide/security/)
- [Kubernetes Encrypting Secret Data at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/)
- [etcd Disaster Recovery](https://etcd.io/docs/v3.5/op-guide/recovery/)
- [Using etcdctl](https://etcd.io/docs/v3.5/dev-guide/interacting_v3/)
