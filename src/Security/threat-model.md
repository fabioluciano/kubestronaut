# Kubernetes Threat Model

```admonish info title="Certificações"
KCSA (16%), CKS (10%)
```

## Conceitos Fundamentais

### O que é Threat Modeling?

Threat Modeling é o processo de identificar potenciais ameaças e vulnerabilidades em um sistema, avaliar riscos e definir contramedidas.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title PROCESSO DE THREAT MODELING

rectangle "1. Identificar Assets" as a1
rectangle "2. Criar Arquitetura" as a2
rectangle "3. Identificar Ameaças" as a3
rectangle "4. Avaliar Riscos" as a4
rectangle "5. Definir Mitigações" as a5

a1 --> a2
a2 --> a3
a3 --> a4
a4 --> a5

@enduml
```

### Por que é importante?

- Identificar vulnerabilidades antes de ataques
- Priorizar esforços de segurança
- Comunicar riscos para stakeholders
- Compliance e auditoria
- Arquitetura segura desde o início (Shift-Left)

---

## STRIDE Framework

Framework desenvolvido pela Microsoft para categorizar ameaças.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title STRIDE FRAMEWORK

card "S - Spoofing Identity\nFingir ser outra entidade" as s
card "T - Tampering with Data\nModificar dados indevidamente" as t
card "R - Repudiation\nNegar ter realizado ação" as r
card "I - Information Disclosure\nVazamento de informações" as i
card "D - Denial of Service\nIndisponibilizar serviço" as d
card "E - Elevation of Privilege\nObter permissões indevidas" as e

@enduml
```

### STRIDE no Kubernetes

| Ameaça | Exemplo no K8s | Mitigação |
|--------|----------------|-----------|
| **Spoofing** | ServiceAccount falso, certificado forjado | mTLS, RBAC, token validation |
| **Tampering** | Modificar ConfigMap, alterar imagem | Admission control, image signing |
| **Repudiation** | Ação sem audit log | Audit logging, immutable logs |
| **Info Disclosure** | Secret exposto, metadata leak | Encryption, RBAC, Network Policy |
| **DoS** | Fork bomb, resource exhaustion | ResourceQuota, LimitRange, PDB |
| **Elevation** | Container escape, RBAC bypass | Pod Security, Seccomp, AppArmor |

---

## Attack Surfaces no Kubernetes

### Visão Geral

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title ATTACK SURFACES

rectangle "External" {
  card "Ingress/LoadBalancer" as ext1
  card "NodePort Services" as ext2
  card "API Server (se exposto)" as ext3
}

rectangle "Network" {
  card "Pod-to-Pod" as net1
  card "Pod-to-Service" as net2
  card "Egress to Internet" as net3
}

rectangle "Node" {
  card "kubelet API" as node1
  card "Container Runtime" as node2
  card "Host filesystem" as node3
}

rectangle "Workload" {
  card "Application vulnerabilities" as work1
  card "Container image" as work2
  card "Secrets/ConfigMaps" as work3
}

@enduml
```

### API Server Attacks

| Vetor | Descrição | Mitigação |
|-------|-----------|-----------|
| **Anonymous access** | Acesso não autenticado | `--anonymous-auth=false` |
| **Weak auth** | Tokens fracos, static tokens | OIDC, certificates |
| **Insecure port** | Porta 8080 sem auth | Desabilitar (deprecated) |
| **RBAC bypass** | Permissões excessivas | Least privilege, audit |

### etcd Attacks

| Vetor | Descrição | Mitigação |
|-------|-----------|-----------|
| **Direct access** | Conexão direta ao etcd | Firewall, mTLS |
| **Unencrypted data** | Secrets em plaintext | Encryption at rest |
| **Backup theft** | Backup não criptografado | Encrypted backups |

### Node-Level Attacks

| Vetor | Descrição | Mitigação |
|-------|-----------|-----------|
| **kubelet API** | Acesso anônimo ao kubelet | Webhook auth, disable anonymous |
| **Container escape** | Sair do container para o host | Seccomp, AppArmor, SELinux |
| **Host path mount** | Acesso ao filesystem do host | Pod Security, admission |
| **Privileged container** | Container com acesso root | Pod Security Restricted |

### Network Attacks

| Vetor | Descrição | Mitigação |
|-------|-----------|-----------|
| **Lateral movement** | Mover entre pods/namespaces | Network Policies |
| **Service impersonation** | Fingir ser outro serviço | mTLS, Service Mesh |
| **Metadata API** | Acessar cloud metadata (169.254.169.254) | Network Policy egress |
| **DNS spoofing** | Poisoning de DNS | CoreDNS security, Network Policy |

---

## Threat Actors

### Tipos de Atacantes

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title THREAT ACTORS

rectangle "External" {
  card "Script Kiddies\nBaixa sofisticação" as ext1
  card "Cybercriminals\nMotivação financeira" as ext2
  card "Nation States\nAPT, recursos ilimitados" as ext3
}

rectangle "Internal" {
  card "Malicious Insider\nAcesso legítimo" as int1
  card "Negligent User\nErros acidentais" as int2
  card "Compromised Account\nCredenciais roubadas" as int3
}

@enduml
```

### Motivações

| Actor | Motivação | Alvo Típico |
|-------|-----------|-------------|
| **Script Kiddie** | Diversão, fama | Vulnerabilidades conhecidas |
| **Cybercriminal** | Dinheiro | Ransomware, cryptomining |
| **Nation State** | Espionagem, sabotagem | Infraestrutura crítica |
| **Insider** | Vingança, lucro | Dados sensíveis |

---

## Attack Scenarios

### Scenario 1: Compromised Container

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title CONTAINER COMPROMISE

rectangle "Attacker" as att

rectangle "Compromised Pod" as pod {
  card "1. Exploit app vulnerability" as s1
  card "2. Access ServiceAccount token" as s2
  card "3. Query API Server" as s3
  card "4. Escalate privileges" as s4
}

att --> s1
s1 --> s2
s2 --> s3
s3 --> s4

note bottom
  Mitigação:
  • RBAC mínimo para ServiceAccount
  • automountServiceAccountToken: false
  • Network Policy
  • Pod Security Restricted
end note

@enduml
```

### Scenario 2: Supply Chain Attack

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title SUPPLY CHAIN ATTACK

rectangle "Attack Chain" {
  card "1. Compromete base image" as s1
  card "2. Imagem usada no build" as s2
  card "3. Deploy em produção" as s3
  card "4. Backdoor ativo" as s4
}

s1 --> s2
s2 --> s3
s3 --> s4

note bottom
  Mitigação:
  • Image scanning (Trivy)
  • Image signing (Cosign)
  • Admission policies
  • SBOM verification
end note

@enduml
```

### Scenario 3: Lateral Movement

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title LATERAL MOVEMENT

rectangle "Namespace A" {
  card "Compromised\nPod A" as poda
}

rectangle "Namespace B" {
  card "Database\nPod" as podb
}

rectangle "Namespace C" {
  card "Secret\nStore" as podc
}

poda --> podb : "Sem Network Policy"
podb --> podc : "Cross-namespace"

note bottom
  Mitigação:
  • Default deny Network Policy
  • Namespace isolation
  • Service Mesh mTLS
end note

@enduml
```

---

## Kubernetes-Specific Threats

### Container Escape

```yaml
{{#include ../assets/security/threat-model-example-1.yaml}}
```

**Mitigações:**
- Pod Security Standard: Restricted
- Seccomp profile
- AppArmor/SELinux
- No privileged containers

### RBAC Misconfiguration

```yaml
{{#include ../assets/security/threat-model-example-2.yaml}}
```

### Secrets Exposure

| Vetor | Descrição | Mitigação |
|-------|-----------|-----------|
| **Environment variables** | Vazamento em logs, ps | Volume mounts |
| **Unencrypted etcd** | Secrets em plaintext | Encryption at rest |
| **RBAC permissivo** | Acesso desnecessário | Least privilege |
| **Git commit** | Secret no código | Secret scanning, external secrets |

### Resource Exhaustion (DoS)

```yaml
{{#include ../assets/security/threat-model-example-3.yaml}}
```

---

## Ferramentas de Threat Assessment

### Scanning e Testing

| Ferramenta | Função |
|------------|--------|
| **kube-hunter** | Penetration testing |
| **kube-bench** | CIS Benchmark |
| **Trivy** | Vulnerability scanning |
| **Falco** | Runtime detection |
| **kubescape** | Security posture |

### kube-hunter

```bash
# Executar kube-hunter
# Como pod no cluster (internal scan)
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-hunter/main/job.yaml

# Ver resultados
kubectl logs -l app=kube-hunter
```

### Trivy para Threat Assessment

```bash
# Scan de vulnerabilidades
trivy image nginx:latest

# Scan de configuração K8s
trivy config deployment.yaml

# Scan do cluster
trivy k8s --report summary cluster
```

---

## Mitigações por Camada

### Control Plane

| Componente | Mitigações |
|------------|------------|
| **API Server** | RBAC, Audit, TLS, Admission Controllers |
| **etcd** | Encryption, mTLS, Network isolation |
| **Scheduler** | Secure communication |
| **Controller Manager** | ServiceAccount com least privilege |

### Worker Nodes

| Componente | Mitigações |
|------------|------------|
| **kubelet** | Webhook auth, disable anonymous |
| **Container Runtime** | Secure configuration |
| **OS** | Hardening, minimal image |

### Workloads

| Aspecto | Mitigações |
|---------|------------|
| **Pods** | Pod Security, Seccomp, AppArmor |
| **Network** | Network Policies, mTLS |
| **Secrets** | Encryption, external secrets |
| **Images** | Scanning, signing, admission |

---

## Best Practices

### Defense in Depth

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DEFENSE IN DEPTH

rectangle "Camada 1: Network" {
  card "Firewall, Network Policy" as c1
}

rectangle "Camada 2: Identity" {
  card "RBAC, mTLS, OIDC" as c2
}

rectangle "Camada 3: Workload" {
  card "Pod Security, Seccomp" as c3
}

rectangle "Camada 4: Data" {
  card "Encryption, Secrets Mgmt" as c4
}

rectangle "Camada 5: Detection" {
  card "Audit, Monitoring, Falco" as c5
}

c1 -[hidden]down-> c2
c2 -[hidden]down-> c3
c3 -[hidden]down-> c4
c4 -[hidden]down-> c5

@enduml
```

### Zero Trust Principles

1. **Never trust, always verify** - Autenticação em todas as camadas
2. **Least privilege** - Mínimo de permissões necessárias
3. **Assume breach** - Planejar para quando (não se) houver comprometimento
4. **Verify explicitly** - Validar todas as requests

---

## Dicas para o Exame

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS - THREAT MODEL

card "1. Conheça STRIDE\nCada letra e exemplo em K8s" as d1
card "2. Attack surfaces\nAPI Server, etcd, kubelet, pods" as d2
card "3. Container escape\nPrivileged, capabilities, hostPID" as d3
card "4. Lateral movement\nNetwork Policy é a mitigação" as d4
card "5. Supply chain\nImage scanning, signing, SBOM" as d5

@enduml
```

### Conceitos-Chave

| Conceito | Lembrar |
|----------|---------|
| **STRIDE** | 6 categorias de ameaças |
| **Attack surface** | API Server é o alvo principal |
| **Container escape** | Privileged = risco máximo |
| **Lateral movement** | Network Policy previne |
| **Zero Trust** | Never trust, always verify |

---

## Referências

### Documentação
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/)
- [STRIDE](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [OWASP Kubernetes Security](https://owasp.org/www-project-kubernetes-security/)

### Arquivos Relacionados
- [Os Quatro Cs](os-quatro-cs.md)
- [Pod Security Admission](pod-security-admission.md)
- [Network Policy](network-policy.md)
- [RBAC](rbac.md)
- [Supply Chain Security](supply-chain-security.md)
- [Hardening](hardening.md)
- [KCSA](../certifications/kcsa.md)
