- Quando você está utilizando o `kubectl`você está interagindo o `kube-apiserver`.
- Quando uma requisição é criada, primeiro ela é autentica e validada pelo [[Admission Controllers]]
- É possível criar objetos utilizando o curl fazendo uma requisição para a api
	- usa o [[kubectl]]proxy e faz as requisições
- É o único componente que interage com o [[Kubernetes/nodes-components/etcD|etcd]]
- Todos os outros componentes vão fazer chamadas para o [[kube-apiserver]]

Para visualizar suas configurações
- Instalado pelo kubeadm `/etc/kubernetes/manifest/kube-apiserver.yaml`
- instalado na mão: `/etc/systemd/system/kube-apiserver.service`