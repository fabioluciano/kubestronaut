
* Deployments são recursos capazes de realizar a manipulação de pods e [[ReplicaSet]]. Configurando o estado desejado de um deployment ele permite de maneira controlada a implantação/alteração do estado atual do recurso para o estado desejado.
* Possui quase a mesma estrutura básica de um [[ReplicaSet]]
* Deployments utiliza apiVersion: apps/v1
* Controla e versiona [[ReplicaSet]], sempre criando um novo, quando houver modificações.
* `.spec.revisionHistoryLimit`, quantas versões serão guardadas no deploy
* É possível com o comando `kubectl rollout pause`, fazer com que modificações feitas no deployment, não sejam refletidas nos replicasets/pods. O comportamento normal do deployment pode ser retormado com `kubectl rollout resume`
* Existem duas estrategias de deploy(`.spec.strategy.type`), `Recreate` e `RollingUpdate`. O padrão é `RollingUpdate`.
	* `Recreate` - Vai apagar todos os [[Pods]] existentes substituindo pelos novos, quando modificado. Blue-green. Têm **downtime**
	* `RollingUpdate` - Define quantos pods estarão indisponíveis e quantos pods serão criados por vez. 
		* Caso haja um erro apresente erro durante o rollout, os pods não subirão se o maxUnavailable não estiver com 100%
		* Quando definido, é necessário também adicionar `.spec.strategy.rollingUpdate.maxSurge` e `.spec.strategy.rollingUpdate.maxUnavailable`
			* `.spec.strategy.rollingUpdate.maxSurge` - Máximo de pods que serão criados por vez. Pode ser um valor absoluto, ou um percentual;
			* `.spec.strategy.rollingUpdate.maxUnavailable` - Máximo de pods que podem ficar indisponíveis durante a atualização. Pode ser um valor absoluto, ou um percentual;


> [!NOTE]- `Deployment` example
```reference
filePath: "@/Attachments/Kubernetes/deployment/teste-deployment.yaml"
```


> [!NOTE]- `Deployement` with `spec.strategy = Recreate`
```reference
filePath: "@/Attachments/Kubernetes/deployment/deployment-strategy-recreate.yaml"
```


> [!NOTE]- `Deployement` with `spec.strategy = RollingUpdate`
```reference
filePath: "@/Attachments/Kubernetes/deployment/deployment-strategy-rollingupdate.yaml"
```


## Estratégias adicionais

### Blue/Green

- Existem diversas formas de implementar:
	- Usando Services
		- Acontece num nível mais baixo,
		- Os usuários podem notar a modificação
	- Usando Ingress
		-  Só funciona eh HTTP / HTTPS
- As duas versões da aplicação rodam em paralelo.
- É definida uma label para cada versão(blue/green)
- Existe um serviço que aponta para a bl;ue
- Dado que todos os testes da green foram feitos o mudo o seletor da blue para green


#### Service Based
```reference
filePath: "@/Attachments/Kubernetes/deployment/bluegreen-service-based.yaml"
```

#### Ingress Based
```reference
filePath: "@/Attachments/Kubernetes/deployment/bluegreen-ingress-based.yaml"
```

kodekloud/webapp-color:v1
### Canary
- Apenas uma fração das requisições é direcionada para a nova versão
- É criada uma label comum entre os dois deployments
- a service deixa de apontar para a v1, mas para essa nova label criada
- Diminui-se o número de replicas da nova versão 
- Assim  trafego será dividido entre a versão v1`e v2

#### Ingress Based

```reference
filePath: "@/Attachments/Kubernetes/deployment/canary-ingress-based.yaml"
```

#### Service Based

```reference
filePath: "@/Attachments/Kubernetes/deployment/canary-service-based.yaml"
```
## Comandos úteis
 
 > Recupera deployments dos nós
 > `kubectl get deployments`

> Recupera informações sobre o deployment
> `kubectl describe deployment deployment-name`

```shell title:"Criar template de deployment"
export kdry="--dry-run=client -o yaml"
kubectl create deployment nginx --image nginx --port 80 $kdry
```

### Salvar motivo de modificação de um deployment
```shell
kubectl (apply|replace) -f deployment meu deploy --record
```

### Aumentar o número de replicas de um replicationController
``` shell
kubectl scale --replicas NUMREPLICAS -f arquivodeployment.yaml
kubectl scale deployment deployment-teste --replicas NUMREPLICAS
```

```shell title:"Mostra todas as revisões de um deployment"
kubectl rollout history deploy meu-deploy
```


```shell title:"Mostra as moficações em uma determinada versão"
kubectl rollout history deploy meu-deploy --revision=REVNUMBER
```

```shell title:"Volta um deploy para uma revisão"
kubectl rollout undo deployment meu-deploy --to-revision NUMREVISION
```

```shell title:"Pausar e retomar modificações feitas em um deployment"
kubectl rollout pause deployment meu-deploy
kubectl rollout resume deployment meu-deploy
```

```shell title:"Cria um deployment"
kubectl create -f deployment-file-definition.yml
```

```shell title:"Deleta deployment"
kubectl delete deploy deployment-name
```