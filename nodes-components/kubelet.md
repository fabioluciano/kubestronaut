- Executa comando ordenados pelo [[kube-scheduler]]
- Regularmente informa ao apiserver o estado do nó
- Registra os nós no cluster
- Quando recebe a ordem de criar um container, vai chamar o CRI para baixar a imagem, e monitorar a saúde dos pods para o api server
- O kubelet não é instalado pelo kubeadm. Deve ser instalado manualmente

## Security

- As configurações são feitas utilizando o parametro --config, que carregará um arquivo do `kind` KubeletConfiguration
- O Kubelet serve duas portas:
	- 10250 - Serve a API habilitando acesso full
	- 10255 - Serve a API que permite requisições não atenticadas  readonly
		- Só estará disponbível se a opção read-only-port for configurada
- O kubeapi é um cliente do kubelet, e utiliza certificado/key para fazer a comunicação com o kubelet
- É necessário utilizar o authorization.mode para Webhook, para que o kubelet faça uma chamada ao kubeapi sever para determinar se a requisição é autorizada



```shell title:"Recupera a configuração do kubelet usada por um nó"
curl -X GET http://127.0.0.1:8001/api/v1/nodes/<node-name>/proxy/configz | jq .
```



PARA MODIFICAR AS CONFIGURACOES DOS KUBELETS DE NOVOS NOS, EH NECESSARIO MODIFICAR O CONFIGMAP `kubelet-config` no namespace `kube-system`

```shell
kubectl edit cm -n kube-system kubelet-config
```

DEPOIS DISSO... EH PRECISO RODAR O COMANDO KUBEADM NAS MAQUINAS PRA PODER ATUALIZAR AUTOMOTICAMENTE SEM PRECISAR EDITAR O ARQUIVO DE CONFIGURACAO

```shell
kubeadm upgrade node phase kubelet-config
```

RESTART DO KUBELET

```shell
systemctl restart kubelet
```