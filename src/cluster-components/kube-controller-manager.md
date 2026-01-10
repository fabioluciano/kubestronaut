# kube-controller-manager

- Observa o estado dos recursos
- toma medidas para remediar situações específicas. atingir o [[Desired State]]
- São os cérebros do cluster

Tipos:
	- Node controller - Toma de conta dos controllers
		- Monitora Informa a cada 5 segundos
		- Grace period: 40 . SE o pod ficar unreachable por ... ele ...
		- Eviction: 5 minutos
	- Replication Controller - Toma de conta de [[ReplicaSet]]

Para visualizar suas configurações
- Instalado pelo kubeadm `/etc/kubernetes/manifest/kube-controller-manager.yaml`
- instalado na mão: `/etc/systemd/system/kube-controller-manager.service`