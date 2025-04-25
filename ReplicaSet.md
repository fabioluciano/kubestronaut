# ReplicaSet
- É um controller (Replication Controller);
- Garante que um determinado número de pods esteja rodando;
* ReplicaSet é um conjunto de pods que possibilita a execução e controle de réplicas. Visando garantir a disponibilidade de um número especificado/desejado de pods.

* ReplicaSet utiliza apiVersion: apps/v1


```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: teste
  labels:
    tier: "frontend"
spec:
  replicas: 10
  selector:
    matchLabels:
      tier: "frontend"
  template:
    metadata:
      name: replicase-teste
      labels:
        tier: "frontend"
    spec:
      containers:
        - image: nginx
          name: nginx
        - image: redis
          name: redis
```



- o `metadata.labels` devem bater com `spec.template.metadata.labels`
- pode-se utilizar dois tipos de seletores `matchLabels` e `matchExpressions`
	- `matchLabels`: 
	- `matchExpressions`: 
- Quando for criar um replicaset em que já existam pods com os seletores iguais, ele vai capturar os podes para o replicaset
- Não se pode atualizar informações do replicaset. É possível alterar o replicaset e manualmente matar os pods. Para ter atualização nesse nível, utilizase o [[Deployments]]
- Pode conter pods que não foram criados pelo `.spec.template`, mas que casam com `spec.selector`. Os pods criados fora do replicaset serão contabilizados na contagem de `spec.replicas`. `spec.template` é necessário neste cenário, ja que se um dos pods existentes morrer, ele têm que criar mais um para manter o [[Desired State]]



> [!NOTE]- Replication Controller
```reference
filePath: "@/Attachments/Kubernetes/replicaset/teste-replicationcontroller.yaml"
```



> [!NOTE]- Replicaset with `spec.selector.matchExpressions`
```reference
filePath: "@/Attachments/Kubernetes/replicaset/teste-replicaset-matchexpressions.yaml"
```



> [!NOTE]- Replicaset with `spec.selector.matchLabels`
```reference
filePath: "@/Attachments/Kubernetes/replicaset/teste-replicaset-matchlabels.yaml"
```


> [!NOTE]- Replicaset with `spec.selector.matchLabels` and existing pods
```reference
filePath: "@/Attachments/Kubernetes/replicaset/teste-replicaset-matchlabels-existing-pods.yaml"
```

## Comandos úteis
 
 > Recupera replicaset dos nós
 > `kubectl get replicaset`
 ou
  > `kubectl get rs`

> Recupera informações sobre todos os replicasets
> `kubectl describe replicaset`

> Recupera informações sobre um replicaset específico
> `kubectl describe replicaset name-replicaset`

> Cria replicaset
> `kubectl create -f replicaset-file-definition.yml`

> deleta replicaset
> `kubectl delete replicaset name-replicaset`

> escala o número de pods do replicaset
> `kubectl scale replicaset --replicas=5 name-replicaset`

