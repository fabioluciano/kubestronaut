* É um componente utilizado para fazer com que os pods sejam acessíveis ao mundo externo, ou mesmo dentro do cluster
* Aplica o load balancing round-robin, direcionando para os pods
	* As requisições são "mais ou menos" divididas entre os pods
- Cada Service recebe um nome acessível em `NOMEDASERVICE.NAMESPACE.svc`
* Existem 3 tipos de services:
	- `service.spec.type = ClusterIP`: Torna o serviço acessível apenas dentro do cluster. É o `serviceType` padrão.
		- Existe uma faixa de ips para os pods e outra para os serviços
		- É criado um ip virtual para que o serviço seja acessível dentro do CLuster
	- HEADLESS SERVICE`service.spec.type = ClusterIP`, `service.spec.ClusterIP = None` 
		- Vai usar os IPS dos pods e não o IP a service... Já que ela nem tem
		- PESQUISAR MAIs
	- `service.spec.type = NodePort`: Torna o serviço acessível ao mundo externo, colocando uma porta anexada a um nó `NodeIP:NodePort`. Também possui um `ClusterIp`.
		- A porta, se não setada, é automaticamente  preenchida.
		- A porta deve estar entre 30000 e 32767
		- Qualquer nó responderá pela porta
		- Quando há multiplas portas sendo expostas, é necessário informar o name
	- `service.spec.type = LoadBalancer`:
		- É necessário um agente externo para seu funcionamento. Possui um `NodePort` e um `ClusterIp`
	- `service.spec.type = ExternalName`
		- Cria um `CNAME` dns registry para algo que está fora do cluster
- Endpoints são para quantos pods o trafego está sendo direcionado com determinado serviço
- Quando um serviço é criado, um registro`A/AAAA` e um `SRV` é gerado no coredns

As informações da service utilizada pelo pod podem ser visualizadas também pelas variáveis de ambiente definidas. Só serão disponibilizadas em pods que estejam rodando no mesmo namespace

```shell
export # executar commando

#### SAIDA

### SERVICENAME_SERVICE_HOST
export TESTE_SERVICE_HOST='10.109.105.76'
export TESTE_SERVICE_PORT='80'
```

Vai mostrar 


> [!NOTE]- Criação de uma `Secret`
```reference
filePath: "@/Attachments/Kubernetes/service/deploy-service-nodeip.yaml"
```


> [!NOTE]- Service para um Pod utilizando `spec.type.ClusterIP`
```reference
filePath: "@/Attachments/Kubernetes/service/service-clusterip.yaml"
```


> [!NOTE]- Service para um Pod utilizando `spec.type.NodePort`
```reference
filePath: "@/Attachments/Kubernetes/service/service-nodeport.yaml"
```
## Comandos úteis

```shell title:"Recupera o Range de IP utilizado pelos serviços"
kubectl cluster-info dump | grep service-cluster-ip-range
```

```shell title:"Recupera o CIDR utilizado pelo cluster para alocar aos pods"
kubectl cluster-info dump | grep cluster-cidr
```

```shell
kubectl expose pod service-test-nodeport --port 8080 --target-port 80 --selector svcType=NodePort
```
 > Cria service
> `kubectl create -f service-file-definition.yml`

 > Recupera informações sobre o service
 > `kubectl get svc`

> Deleta service
> `kubectl delete svc name-service`

```shell
kubectl run -ti --rm testpod --image nginx -- cat /etc/resolv.conf
```


## Endpoints
- Coleção de Ips e portas expostas pelos pods selecionados pelo pod
- Todas vez que um pod é removido ou adicionado ao seletor, o endpoint é atualizado
- Só podem ter 1000 ips dentro de um endpoint. ou seja, não pode ter mais de 1000 replicas rodando...
- Foi criado o EndpointSlice para resolver os problemas dos endpoints. Ele também guarda informação do nó