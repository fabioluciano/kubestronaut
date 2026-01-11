# Sumário

[Página inicial](index.md)
[Atualizações](CHANGELOG.md)

# Fundamentos

- [Introdução](introduction.md)
- [Arquitetura](fundamentals/arquitetura.md)
- [Containers](fundamentals/containers.md)
  - [Docker](fundamentals/docker.md)
  - [containerd](cluster-components/containerd.md)
- [Metadata](fundamentals/metadata.md)
- [Namespaces](fundamentals/namespace.md)
- [Cluster](fundamentals/cluster.md)
- [Cloud Native](fundamentals/cloud-native.md)

# Componentes do Cluster

- [Componentes dos Nós](cluster-components/node-components.md)
  - [kubelet](cluster-components/kubelet.md)
  - [kube-proxy](cluster-components/kube-proxy.md)
  - [kube-apiserver](cluster-components/kube-apiserver.md)
  - [kube-controller-manager](cluster-components/kube-controller-manager.md)
  - [kube-scheduler](cluster-components/kube-scheduler.md)
  - [etcd](cluster-components/etcd.md)

# Objetos da API

- [API](api/api.md)
- [Objetos da API](api/api-objects.md)
- [CRDs e Operators](api/crds-operators.md)

# Workloads

- [Pods](workloads/pod.md)
- [Static Pods](workloads/static-pods.md)
- [ReplicaSet](workloads/replicaset.md)
- [Deployments](workloads/deployment.md)
- [StatefulSet](workloads/statefulset.md)
- [DaemonSet](workloads/daemonset.md)
- [Job](workloads/job.md)
- [CronJob](workloads/cronjob.md)
- [Scheduling](workloads/scheduling.md)
- [Probes (Health Checks)](workloads/probes.md)
- [Horizontal Pod AutoScaler](workloads/horizontal-pod-autoscaler.md)

# Configuração

- [ConfigMap](configuration/configmap.md)
- [Secrets](configuration/secrets.md)
- [ResourceQuota](configuration/resource-quota.md)
- [LimitRange](configuration/limit-range.md)

# Armazenamento

- [Storage](storage/storage.md)

# Rede

- [Networking](networking/index.md)
- [Services](networking/service.md)
- [DNS](networking/dns.md)
- [Endpoints](networking/endpoint.md)
- [Gateway API](networking/gateway-api.md)
- [Ingress](networking/ingress.md)
- [Service Mesh](networking/service-mesh.md)

# Segurança

- [Os Quatro Cs](security/os-quatro-cs.md)
- [Threat Model](security/threat-model.md)
- [Compliance](security/compliance.md)
- [Primitivos de Segurança](security/primitivos-seguranca.md)
- [RBAC](security/rbac.md)
- [ServiceAccount](security/service-account.md)
- [NetworkPolicy](security/network-policy.md)
- [Pod Security Admission](security/pod-security-admission.md)
- [Admission Controllers](security/admission-controllers.md)
- [OPA - Open Policy Agent](security/open-policy-agent.md)
- [Certificados e TLS](security/tls.md)
  - [Certificate API](security/certificate-api.md)
  - [mTLS](security/mtls.md)
- [Hardening](security/hardening.md)
  - [CIS Benchmark](security/cis-benchmark.md)
  - [AppArmor](security/apparmor.md)
  - [Seccomp](security/seccomp.md)
  - [Runtime Classes](security/runtime-classes.md)
- [Auditoria](security/audit.md)
- [Falco (Runtime Security)](security/falco.md)
- [Monitoring e Logging](security/monitoring-logging.md)
- [Multi Tenancy](security/multi-tenancy.md)
- [Supply Chain Security](security/supply-chain-security.md)
- [Cilium](security/cilium.md)
- [Aqua Security](security/aqua-security.md)
- [etcd Security](security/etcd.md)
- [etcdctl](security/etcdctl.md)
- [Ingress Security](security/ingress.md)
- [Verificando Binários](security/verificando-binarios.md)
- [Minimizar Acesso GUI](security/minimizar-acesso-gui.md)
- [Misc](security/misc.md)

# Operações e Manutenção

- [Instalação](maintenance/install.md)
- [Atualização do Cluster](maintenance/cluster-upgrade.md)
- [Atualização do SO](maintenance/os-upgrade.md)
- [Backup e Restore](maintenance/backup-e-restore.md)
- [Alta Disponibilidade](fundamentals/high-availability.md)
- [Troubleshooting](maintenance/troubleshooting.md)

# Observabilidade

- [Monitoring](observability/monitoring.md)
- [Observabilidade Geral](observability/observabilidade.md)

# Ferramentas

- [kubectl](tools/kubectl.md)
- [kubeadm](tools/kubeadm.md)
- [crictl](tools/crictl.md)
- [Helm](tools/helm.md)
- [Kustomize](tools/kustomize.md)
- [GitOps (ArgoCD/Flux)](tools/gitops.md)

# Certificações

- [Checklists de Estudo](certifications/checklists.md)
- [KCNA](certifications/kcna.md)
- [KCSA](certifications/kcsa.md)
- [CKAD](certifications/ckad.md)
- [CKA](certifications/cka.md)
- [CKS](certifications/cks.md)

# Outros

- [Apresentação](apresentacao.md)
- [Configuração do vim](meta.md)
- [Misc](misc.md)
