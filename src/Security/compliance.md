# Compliance e Security Frameworks

```admonish info title="Certificações"
KCSA (10%), CKS (5%)
```

## Conceitos Fundamentais

### O que é Compliance?

Compliance é o conjunto de práticas para garantir que uma organização siga regulamentações, padrões e políticas de segurança aplicáveis.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title COMPLIANCE NO KUBERNETES

rectangle "Regulamentações" {
  card "GDPR" as gdpr
  card "HIPAA" as hipaa
  card "PCI DSS" as pci
  card "SOC 2" as soc
}

rectangle "Frameworks" {
  card "CIS Benchmark" as cis
  card "NIST" as nist
  card "ISO 27001" as iso
}

rectangle "Kubernetes" {
  card "Pod Security" as ps
  card "RBAC" as rbac
  card "Audit" as audit
  card "Network Policy" as np
}

@enduml
```

### Por que Compliance é Importante?

- **Legal**: Evitar multas e penalidades
- **Confiança**: Demonstrar segurança para clientes
- **Risco**: Reduzir exposição a ataques
- **Governança**: Controle e visibilidade

---

## CIS Kubernetes Benchmark

### O que é o CIS Benchmark?

O Center for Internet Security (CIS) publica benchmarks de configuração segura para diversas plataformas, incluindo Kubernetes.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title CIS BENCHMARK - SEÇÕES

card "1. Control Plane Components" as s1
card "2. etcd" as s2
card "3. Control Plane Configuration" as s3
card "4. Worker Nodes" as s4
card "5. Policies" as s5

note right of s1
  kube-apiserver
  kube-controller-manager
  kube-scheduler
end note

note right of s4
  kubelet
  kube-proxy
end note

note right of s5
  RBAC, PSP/PSA
  Network Policies
  Secrets
end note

@enduml
```

### Níveis do CIS Benchmark

| Nível | Descrição | Impacto |
|-------|-----------|---------|
| **Level 1** | Configurações básicas de segurança | Baixo impacto operacional |
| **Level 2** | Configurações avançadas | Pode impactar funcionalidade |

### kube-bench

Ferramenta para verificar conformidade com CIS Benchmark.

```bash
# Executar kube-bench (como container)
docker run --pid=host -v /etc:/etc:ro -v /var:/var:ro \
  -t aquasec/kube-bench:latest run --targets=master

# Como Job no cluster
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml

# Ver resultados
kubectl logs -l app=kube-bench

# Targets específicos
kube-bench run --targets=node
kube-bench run --targets=etcd
kube-bench run --targets=controlplane
kube-bench run --targets=policies
```

### Exemplos de Verificações CIS

#### 1.1 - API Server

```yaml
{{#include ../assets/security/compliance-example-1.yaml}}
```

#### 1.2 - etcd

```yaml
{{#include ../assets/security/compliance-example-2.yaml}}
```

#### 4.1 - Worker Nodes (kubelet)

```yaml
{{#include ../assets/security/compliance-example-3.yaml}}
```

---

## NIST Cybersecurity Framework

### Os Cinco Pilares

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title NIST CYBERSECURITY FRAMEWORK

card "1. IDENTIFY\nAssets, riscos, vulnerabilidades" as id
card "2. PROTECT\nControles preventivos" as pr
card "3. DETECT\nMonitoramento, detecção" as de
card "4. RESPOND\nResposta a incidentes" as re
card "5. RECOVER\nRecuperação" as rc

id --> pr
pr --> de
de --> re
re --> rc

@enduml
```

### Mapeamento para Kubernetes

| Pilar | Controles K8s |
|-------|---------------|
| **Identify** | Asset inventory, RBAC audit, vulnerability scanning |
| **Protect** | RBAC, Network Policy, Pod Security, Encryption |
| **Detect** | Audit logs, Falco, monitoring, alerting |
| **Respond** | Incident response, pod isolation, RBAC revoke |
| **Recover** | Backup/restore, disaster recovery |

---

## SOC 2

### Trust Service Criteria

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title SOC 2 - TRUST SERVICE CRITERIA

card "Security\nProteção contra acesso não autorizado" as sec
card "Availability\nSistema disponível para uso" as avail
card "Processing Integrity\nProcessamento correto" as proc
card "Confidentiality\nProteção de dados confidenciais" as conf
card "Privacy\nProteção de dados pessoais" as priv

@enduml
```

### Controles K8s para SOC 2

| Critério | Controles Kubernetes |
|----------|---------------------|
| **Security** | RBAC, Network Policy, Pod Security, Audit |
| **Availability** | HA control plane, PDB, HPA, multi-zone |
| **Processing Integrity** | Admission controllers, validation |
| **Confidentiality** | Encryption, Secrets management |
| **Privacy** | Data isolation, RBAC, audit logging |

---

## PCI DSS

### Requisitos Principais

Para ambientes que processam dados de cartão de crédito.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title PCI DSS - REQUISITOS CHAVE

card "1. Firewall\nNetwork segmentation" as r1
card "2. No default passwords\nCredential management" as r2
card "3. Protect stored data\nEncryption" as r3
card "4. Encrypt transmission\nTLS" as r4
card "5. Anti-malware\nImage scanning" as r5
card "6. Secure development\nCI/CD security" as r6

@enduml
```

### Implementação em Kubernetes

| Requisito PCI | Implementação K8s |
|---------------|-------------------|
| **Network segmentation** | Network Policies, namespaces |
| **Access control** | RBAC, ServiceAccounts |
| **Encryption** | TLS, encryption at rest, secrets |
| **Logging** | Audit logs, centralized logging |
| **Vulnerability management** | Image scanning, admission policies |

---

## HIPAA

### Requisitos para Dados de Saúde

| Requisito | Implementação K8s |
|-----------|-------------------|
| **Access controls** | RBAC granular |
| **Audit controls** | Audit logging habilitado |
| **Integrity** | Image signing, admission control |
| **Transmission security** | mTLS, Network Policy |
| **Encryption** | Encryption at rest |

---

## GDPR

### Requisitos para Dados Pessoais (EU)

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title GDPR - REQUISITOS CHAVE

card "Data Protection\nCriptografia, pseudonymization" as dp
card "Access Control\nPrincípio do menor privilégio" as ac
card "Audit Trail\nRastreabilidade de acessos" as at
card "Data Portability\nBackup, export" as port
card "Right to Erasure\nDeleção de dados" as del

@enduml
```

### Implementação em Kubernetes

| Requisito | Controle K8s |
|-----------|--------------|
| **Data Protection** | Encryption at rest, secrets management |
| **Access Control** | RBAC, namespaces, Network Policy |
| **Audit Trail** | Audit logs, Falco |
| **Breach Notification** | Alerting, incident response |

---

## Ferramentas de Compliance

### Scanning e Validação

| Ferramenta | Função | Framework |
|------------|--------|-----------|
| **kube-bench** | CIS Benchmark scanning | CIS |
| **kubescape** | Multi-framework scanning | NSA, MITRE, CIS |
| **Polaris** | Best practices validation | Custom |
| **Starboard** | Security reports | Multiple |
| **Trivy** | Vulnerability + config scan | Multiple |

### kubescape

```bash
# Instalar kubescape
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash

# Scan com NSA framework
kubescape scan framework nsa

# Scan com CIS Benchmark
kubescape scan framework cis-v1.23-t1.0.1

# Scan específico de namespace
kubescape scan framework nsa --include-namespaces production

# Export HTML report
kubescape scan framework nsa --format html --output report.html
```

### Polaris

```bash
# Instalar Polaris
kubectl apply -f https://github.com/FairwindsOps/polaris/releases/latest/download/dashboard.yaml

# Acessar dashboard
kubectl port-forward -n polaris svc/polaris-dashboard 8080:80

# CLI scan
polaris audit --audit-path ./manifests/
```

---

## Audit Logging

### Configuração de Audit

```yaml
{{#include ../assets/security/policy-1.yaml}}
```

### Níveis de Audit

| Nível | O que registra |
|-------|----------------|
| **None** | Nada |
| **Metadata** | Request metadata (user, timestamp, resource) |
| **Request** | Metadata + request body |
| **RequestResponse** | Metadata + request + response bodies |

### Habilitar Audit no API Server

```yaml
{{#include ../assets/security/compliance-example-5.yaml}}
```

---

## Compliance as Code

### Policy as Code

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title POLICY AS CODE

rectangle "Define" {
  card "Rego (OPA)" as rego
  card "Kyverno YAML" as kyv
}

rectangle "Enforce" {
  card "Admission Controller" as ac
  card "CI/CD Pipeline" as ci
}

rectangle "Audit" {
  card "Continuous Scanning" as scan
  card "Compliance Reports" as rep
}

rego --> ac
kyv --> ac
ac --> scan
ci --> scan
scan --> rep

@enduml
```

### OPA/Gatekeeper Policy

```yaml
{{#include ../assets/security/constrainttemplate-k8srequiredlabels.yaml}}
```

### Kyverno Policy

```yaml
{{#include ../assets/security/clusterpolicy-require-labels.yaml}}
```

---

## Relatórios de Compliance

### Gerando Evidências

```bash
# Exportar RBAC atual
kubectl get roles,rolebindings,clusterroles,clusterrolebindings -A -o yaml > rbac-export.yaml

# Exportar Network Policies
kubectl get networkpolicies -A -o yaml > networkpolicies.yaml

# Exportar Pod Security
kubectl get pods -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}: {.spec.securityContext}{"\n"}{end}'

# Audit logs (se habilitado)
cat /var/log/kubernetes/audit.log | jq .
```

### Dashboard de Compliance

```bash
# Starboard operator
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/starboard/main/deploy/static/starboard.yaml

# Ver relatórios
kubectl get vulnerabilityreports -A
kubectl get configauditreports -A
kubectl get ciskubebenchreports -A
```

---

## Dicas para o Exame

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS - COMPLIANCE

card "1. CIS Benchmark\nConheça as seções principais" as d1
card "2. kube-bench\nSaiba executar e interpretar" as d2
card "3. Audit logging\nNíveis: None, Metadata, Request, RequestResponse" as d3
card "4. Frameworks\nNIST (5 pilares), SOC 2 (Trust Criteria)" as d4
card "5. Tools\nkube-bench, kubescape, Polaris" as d5

@enduml
```

### Conceitos-Chave

| Conceito | Lembrar |
|----------|---------|
| **CIS Benchmark** | L1 = básico, L2 = avançado |
| **kube-bench** | Ferramenta para validar CIS |
| **NIST** | Identify, Protect, Detect, Respond, Recover |
| **Audit levels** | None < Metadata < Request < RequestResponse |
| **Policy as Code** | OPA/Gatekeeper, Kyverno |

---

## Referências

### Documentação
- [CIS Benchmarks](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Kubernetes Audit](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/)

### Arquivos Relacionados
- [CIS Benchmark](cis-benchmark.md)
- [Audit](audit.md)
- [RBAC](rbac.md)
- [Pod Security Admission](pod-security-admission.md)
- [Open Policy Agent](open-policy-agent.md)
- [KCSA](../certifications/kcsa.md)
