# Checklists de Estudo por Certificação

Esta página consolida todos os checklists de estudo organizados por certificação e domínio do currículo oficial.

---

## CKS - Certified Kubernetes Security Specialist

> **Currículo**: v1.34 | **Pré-requisito**: CKA válido

### Cluster Setup (15%)

- [ ] Sei criar NetworkPolicies para restringir acesso → [NetworkPolicy](../security/network-policy.md)
- [ ] Sei usar kube-bench para CIS Benchmark → [CIS Benchmark](../security/cis-benchmark.md)
- [ ] Sei configurar Ingress com TLS → [Ingress Security](../security/ingress.md)
- [ ] Sei proteger metadata de nodes → [Hardening](../security/hardening.md)
- [ ] Sei verificar binários com sha256sum → [Verificando Binários](../security/verificando-binarios.md)

### Cluster Hardening (15%)

- [ ] Sei configurar RBAC com menor privilégio → [RBAC](../security/rbac.md)
- [ ] Sei gerenciar ServiceAccounts de forma segura → [ServiceAccount](../security/service-account.md)
- [ ] Sei restringir acesso ao API Server → [Hardening](../security/hardening.md)
- [ ] Sei fazer upgrade do cluster → [Cluster Upgrade](../maintenance/cluster-upgrade.md)

### System Hardening (10%)

- [ ] Sei minimizar superfície de ataque do host → [Hardening](../security/hardening.md)
- [ ] Sei configurar AppArmor em Pods → [AppArmor](../security/apparmor.md)
- [ ] Sei configurar Seccomp em Pods → [Seccomp](../security/seccomp.md)
- [ ] Sei usar RuntimeClasses → [Runtime Classes](../security/runtime-classes.md)

### Minimize Microservice Vulnerabilities (20%)

- [ ] Sei aplicar Pod Security Standards → [Pod Security Admission](../security/pod-security-admission.md)
- [ ] Sei gerenciar Secrets de forma segura → [Secrets](../configuration/secrets.md)
- [ ] Sei implementar multi-tenancy → [Multi Tenancy](../security/multi-tenancy.md)
- [ ] Sei configurar Pod-to-Pod encryption com Cilium → [Cilium](../security/cilium.md)
- [ ] Entendo isolation com sandboxed containers → [Runtime Classes](../security/runtime-classes.md)

### Supply Chain Security (20%)

- [ ] Sei minimizar base images → [Supply Chain](../security/supply-chain-security.md)
- [ ] Entendo SBOM e supply chain → [Supply Chain](../security/supply-chain-security.md)
- [ ] Sei configurar registries permitidos → [Admission Controllers](../security/admission-controllers.md)
- [ ] Sei assinar e validar imagens → [Supply Chain](../security/supply-chain-security.md)
- [ ] Sei usar ferramentas de análise estática (Trivy, KubeLinter) → [Aqua Security](../security/aqua-security.md)

### Monitoring, Logging and Runtime Security (20%)

- [ ] Sei configurar Kubernetes Audit → [Audit](../security/audit.md)
- [ ] Sei usar Falco para runtime security → [Falco](../security/falco.md)
- [ ] Sei detectar atividades maliciosas em runtime → [Monitoring Logging](../security/monitoring-logging.md)
- [ ] Sei garantir imutabilidade de containers → [Pod Security Admission](../security/pod-security-admission.md)
- [ ] Sei investigar fases de ataque → [Threat Model](../security/threat-model.md)

---

## CKA - Certified Kubernetes Administrator

> **Currículo**: v1.34

### Storage (10%)

- [ ] Sei criar e gerenciar PersistentVolumes → [Storage](../storage/storage.md)
- [ ] Sei criar e gerenciar PersistentVolumeClaims → [Storage](../storage/storage.md)
- [ ] Sei configurar StorageClasses → [Storage](../storage/storage.md)
- [ ] Entendo access modes (RWO, RWX, ROX) → [Storage](../storage/storage.md)
- [ ] Entendo reclaim policies (Retain, Delete) → [Storage](../storage/storage.md)

### Troubleshooting (30%) - CRÍTICO!

- [ ] Sei debugar clusters e nodes → [Troubleshooting](../maintenance/troubleshooting.md)
- [ ] Sei debugar componentes do control plane → [Troubleshooting](../maintenance/troubleshooting.md)
- [ ] Sei monitorar uso de recursos → [Monitoring](../observability/monitoring.md)
- [ ] Sei analisar logs de containers → [Troubleshooting](../maintenance/troubleshooting.md)
- [ ] Sei debugar problemas de networking → [Troubleshooting](../maintenance/troubleshooting.md)

### Workloads and Scheduling (15%)

- [ ] Sei criar e gerenciar Deployments → [Deployments](../workloads/deployment.md)
- [ ] Sei fazer rolling updates e rollbacks → [Deployments](../workloads/deployment.md)
- [ ] Sei usar ConfigMaps e Secrets → [ConfigMap](../configuration/configmap.md), [Secrets](../configuration/secrets.md)
- [ ] Sei configurar autoscaling (HPA) → [HPA](../workloads/horizontal-pod-autoscaler.md)
- [ ] Sei configurar node affinity e taints → [Scheduling](../workloads/scheduling.md)
- [ ] Entendo LimitRange e ResourceQuota → [LimitRange](../configuration/limit-range.md), [ResourceQuota](../configuration/resource-quota.md)

### Services and Networking (20%)

- [ ] Entendo conectividade entre Pods → [Networking](../networking/index.md)
- [ ] Sei criar e aplicar NetworkPolicies → [NetworkPolicy](../security/network-policy.md)
- [ ] Sei usar todos os tipos de Service → [Services](../networking/service.md)
- [ ] Sei configurar Ingress → [Ingress](../networking/ingress.md)
- [ ] Sei usar Gateway API → [Gateway API](../networking/gateway-api.md)
- [ ] Entendo CoreDNS → [DNS](../networking/dns.md)

### Cluster Architecture, Installation and Configuration (25%)

- [ ] Sei configurar RBAC → [RBAC](../security/rbac.md)
- [ ] Sei instalar cluster com kubeadm → [kubeadm](../tools/kubeadm.md)
- [ ] Sei fazer upgrade de cluster → [Cluster Upgrade](../maintenance/cluster-upgrade.md)
- [ ] Sei configurar cluster HA → [High Availability](../fundamentals/high-availability.md)
- [ ] Sei usar Helm e Kustomize → [Helm](../tools/helm.md), [Kustomize](../tools/kustomize.md)
- [ ] Entendo interfaces (CNI, CSI, CRI) → [Node Components](../cluster-components/node-components.md)
- [ ] Entendo CRDs e Operators → [CRDs e Operators](../api/crds-operators.md)

---

## CKAD - Certified Kubernetes Application Developer

> **Currículo**: v1.34

### Application Design and Build (20%)

- [ ] Sei criar e modificar container images → [Containers](../fundamentals/containers.md)
- [ ] Sei escolher o workload correto (Deployment, DaemonSet, Job, CronJob) → [Workloads](../workloads/pod.md)
- [ ] Entendo padrões multi-container (sidecar, init) → [Pods](../workloads/pod.md)
- [ ] Sei usar volumes persistentes e efêmeros → [Storage](../storage/storage.md)

### Application Deployment (20%)

- [ ] Sei implementar estratégias de deploy (blue/green, canary) → [Deployments](../workloads/deployment.md)
- [ ] Sei fazer rolling updates e rollbacks → [Deployments](../workloads/deployment.md)
- [ ] Sei usar Helm para deploy → [Helm](../tools/helm.md)
- [ ] Sei usar Kustomize → [Kustomize](../tools/kustomize.md)

### Application Environment, Configuration and Security (25%)

- [ ] Sei usar CRDs e Operators → [CRDs e Operators](../api/crds-operators.md)
- [ ] Entendo autenticação e autorização → [RBAC](../security/rbac.md)
- [ ] Sei configurar requests e limits → [ResourceQuota](../configuration/resource-quota.md)
- [ ] Sei usar ConfigMaps → [ConfigMap](../configuration/configmap.md)
- [ ] Sei usar Secrets → [Secrets](../configuration/secrets.md)
- [ ] Sei usar ServiceAccounts → [ServiceAccount](../security/service-account.md)
- [ ] Sei configurar SecurityContext → [Pod Security Admission](../security/pod-security-admission.md)

### Application Observability and Maintenance (15%)

- [ ] Entendo API deprecations → [API](../api/api.md)
- [ ] Sei configurar probes (liveness, readiness, startup) → [Probes](../workloads/probes.md)
- [ ] Sei usar kubectl para monitorar apps → [kubectl](../tools/kubectl.md)
- [ ] Sei analisar logs de containers → [Troubleshooting](../maintenance/troubleshooting.md)
- [ ] Sei debugar aplicações → [Troubleshooting](../maintenance/troubleshooting.md)

### Services and Networking (20%)

- [ ] Sei criar NetworkPolicies básicas → [NetworkPolicy](../security/network-policy.md)
- [ ] Sei expor aplicações via Services → [Services](../networking/service.md)
- [ ] Sei usar Ingress → [Ingress](../networking/ingress.md)

---

## KCSA - Kubernetes and Cloud Native Security Associate

> **Currículo**: 2024

### Overview of Cloud Native Security (14%)

- [ ] Entendo os 4Cs da segurança cloud native → [Os Quatro Cs](../security/os-quatro-cs.md)
- [ ] Entendo segurança de infraestrutura cloud → [Os Quatro Cs](../security/os-quatro-cs.md)
- [ ] Entendo técnicas de isolamento → [Multi Tenancy](../security/multi-tenancy.md)
- [ ] Entendo segurança de repositórios de artefatos → [Supply Chain](../security/supply-chain-security.md)

### Kubernetes Threat Model (16%)

- [ ] Entendo trust boundaries e data flow → [Threat Model](../security/threat-model.md)
- [ ] Entendo ataques de persistência → [Threat Model](../security/threat-model.md)
- [ ] Entendo DoS em Kubernetes → [Threat Model](../security/threat-model.md)
- [ ] Entendo execução de código malicioso → [Threat Model](../security/threat-model.md)
- [ ] Entendo privilege escalation → [Threat Model](../security/threat-model.md)

### Kubernetes Cluster Component Security (22%)

- [ ] Entendo segurança do API Server → [Hardening](../security/hardening.md)
- [ ] Entendo segurança do etcd → [etcd Security](../security/etcd.md)
- [ ] Entendo segurança do kubelet → [Hardening](../security/hardening.md)
- [ ] Entendo segurança de container runtime → [Runtime Classes](../security/runtime-classes.md)
- [ ] Entendo segurança de rede de containers → [NetworkPolicy](../security/network-policy.md)

### Kubernetes Security Fundamentals (22%)

- [ ] Entendo Pod Security Standards → [Pod Security Admission](../security/pod-security-admission.md)
- [ ] Entendo Pod Security Admission → [Pod Security Admission](../security/pod-security-admission.md)
- [ ] Entendo autenticação no Kubernetes → [RBAC](../security/rbac.md)
- [ ] Sei gerenciar Secrets → [Secrets](../configuration/secrets.md)
- [ ] Sei implementar isolamento com NetworkPolicy → [NetworkPolicy](../security/network-policy.md)
- [ ] Entendo Audit Logging → [Audit](../security/audit.md)

### Platform Security (16%)

- [ ] Entendo supply chain security → [Supply Chain](../security/supply-chain-security.md)
- [ ] Entendo segurança de image registry → [Supply Chain](../security/supply-chain-security.md)
- [ ] Entendo observabilidade para segurança → [Monitoring Logging](../security/monitoring-logging.md)
- [ ] Entendo PKI e certificados → [TLS](../security/tls.md)
- [ ] Entendo Admission Control → [Admission Controllers](../security/admission-controllers.md)

### Compliance and Security Frameworks (10%)

- [ ] Entendo frameworks de compliance → [Compliance](../security/compliance.md)
- [ ] Entendo threat modeling → [Threat Model](../security/threat-model.md)
- [ ] Entendo compliance de supply chain → [Supply Chain](../security/supply-chain-security.md)

---

## KCNA - Kubernetes and Cloud Native Associate

> **Currículo**: 2024

### Kubernetes Fundamentals (44%)

- [ ] Entendo conceitos core do Kubernetes → [Introdução](../introduction.md)
- [ ] Entendo administração básica → [kubectl](../tools/kubectl.md)
- [ ] Entendo scheduling → [Scheduling](../workloads/scheduling.md)
- [ ] Entendo containerização → [Containers](../fundamentals/containers.md)

### Container Orchestration (28%)

- [ ] Entendo observabilidade → [Observabilidade](../observability/observabilidade.md)
- [ ] Entendo networking básico → [Networking](../networking/index.md)
- [ ] Entendo conceitos de segurança → [Primitivos de Segurança](../security/primitivos-seguranca.md)
- [ ] Entendo troubleshooting básico → [Troubleshooting](../maintenance/troubleshooting.md)
- [ ] Entendo storage → [Storage](../storage/storage.md)

### Cloud Native Application Delivery (16%)

- [ ] Entendo entrega de aplicações → [Deployments](../workloads/deployment.md)
- [ ] Entendo debugging básico → [Troubleshooting](../maintenance/troubleshooting.md)

### Cloud Native Architecture (12%)

- [ ] Entendo o ecossistema CNCF → [Cloud Native](../fundamentals/cloud-native.md)
- [ ] Entendo princípios cloud native → [Cloud Native](../fundamentals/cloud-native.md)

---

## Legenda

- [ ] Item pendente de estudo
- [x] Item dominado

```admonish tip title="Dica de Estudo"
Marque os itens conforme for estudando. Foque primeiro nos domínios com maior peso na prova!
```
