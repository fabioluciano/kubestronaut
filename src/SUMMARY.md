# Sumário

[Página inicial](index.md)
[Atualizações](CHANGELOG.md)

# Fundamentos
- [Introdução](introduction.md)
- [Arquitetura](Arquitetura.md)
- [Containers](Containers.md)
  - [Docker](Docker.md)
  - [containerd](nodes-components/ContainerD.md)
- [Metadata](Metadata.md)
- [Namespaces](Namespace.md)
- [Cluster](Cluster.md)

# Componentes do Cluster

## Nós (Nodes)
  - [kubelet](nodes-components/kubelet.md)
  - [kube-proxy](nodes-components/kube-proxy.md)

## Control Plane
  - [kube-apiserver](nodes-components/kube-apiserver.md)
  - [kube-controller-manager](nodes-components/kube-controller-manager.md)
  - [kube-scheduler](nodes-components/kube-scheduler.md)
  - [etcd](nodes-components/etcD.md)

# Objetos da API

- [API](API.md)
- [Objetos da API](ApiObjects.md)

# Workloads

- [Pods](Pods.md)
  - [Static Pods](Static_Pods.md)
- [ReplicaSet](ReplicaSet.md)
- [Deployments](Deployments.md)
- [StatefulSet](StatefulSet.md)
- [DaemonSet](DaemonSet.md)
- [Job](Job.md)
- [CronJob](CronJob.md)
- [Scheduling](Scheduling.md)
- [Horizontal Pod AutoScaler](HorizontalPodAutoScaler.md)

# Configuração

- [ConfigMap](ConfigMap.md)
- [Secrets](Secrets.md)
- [ResourceQuota](ResourceQuota.md)
- [LimitRange](LimitRange.md)

# Rede

- [Networking](Networking.md)
  - [Services](Services.md)
  - [DNS](DNS.md)
  - [Endpoints](Endpoints.md)
  - [Gateway API](Gateway_API.md)

# Segurança

- [RBAC](Security/RBAC.md)
- [ServiceAccount](Security/ServiceAccount.md)
- [NetworkPolicy](Security/NetworkPolicy.md)
- [Pod Security Admission](Security/Pod_Security_Admission.md)
- [OPA - Open Policy Agent](Security/Open_Policy_Agent.md)
- [Certificados e TLS](Security/TLS.md)
  - [Certificate API](Security/Certificate_API.md)
  - [mTLS](Security/mTLS.md)
- [Hardening](Security/Hardening.md)
  - [CIS Benchmark](Security/CIS_Benchmark.md)
  - [AppArmor](Security/AppArmor.md)
  - [Seccomp](Security/Seccomp.md)
  - [Runtime Classes](Security/Runtime-Classes.md)
- [Auditoria e Monitoramento](Security/Monitoring_Logging.md)
  - [Audit](Security/Audit.md)
  - [Minimizar acesso ao GUI](Security/Minimizar_Acesso_GUI.md)
- [Conceitos Complementares](Security/Misc.md)
  - [Os Quatro Cs](Security/Os_Quatro_Cs.md)
  - [Primitivos de Segurança](Security/Primitivos_Seguranca.md)
  - [Supply Chain Security](Security/Supply_Chain_Security.md)
  - [Multi Tenancy](Security/Multi_Tenancy.md)

# Operações

- [Instalação](maintenance/Install.md)
- [Atualização do Cluster](maintenance/Cluster_Upgrade.md)
- [Atualização do SO](maintenance/OS_Upgrade.md)
- [Backup e Restore](maintenance/Backup_e_Restore.md)
- [Alta Disponibilidade](High_Availability.md)
- [Troubleshooting](maintenance/Troubleshooting.md)

# Observabilidade

- [Monitoring](Monitoring.md)
- [Observabilidade Geral](Observabilidade.md)

# Ferramentas

- [kubectl](Kubectl.md)
- [kubeadm](kubeadm.md)
- [crictl](crictl.md)
- [Helm](Helm.md)
- [Kustomize](Kustomize.md)
- [Configuração do vim](META.md)

# Outros Tópicos

- [KCNA](KCNA.md)
