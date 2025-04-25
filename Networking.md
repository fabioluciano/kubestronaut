- O kubernetes cria duas redes criada por software
	- A primeira é a rede do cluster
		- Usada pelo cluster com o propósito de ser administrativa
	- A segunda é a rede dos pods 
		- Usada para anexar os pods a rede do kubernetes
		- Esses endereços de IP não podem ser acessados externamente
- Logo, para expor recursos para o mundo externo, é preciso criar [[Services]], que se conectam as duas redes possibilitando a exportação de valores

---

- O Kubelet consegue se comunicar somente com os pods de um determinado nó
- CNI - Gerencia os componentes de rede e segurança


## Tipos de comunicação
### Container para container

- Namespace IPC
- Containers de um pod compartilham o namespace de network. Logo, compartilham o mesmo IP/MAC adress


```shell title:"lista todos os namespaces do tipo pid"
sudo lsns -t pid
```

```shell title:"Recupera o namespace de rede utilizado por um processo"
sudo ip netns identify $PID 
```

```shell title:"Recupera todas as interfaces de rede criadas"
sudo ip netns exec $NETNS_NAME ip add
sudo ip netns exec $(sudo ip netns identify 11694) ip a
```


### Pod para pod

- Qulquer pod pode se conectar com qualquer outro pod, até que tenha uma [[NetworkPolicy]] ] impedindo a comunicação
- O tráfego entre Pods é feito utilizando um plugin. Calico

```shell
kubectl exec -ti container1 -- curl $CONTAINER2_IP
```


### Pod para Service
- O `/etc/resolv.conf` é gerado pelo [[kubelet]], quando está criando o pod
- Pra descobrir o endereço de IP de uma dada service, é só usar o `nslookup`no dado endereço do serviço `servicename.default.svc.cluster.local` . `servicename.default`
- Importante notar sobre [[Services#Endpoints]] e como eles são essenciais para debugar as services.
### Externo para Service

- São utilizados [[Ingress]] para que um serviço seja exposto ao mundo externo;
- Define regras que garantem que requisições SOMENTE http e https sejam roteadas para serviços dentro do cluster

```plantuml
"Cliente" -> "Ingress Resource"
"Ingress Resource" -> "Ingress Controller": Informa ao ingress controler que há \num novo grupo de regras que precisa ser configurada
"Ingress Resource" -> "Service"
"Service" -> "Pods"
``` 


## CNI

- As configurações da CNI utilizada está no diretório: `/etc/cni/net.d/`
 - Projeto liderado pela CNI para criação de especificações e bibliotecas para a construção de plugins de redes para o kubernetes
	 - Padronização
 - O Container Runtime vai chama o CNI para a criação de uma interface que será anexada ao pod
	 - O processo inverso é feito para remover uma interface de rede quando o pod é morto

```plantuml
"Kube API" -> "Kubelet": Fala com o Kubelet para \nque um novo pod seja criado
"Kubelet" -> "CRI": O Kubelet envia um comando\n de criação para o CRI
"CRI" -> "Network Namespace": O CRI cria um namespace de rede
"CRI" -> "CNI": Solicita a criação de uma interface de rede
"CNI" -> "Root Network Namespace": Envia o comando de criação de uma nova interface
"CNI" -> "CRI": Retorna a configuração para o CRI
"CNI" -> "POD": Cria o container no namespace do POD
``` 

## Security


## mTLS (Mutal TLS)
 - Tanto cliente quanto Servidor apresenta um certificado para ser validado
 - As duas partes têm que apresentar e validar um certificado emitido por uma autoridade certificadora
 - Toda a comunicação, tanto do cliente quanto do servidor é criptografada



---
[[Services]]
[[Ingress]]