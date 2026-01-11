# Pod Security Admission (PSA)

## Conceitos Fundamentais

### O que é Pod Security Admission?

Pod Security Admission (PSA) é o mecanismo nativo do Kubernetes para aplicar padrões de segurança a Pods. Substituiu o deprecated PodSecurityPolicy (PSP) a partir do Kubernetes 1.25.

```plantuml,format=png
@startuml
skinparam monochrome true

title POD SECURITY ADMISSION

actor User
entity "kubectl apply -f pod.yaml" as kubectl
entity "API Server" as api
entity "Admission Controllers" as admission
rectangle "Pod Security Admission" as psa {
  note as ns
    **Namespace: production**
    Labels:
      pod-security.kubernetes.io/enforce: restricted
      pod-security.kubernetes.io/warn: restricted
  end note
}

User -> kubectl
kubectl -> api
api -> admission
admission -> psa

psa --> [✓ ALLOW] : Pod não viola política
psa --> [✗ DENY] : Pod viola política
@enduml
```

### Pod Security Standards

```plantuml,format=png
@startuml
skinparam monochrome true

title SECURITY LEVELS

rectangle "PRIVILEGED" as priv {
  note as n1
    • Sem restrições
    • Permite qualquer configuração
    • Use apenas quando necessário (kube-system)
  end note
}

rectangle "BASELINE" as base {
  note as n2
    • Previne escalação de privilégios conhecida
    • Permite a maioria das cargas de trabalho
    • Bloqueia: privileged, hostPID, hostNetwork...
  end note
}

rectangle "RESTRICTED" as rest {
  note as n3
    • Hardening máximo
    • Segue melhores práticas
    • Requer: runAsNonRoot, drop ALL capabilities...
  end note
}

priv -[hidden]down-> base : Menos Restritivo
base -[hidden]down-> rest : Mais Restritivo

note left of priv
  **Menos Restritivo**
  ↑
end note

note left of rest
  ↓
  **Mais Restritivo**
end note
@enduml
```

### Modos de Operação

| Modo | Comportamento |
|------|---------------|
| **enforce** | Rejeita Pods que violam a política |
| **audit** | Registra violações no audit log, mas permite |
| **warn** | Mostra warning ao usuário, mas permite |

---

## Configuração por Namespace

### Via Labels

PSA é configurado através de **labels** no namespace (não annotations!).

```bash
# Formato das labels
pod-security.kubernetes.io/<MODE>: <LEVEL>
pod-security.kubernetes.io/<MODE>-version: <VERSION>
```

### Aplicar via kubectl

```bash
# Enforce baseline
kubectl label namespace production pod-security.kubernetes.io/enforce=baseline

# Warn + Audit restricted
kubectl label namespace production pod-security.kubernetes.io/warn=restricted
kubectl label namespace production pod-security.kubernetes.io/audit=restricted

# Especificar versão
kubectl label namespace production pod-security.kubernetes.io/enforce-version=v1.28

# Remover label
kubectl label namespace production pod-security.kubernetes.io/enforce-

# Ver labels do namespace
kubectl get namespace production --show-labels
```

### Exemplo Completo de Namespace

```yaml
{{#include ../assets/security/psa/namespace-production.yaml}}
```

---

## Pod Security Standards em Detalhes

### Privileged

Sem restrições - permite qualquer configuração.

```yaml
{{#include ../assets/security/psa/privileged-pod.yaml}}
```

### Baseline

Bloqueia escalação de privilégios conhecida.

```plantuml,format=png
@startuml
skinparam monochrome true

map "BASELINE - RESTRIÇÕES" as baseline {
}

note bottom of baseline
  **❌ BLOQUEADO:**
  • spec.hostNetwork: true
  • spec.hostPID: true
  • spec.hostIPC: true
  • spec.containers[*].securityContext.privileged: true
  • spec.containers[*].securityContext.capabilities.add:
    - NET_RAW (exceto se explicitamente permitido)
  • spec.containers[*].securityContext.procMount != Default
  • spec.volumes[*].hostPath
  • spec.containers[*].ports[*].hostPort

  **✅ PERMITIDO:**
  • runAsRoot (container pode rodar como root)
  • Capabilities padrão mantidas
  • Volumes normais (emptyDir, PVC, etc)
end note
@enduml
```

### Restricted

Hardening máximo seguindo melhores práticas.

```plantuml,format=png
@startuml
skinparam monochrome true

map "RESTRICTED - RESTRIÇÕES" as restricted {
}

note bottom of restricted
  **❌ Tudo do Baseline, MAIS:**

  **OBRIGATÓRIO:**
  • runAsNonRoot: true
  • allowPrivilegeEscalation: false
  • seccompProfile.type: RuntimeDefault OU Localhost
  • capabilities.drop: ["ALL"]

  **BLOQUEADO:**
  • runAsUser: 0 (root)
  • Qualquer capability (exceto NET_BIND_SERVICE)
end note
@enduml
```

### Pod Compliant com Restricted

```yaml
{{#include ../assets/security/psa/restricted-compliant.yaml}}
```

---

## Configuração Global (Cluster-wide)

### Via AdmissionConfiguration

Para definir padrões no cluster inteiro, configure o kube-apiserver.

```yaml
{{#include ../assets/security/psa/admission-configuration.yaml}}
```

### Configurar no kube-apiserver

```yaml
{{#include ../assets/security/psa/kube-apiserver-psa.yaml}}
```

---

## Exemptions (Isenções)

### Tipos de Exemptions

```yaml
{{#include ../assets/security/psa/exemptions.yaml}}
```

---

## Comandos Úteis

### Verificar PSA no Cluster

```bash
# Verificar se PSA está habilitado
kubectl exec -n kube-system kube-apiserver-<node> -- \
  kube-apiserver -h | grep enable-admission

# Listar namespaces com PSA configurado
kubectl get namespaces -o custom-columns=\
'NAME:.metadata.name,ENFORCE:.metadata.labels.pod-security\.kubernetes\.io/enforce,WARN:.metadata.labels.pod-security\.kubernetes\.io/warn'
```

### Testar Antes de Aplicar

```bash
# Dry-run com validação PSA
kubectl apply -f pod.yaml --dry-run=server

# Ver warning sem criar
kubectl create -f pod.yaml --dry-run=server
```

### Ver Audit Logs

```bash
# Violações aparecem no audit log do API server
# Procure por eventos com:
# annotations:
#   pod-security.kubernetes.io/audit-violations: ...
```

---

## Exemplos Práticos

### Exemplo 1: Namespace Seguro para Produção

```yaml
{{#include ../assets/security/psa/namespace-restricted.yaml}}
```

```bash
# Criar namespace
kubectl apply -f namespace.yaml

# Tentar criar pod não-compliant
kubectl run test --image=nginx -n production
# Error: pods "test" is forbidden: violates PodSecurity "restricted:v1.28"
```

### Exemplo 2: Migração Gradual

```yaml
{{#include ../assets/security/psa/namespace-migration.yaml}}
```

### Exemplo 3: Deployment Compliant

```yaml
{{#include ../assets/security/psa/secure-deployment.yaml}}
```

---

## Troubleshooting

### Pod Rejeitado

```bash
# Erro típico
Error from server (Forbidden): error when creating "pod.yaml": 
pods "test" is forbidden: violates PodSecurity "restricted:latest": 
allowPrivilegeEscalation != false (container "app" must set 
securityContext.allowPrivilegeEscalation=false), 
runAsNonRoot != true (pod or container "app" must set 
securityContext.runAsNonRoot=true)

# Solução: Adicionar campos requeridos
spec:
  securityContext:
    runAsNonRoot: true
  containers:
  - securityContext:
      allowPrivilegeEscalation: false
```

### Verificar Violações Existentes

```bash
# Ver warnings ao descrever namespace
kubectl describe namespace production

# Ver eventos relacionados a PSA
kubectl get events --field-selector reason=FailedCreate -A
```

---

## PSA vs PodSecurityPolicy vs OPA

```plantuml,format=png
@startuml
skinparam monochrome true

map "COMPARAÇÃO" as comp {
}

note bottom of comp
  **Pod Security Admission (PSA):**
  ✅ Nativo do Kubernetes (1.25+)
  ✅ Simples (3 níveis predefinidos)
  ✅ Configurado via labels no namespace
  ❌ Pouca flexibilidade/customização
  ❌ Apenas para Pods

  **PodSecurityPolicy (PSP): DEPRECATED**
  ❌ Removido no Kubernetes 1.25
  ❌ Complexo de configurar

  **OPA Gatekeeper / Kyverno:**
  ✅ Altamente customizável
  ✅ Qualquer recurso Kubernetes
  ✅ Políticas granulares
  ❌ Mais complexo de implementar
  ❌ Componente adicional no cluster
end note
@enduml
```

---

## Dicas para o Exame CKS

```plantuml,format=png
@startuml
skinparam monochrome true

map "DICAS CKS - PSA" as dicas {
}

note bottom of dicas
  **Labels (não annotations!):**
  pod-security.kubernetes.io/enforce: <level>
  pod-security.kubernetes.io/warn: <level>
  pod-security.kubernetes.io/audit: <level>

  **Levels:**
  • privileged - sem restrições
  • baseline - bloqueia escalação
  • restricted - hardening máximo

  **Modes:**
  • enforce - bloqueia
  • warn - avisa
  • audit - registra

  **Restricted requer:**
  • runAsNonRoot: true
  • allowPrivilegeEscalation: false
  • capabilities.drop: ["ALL"]
  • seccompProfile.type: RuntimeDefault

  **Comando rápido:**
  kubectl label ns NAME pod-security.kubernetes.io/enforce=X
end note
@enduml
```

---

## Referências

- [AppArmor](apparmor.md)
- [Seccomp](seccomp.md)
- [Open Policy Agent](open-policy-agent.md)
- [Hardening](hardening.md)
- [Pod](../workloads/pod.md)
