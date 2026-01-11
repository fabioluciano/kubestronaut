# Kubernetes Audit Logging

<span class="badge badge-cks">CKS</span>

---

## O que é Audit Logging?

```admonish info title="Kubernetes Audit"
O Kubernetes Audit fornece um registro cronológico e seguro de todas as ações realizadas no cluster, documentando a sequência de atividades que afetaram o sistema. É essencial para segurança, compliance e troubleshooting.
```

### Por que usar Audit?

| Objetivo | Descrição |
|----------|-----------|
| **Segurança** | Detectar atividades suspeitas ou não autorizadas |
| **Compliance** | Atender requisitos regulatórios (SOX, HIPAA, PCI-DSS) |
| **Forense** | Investigar incidentes de segurança |
| **Troubleshooting** | Entender problemas e comportamentos do cluster |

### Perguntas que Audit responde

- **Quem** fez a ação? (usuário, service account)
- **Quando** foi feito? (timestamp preciso)
- **O que** foi feito? (recurso, operação)
- **Como** foi feito? (API, método)
- **De onde** veio? (IP de origem)

---

## Arquitetura do Audit

```admonish note title="Fluxo"
Request → API Server → Audit Policy → Backend (Log/Webhook) → Storage/SIEM
```

### Estágios de Auditoria

| Estágio | Descrição | Quando usar |
|---------|-----------|-------------|
| `RequestReceived` | Assim que a requisição é recebida | Auditoria completa |
| `ResponseStarted` | Headers enviados, corpo pendente (watch) | Long-running requests |
| `ResponseComplete` | Resposta completa enviada | Mais comum |
| `Panic` | Ocorreu um panic no handler | Debug de problemas |

### Níveis de Log (Audit Levels)

| Nível | O que loga | Use case |
|-------|------------|----------|
| `None` | Nada | Excluir recursos ruidosos |
| `Metadata` | Metadados (user, timestamp, resource) | Produção - baixo volume |
| `Request` | Metadata + corpo da requisição | Debug de criação |
| `RequestResponse` | Request + corpo da resposta | Debug completo |

```admonish warning title="Performance"
`RequestResponse` pode gerar logs muito grandes. Use com cuidado em produção!
```

---

## Configuração do API Server

### Flags Essenciais

| Flag | Descrição | Recomendado |
|------|-----------|-------------|
| `--audit-policy-file` | Arquivo de política de audit | Obrigatório |
| `--audit-log-path` | Caminho do arquivo de log | `/var/log/kubernetes/audit.log` |
| `--audit-log-maxage` | Dias para reter logs | 30 |
| `--audit-log-maxbackup` | Arquivos de backup | 10 |
| `--audit-log-maxsize` | Tamanho máximo (MB) | 100 |

## Políticas de Auditoria

### Estrutura da Policy

```yaml
{{#include ../assets/security/audit/audit-policy-structure.yaml}}
```

### Exemplos de Policy

```admonish tip title="Dica"
Use `- level: None` no início para excluir recursos ruidosos (healthchecks, etc.)
```

```yaml
{{#include ../assets/security/policy.yaml}}
```

### Exemplo Avançado

```yaml
{{#include ../assets/security/audit-example-2.yaml}}
```

### Policy para Secrets em Produção

```admonish danger title="Segurança"
Nunca logue o conteúdo de Secrets! Use `Metadata` ou `None` para recursos sensíveis.
```

```yaml
{{#include ../assets/security/audit/audit-policy-secrets-prod.yaml}}
```


---

### API Server Flags

```yaml
{{#include ../assets/security/audit/kube-apiserver-audit-flags.yaml}}
```

### Volumes do API Server

```yaml
{{#include ../assets/security/audit/kube-apiserver-volumes.yaml}}
```

---

## Políticas de Auditoria

### Estrutura da Policy

```yaml
{{#include ../assets/security/audit/audit-policy-structure.yaml}}
```

### Exemplos de Policy

```admonish tip title="Dica"
Use `- level: None` no início para excluir recursos ruidosos (healthchecks, etc.)
```

```yaml
{{#include ../assets/security/policy.yaml}}
```

### Exemplo Avançado

```yaml
{{#include ../assets/security/audit-example-2.yaml}}
```

### Policy para Secrets em Produção

```admonish danger title="Segurança"
Nunca logue o conteúdo de Secrets! Use `Metadata` ou `None` para recursos sensíveis.
```

```yaml
{{#include ../assets/security/audit/audit-policy-secrets-prod.yaml}}
```

---

## Backends de Auditoria

### Log Backend

O backend mais simples - grava em arquivo local:

```yaml
{{#include ../assets/security/audit/audit-log-backend.yaml}}
```

### Webhook Backend

Para integração com SIEM/ferramentas externas:

```yaml
{{#include ../assets/security/audit/audit-webhook-config.yaml}}
```

### Webhook Flags

```yaml
{{#include ../assets/security/audit/audit-webhook-flags.yaml}}
```

### Integração com Falco

```yaml
{{#include ../assets/security/audit/falco-webhook.yaml}}
```

---

## Analisar Logs de Audit

### Formato do Log

```json
{
  "kind": "Event",
  "apiVersion": "audit.k8s.io/v1",
  "level": "Metadata",
  "stage": "ResponseComplete",
  "requestURI": "/api/v1/namespaces/default/secrets",
  "verb": "create",
  "user": {
    "username": "admin",
    "groups": ["system:masters"]
  },
  "sourceIPs": ["10.0.0.1"],
  "objectRef": {
    "resource": "secrets",
    "namespace": "default",
    "name": "my-secret"
  },
  "responseStatus": {
    "metadata": {},
    "code": 201
  }
}
```

### Comandos Úteis

```bash
# Ver últimos eventos
tail -f /var/log/kubernetes/audit.log | jq .

# Filtrar por usuário
cat audit.log | jq 'select(.user.username=="admin")'

# Filtrar por recurso
cat audit.log | jq 'select(.objectRef.resource=="secrets")'

# Eventos de erro
cat audit.log | jq 'select(.responseStatus.code >= 400)'

# Criação de recursos
cat audit.log | jq 'select(.verb=="create")'
```

---

## Troubleshooting

### API Server não inicia após configurar Audit

```bash
# Verificar logs do API Server
sudo crictl logs $(sudo crictl ps -a | grep kube-apiserver | awk '{print $1}')

# Problemas comuns:
# 1. Policy file não existe
# 2. Policy com sintaxe inválida
# 3. Log path não tem permissão de escrita
```

### Validar Policy

```bash
# Verificar sintaxe YAML
kubectl apply --dry-run=client -f audit-policy.yaml

# Verificar campos obrigatórios
# - apiVersion: audit.k8s.io/v1
# - kind: Policy
# - rules: []
```

### Logs não estão sendo gerados

```bash
# Verificar se flag está configurada
ps aux | grep kube-apiserver | grep audit

# Verificar permissões do diretório
ls -la /var/log/kubernetes/

# Verificar espaço em disco
df -h
```

---

## Dicas para o Exame CKS

```admonish tip title="Dicas CKS - Audit"
1. **Policy file é obrigatório**: Sem `--audit-policy-file`, nada é logado
2. **Ordem das regras importa**: Primeira regra que faz match é usada
3. **Excluir noise primeiro**: Use `level: None` para healthchecks
4. **Secrets**: Nunca log level `RequestResponse` para secrets
5. **Volumes**: API Server precisa de volume mounts para policy e logs
```

### Cenários Comuns no Exame

1. **Configurar audit básico**: Adicionar flags e policy ao API Server
2. **Logar apenas secrets**: Policy específica para secrets com level Metadata
3. **Integrar com Falco**: Configurar webhook backend

### Comandos para Memorizar

```bash
# Localização do API Server manifest
/etc/kubernetes/manifests/kube-apiserver.yaml

# Onde colocar policy
/etc/kubernetes/audit-policy.yaml

# Onde ficam os logs
/var/log/kubernetes/audit/audit.log
```

---

## Referências

- [Kubernetes Auditing](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/)
- [Falco](falco.md) - Integração para detecção de ameaças
- [RBAC](rbac.md) - Controle de acesso
