# Kubernetes Threat Model

```admonish info title="Certificações"
KCSA (16%), CKS (10%)
```

## Conceitos Fundamentais

### O que é Threat Modeling?

Threat Modeling é o processo de identificar potenciais ameaças e vulnerabilidades em um sistema, avaliar riscos e definir contramedidas.

```plantuml,format=png
!include ../assets/diagrams/security/threat-model-processo-de-threat-modeling-1.puml
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
!include ../assets/diagrams/security/threat-model-stride-framework-1.puml
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
!include ../assets/diagrams/security/threat-model-attack-surfaces-1.puml
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
!include ../assets/diagrams/security/threat-model-threat-actors-1.puml
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
!include ../assets/diagrams/security/threat-model-container-compromise-1.puml
```

### Scenario 2: Supply Chain Attack

```plantuml,format=png
!include ../assets/diagrams/security/threat-model-supply-chain-attack-1.puml
```

### Scenario 3: Lateral Movement

```plantuml,format=png
!include ../assets/diagrams/security/threat-model-lateral-movement-1.puml
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
!include ../assets/diagrams/security/threat-model-defense-in-depth-1.puml
```

### Zero Trust Principles

1. **Never trust, always verify** - Autenticação em todas as camadas
2. **Least privilege** - Mínimo de permissões necessárias
3. **Assume breach** - Planejar para quando (não se) houver comprometimento
4. **Verify explicitly** - Validar todas as requests

---

## Dicas para o Exame

```plantuml,format=png
!include ../assets/diagrams/security/threat-model-dicas-threat-model-1.puml
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
