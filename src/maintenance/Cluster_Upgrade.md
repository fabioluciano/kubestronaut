- os componentes do controlplane não precisam todos estarem na mesma versão
- porém nenhum outro componente pode estar acima da versão do [[kube-apiserver]]
- o [[kube-controller-manager]] e o [[kube-scheduler]] podem estar em uma versão abaixo
- o [[kubelet]] e o [[kube-proxy]] podem estar a duas versões abaixo
- o[[Kubectl]]pode estar a uma versão abaixo ou uma versão acima do [[kube-apiserver]]
- O suporte do kubernetes são somente para as três últimas versões lançadas
- Para fazer o upgrade é necessário subir uma minor por vez
- Primeiro se atualiza os controlplanes, depois os workernodes
	- durante a atualização, o [[kube-apiserver]] e o [[kube-scheduler]] ficarão fora por um tempo
	- TODAS as funcionalidades de manutenção serão paradas, porém, as aplicações nos worker nodes continuarão a funcionar
- O Kubeadm NÃO vai atualizar o kubelet



```plantuml
@startuml

skinparam defaultTextAlignment center

start

:Adiciona-se o repositório da nova \nversão a lista de repositórios\n disponíveis no sistema;
:Executa o comando\n\n ""apt-cache madison kubeadm"";\n\n para descrobrir qual a última versão\n disponível para atualização;
floating note left: Será apresentada uma lista\n de versões da ""minor"" selecionada.


partition #lightPink """kubeadm""" {
	:Descongela o pacote ""kubeadm""\n\n""apt-mark unhold kubeadm"";
	:Atualiza o pacote ""kubeadm""\n\n""apt upgrade -y kubeadm=$VERSION"";
	:Congela o pacote ""kubeadm""\n\n""apt-mark hold kubeadm"";
}

partition #lightGreen "Componentes do nó" {
	if (É o controlplane principal) then(controlplane principal)
		:Executa o comando para planejar a atualização\n\n""sudo kubeadm upgrade plan"";
		:Atualiza os componentes do controlplane\n\n""sudo kubeadm upgrade apply v1.x.x"";
		else (Controlplane secundário ou Worker)
		:Atualiza os componentes do controlplane\n\n""sudo kubeadm upgrade node"";
	endif
}

:Remove todos os pods do no e o coloca em manutenção\n\n""kubectl drain node --ignore-daemonsets"";

partition #lightSkyBlue """kubelet"""
	:Descongela o pacote ""kubelet""\n\n""apt-mark unhold kubelet"";
	:Atualiza o pacote ""kubelet""\n\n""apt upgrade -y kubelet=$VERSION"";
	:Congela o pacote ""kubelet""\n\n""apt-mark hold kubelet"";
	:Atualiza a lista de serviços\n\n""systemctl daemon-reload"";
	:Reinicia o ""kubelet""\n\n""systemctl restart kubelet"";
}

:Desmarca a manutenção do nó\n\n""kubectl uncordon node"";

stop

@enduml
```
