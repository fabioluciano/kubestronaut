# Sumário

[Introdução](Introdução.md)

# Fundamentos

- [Arquitetura](Arquitetura.md)
- [Containers](Containers.md)
  - [Docker](Docker.md)
  - [containerd](nodes-components/ContainerD.md)
- [Labels](Label.md)
- [Metadata](Metadata.md)
- [Namespaces](Namespace.md)

# Componentes do Cluster

## Nós (Nodes)
- [Cluster](Cluster.md)
  - [kubelet](nodes-components/kubelet.md)
  - [kube-proxy](nodes-components/kube-proxy.md)

## Control Plane
- [Control Plane](nodes-components/nodes-components.md)
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

- [Visão Geral](Security/Security.md)
- [RBAC](Security/RBAC.md)
- [ServiceAccount](Security/ServiceAccount.md)
- [NetworkPolicy](Security/NetworkPolicy.md)
- [Pod Security Admission](Security/PodSecurityAdmission.md)
- [OPA - Open Policy Agent](Security/OpenPolicyAgent.md)
- [Certificados e TLS](Security/TLS.md)
  - [Certificate API](Security/CertificateAPI.md)
  - [mTLS](Security/mTLS.md)
- [Hardening](Security/Hardening.md)
  - [CIS Benchmark](Security/CisBenchmark.md)
  - [AppArmor](Security/AppArmor.md)
  - [Seccomp](Security/Seccomp.md)
  - [Runtime Classes](Security/RuntimeClasses.md)
- [Auditoria e Monitoramento](Security/MonitoringLogging.md)
  - [Audit](Security/Audit.md)
  - [Minimizar acesso ao GUI](Security/MinimizarAcessoGUI.md)
- [Conceitos Complementares](Security/Misc.md)
  - [Os Quatro Cs](Security/OsQuatroCs.md)
  - [Primitivos de Segurança](Security/PrimitivosSeguranca.md)
  - [Supply Chain Security](Security/SupplyChainSecurity.md)
  - [Multi Tenancy](Security/MultiTenancy.md)

# Operações

- [Instalação](maintenance/Install.md)
- [Atualização do Cluster](maintenance/Cluster_Upgrade.md)
- [Atualização do SO](maintenance/OS_Upgrade.md)
- [Backup e Restore](maintenance/Backup_e_Restore.md)
- [Alta Disponibilidade](High_Availability.md)
- [Troubleshooting](Troubleshooting.md)

# Observabilidade

- [Monitoring](Monitoring.md)
- [Observabilidade Geral](Observabilidade.md)

# Ferramentas

- [kubectl](Kubectl.md)
- [kubeadm](kubeadm.md)
- [crictl](crictl.md)
- [Helm](Helm.md)
- [Kustomize](Kustomize.md)

# Outros Tópicos

- [KCNA](KCNA.md)