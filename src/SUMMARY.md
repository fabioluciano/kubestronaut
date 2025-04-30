# Summary

[Introdução](Introdução.md)

# Conceitos Básicos

- [Arquitetura](Arquitetura.md)
- [Containers](Containers.md)
    - [Docker](Docker.md)
    - [ContainerD](nodes-components/ContainerD.md)

# Componentes do Cluster

- [Cluster](Cluster.md)
    - [kubelet](nodes-components/kubelet.md)
    - [kube-proxy](nodes-components/kube-proxy.md)
- [Control Plane](nodes-components/nodes-components.md)
    - [kube-apiserver](nodes-components/kube-apiserver.md)
    - [kube-controller-manager](nodes-components/kube-controller-manager.md)
    - [kube-scheduler](nodes-components/kube-scheduler.md)
    - [etcD](nodes-components/etcD.md)

# Recursos do Kubernetes

- [API](API.md)
- [API Objects](ApiObjects.md)
- [Namespace](Namespace.md)
- [Pods](Pods.md)
    - [Static Pods](Static_Pods.md)
- [ReplicaSet](ReplicaSet.md)
- [Deployments](Deployments.md)
- [StatefulSet](StatefulSet.md)
- [DaemonSet](DaemonSet.md)
- [Job](Job.md)
- [CronJob](CronJob.md)
- [ConfigMap](ConfigMap.md)
- [Secrets](Secrets.md)
- [ResourceQuota](ResourceQuota.md)
- [LimitRange](LimitRange.md)
- [Networking](Networking.md)
    - [Services](Services.md)
    - [DNS](DNS.md)
    - [Endpoints](Endpoints.md)
    - [Gateway API](Gateway_API.md)

# Segurança

- [Security](Security/Security.md)
- [RBAC](Security/RBAC.md)
- [NetworkPolicy](Security/NetworkPolicy.md)
- [ServiceAccount](Security/ServiceAccount.md)
- [Pod Security Admission](Security/PodSecurityAdmission.md)
- [Open Policy Agent (OPA)](Security/OpenPolicyAgent.md)
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
- [Outros](Security/Misc.md)
    - [Os quatro Cs](Security/OsQuatroCs.md)
    - [Primitivos de Segurança](Security/PrimitivosSeguranca.md)
    - [Supply Chain Security](Security/SupplyChainSecurity.md)
    - [Multi Tenancy](Security/MultiTenancy.md)

# Operações
- [Instalação](maintenance/Install.md)
- [Cluster Upgrade](maintenance/Cluster_Upgrade.md)
- [OS Upgrade](maintenance/OS_Upgrade.md)
- [Backup e Restore](maintenance/Backup_e_Restore.md)
- [Alta Disponibilidade](High_Availability.md)
- [Observabilidade](Observabilidade.md)
    - [Monitoring](Monitoring.md)
  - [Troubleshooting](Troubleshooting.md)

# Ferramentas

- [kubectl](Kubectl.md)
- [kubeadm](kubeadm.md)
- [crictl](crictl.md)
- [Helm](Helm.md)
- [Kustomize](Kustomize.md)

# Extras

- [KCNA](KCNA.md)
- [Label](Label.md)
- [Metadata](Metadata.md)
- [Scheduling](Scheduling.md)
- [Horizontal Pod AutoScaler](HorizontalPodAutoScaler.md)
