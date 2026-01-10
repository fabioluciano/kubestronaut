![Logo](assets/logo.png)

# Kubestronaut - Guia de Estudos Kubernetes

Bem-vindo ao Kubestronaut, um guia completo de estudos sobre Kubernetes em português. Este guia foi desenvolvido para ajudar profissionais e entusiastas a dominarem os conceitos e práticas do Kubernetes, desde o básico até tópicos avançados.

## Certificações Kubernetes

Este guia cobre **todas as 5 certificações Kubernetes**:

| Certificação | Nível | Formato | Guia |
|--------------|-------|---------|------|
| **KCNA** | Entry-level | Múltipla escolha | [Guia KCNA](certifications/kcna.md) |
| **KCSA** | Entry-level | Múltipla escolha | [Guia KCSA](certifications/kcsa.md) |
| **CKAD** | Practitioner | Hands-on | [Guia CKAD](certifications/ckad.md) |
| **CKA** | Practitioner | Hands-on | [Guia CKA](certifications/cka.md) |
| **CKS** | Specialist | Hands-on | [Guia CKS](certifications/cks.md) |

## Início Rápido por Objetivo

### Entender Kubernetes (KCNA)
1. [Introdução](introduction.md) - Conceitos fundamentais
2. [Arquitetura](fundamentals/arquitetura.md) - Como o K8s funciona
3. [Cloud Native](fundamentals/cloud-native.md) - Ecossistema CNCF
4. [Containers](fundamentals/containers.md) - Docker e containerd

### Desenvolver Aplicações (CKAD)
1. [Pods](workloads/pod.md) - Unidade básica de deploy
2. [Deployments](workloads/deployment.md) - Gerenciar aplicações
3. [ConfigMaps](configuration/configmap.md) e [Secrets](configuration/secrets.md)
4. [Services](networking/service.md) e [Ingress](networking/ingress.md)

### Administrar Clusters (CKA)
1. [Componentes do Cluster](cluster-components/node-components.md)
2. [kubeadm](tools/kubeadm.md) - Criar e gerenciar clusters
3. [Troubleshooting](maintenance/troubleshooting.md) - 30% do exame CKA!
4. [Backup e Restore](maintenance/backup-e-restore.md)

### Segurança (CKS/KCSA)
1. [Os Quatro Cs](security/os-quatro-cs.md) - Cloud, Cluster, Container, Code
2. [RBAC](security/rbac.md) - Controle de acesso
3. [Network Policy](security/network-policy.md) - Segurança de rede
4. [Pod Security](security/pod-security-admission.md) - Hardening de pods

## Conteúdo do Guia

### Fundamentos
- [Introdução](introduction.md) - Conceitos e benefícios do K8s
- [Arquitetura](fundamentals/arquitetura.md) - Control plane e worker nodes
- [Cloud Native](fundamentals/cloud-native.md) - CNCF, 12-Factor, Microservices
- [Containers](fundamentals/containers.md) - OCI, runtime, imagens

### Workloads
- [Pods](workloads/pod.md) - Multi-container, init containers, probes
- [Deployments](workloads/deployment.md) - Rolling updates, rollbacks
- [StatefulSets](workloads/statefulset.md) - Apps stateful
- [DaemonSets](workloads/daemonset.md) - Um pod por node
- [Jobs e CronJobs](workloads/job.md) - Tarefas batch

### Configuração
- [ConfigMaps](configuration/configmap.md) - Configuração não sensível
- [Secrets](configuration/secrets.md) - Dados sensíveis
- [ResourceQuota](configuration/resource-quota.md) e [LimitRange](configuration/limit-range.md)

### Networking
- [Services](networking/service.md) - ClusterIP, NodePort, LoadBalancer
- [Ingress](networking/ingress.md) - HTTP/HTTPS routing
- [Network Policies](security/network-policy.md) - Firewall para pods
- [DNS](networking/dns.md) - Service discovery

### Segurança
- [RBAC](security/rbac.md) - Roles, ClusterRoles, Bindings
- [Pod Security](security/pod-security-admission.md) - Standards
- [Secrets Management](configuration/secrets.md) - Encryption at rest
- [Audit](security/audit.md) - Logging de ações

### Operações
- [kubectl](tools/kubectl.md) - CLI essencial
- [kubeadm](tools/kubeadm.md) - Gerenciamento de cluster
- [Troubleshooting](maintenance/troubleshooting.md) - Debug de problemas
- [Backup/Restore](maintenance/backup-e-restore.md) - etcd backup

### Ferramentas
- [Helm](tools/helm.md) - Package manager
- [Kustomize](tools/kustomize.md) - Customização de manifests
- [crictl](tools/crictl.md) - Debug de containers

## Estatísticas

| Métrica | Valor |
|---------|-------|
| Arquivos de conteúdo | 93 |
| Exemplos YAML | 420 |
| Diagramas PlantUML | 380+ |
| Páginas HTML | 95 |

## Código Fonte

Este guia é open source e está disponível no GitHub:

- Repositório: [github.com/fabioluciano/kubestronaut](https://github.com/fabioluciano/kubestronaut)
- Licença: MIT
- Contribuições são bem-vindas!

---

Navegue pelo sumário à esquerda para começar seus estudos. Bom aprendizado!
