## Selecionando nós

### Utilizando o Taints e `spec.tolerations`


> [!danger] 
>  PARA GARANTIR QUE UM POD SEJA ALOCADO EM UM NÓ É NECESSÁRIO CONFIGURAR TANTO A `TOLERATION`QUANTO O `NODESELECTOR`
>A TOLERATION GARANTE QUE O POD TENHA A TOLERANCIA AO TAINT DEFINIDO NO NÓ, E O NODESELECTOR GARANTE QUE O POD SEJA ADICIONADO A UM NÓ QUE TENHA OS LABELS DEFINIDOS

- Define uma relação entre pods e nodes, restringindo quais pods pertencem a quais nós
- Define quais pods são scheduled em um pod
- Taints são restrições anexadas a um nó
- Tolerations são anexadas a um pod
- Por padrão, nós não possuem taints, e pods não possuem tolerations
- O efeito é o que acontecerá com os pods que não tiverem essa tolerância
- Não há garantia de que um pod vá para um nó em particular, mesmo com a tolerância aplicada;
- Caso seja um pod sem um replication controller, ele será simplesmente apagado :)
- Tipos de efeitos de taint:
	- `NoSchedule`: Os pods que não tiverem essa tolerância não serão alocados a este pod.
	- `PreferNoSchedule`:  O Scheduler vai tentar não alocar um pod no nó, mas não é garantido
	- `NoExecute`: Os pods que não tiverem essa tolerância não serão alocados a este pod. Se existirem pods existentes no nó, serão migrados.

```shell
kubectl taint nodes node-name key=VALUE:TAINT-EFFECT
kubectl taint nodes node-name app=blue:NoSchedule
```

Para remover um taint basta adicionar um sinal de `-`

```shell
kubectl taint nodes node-name app=blue:NoSchedule-
```


> [!NOTE]- `Pod` with tolerations
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-with-toleration.yaml"
```



### Utilizando o `spec.nodeSelector`
- Aloca um pod a um nó baseado em labels anexadas ao nó
- Não têm `matchLabels` ou `matchExpressions`. Para usar esse tipo de lógica deve-ser usar o `nodeAffinity`

```shell title:"Adicionando uma label a um node"
kubectl label nodes minikube-m04 disk=nvme
```

> [!NOTE]- `Pod` with `spec.nodeSelector`
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-with-nodeselector.yaml"
```

```shell
kubectl label nodes node-name LABEL=VALUE
```

Para remover um tente basta adicionar um sinal de `-`

```shell
kubectl label nodes node-name LABEL-
```

### Utilizando o `spec.affinity`
- Garante que nós serão alocados em determinados nodes.
- Caso haja mudanças nas affinities, e o `spec.strategy`de um deployment esteja como `RollingRelease`, ainda ficarão pods esperando caso não seja configurado o maxUnavailable para 100%.

#### Utilizando o `spec.affinity.nodeAffinity`

- `spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution`: Quer dizer que o pod precisa que exista um nó com essa label. Caso não exista, o pod não será alocado. Quer dizer que o pod precisa que exista um nó com as condições especificadas em `matchExpression`
- `spec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution`: Ele vai tentar colocar o pod em um nó com a afinnity definida, porem alocará em qualquer lugar, se não conseguir. Com o weight, você pode definir a ordem que ele tentará alocar.

`IgnoreDuringExecution` significa que pods que não serão afetados, caso as labels dos nodes mudem após os pods serem atribuídos ao nó.

#### Utilizando o `spec.affinity.podAffinity`
- define uma relação do pod sendo criado com outros pods presentes no nó
- topologykey será a chave utilizada para filtrar os nós que contenham aquela label

#### Utilizando o `spec.affinity.podAntiAffinity`
- define uma relação do pod sendo criado com outros pods presentes no no 

### Utilizando o `spec.nodeName`

- Se voce não selecionar, o scheduler vai selecionar por voce
- Só pode ser adicionada na criação do Pod. Não é possível editar


```reference
filePath: "@/Attachments/Kubernetes/pod/deploy-with-nodeaffinity-required.yaml"
```


```reference
filePath: "@/Attachments/Kubernetes/pod/deploy-with-nodeaffinity-preferred.yaml"
```

### Taints and Tolerations - x nodeAffinity
- Com taints e tolerations você diz que certo nó só aceita um certo tipo de pod, mas não garante que todo pod criado cairá para este nó
	- Você restringe um nó ao que ele pode rodar
	- Você marca um pod com o taint que é aceito
- Para isso, usa-se node affinity, para garantir que esse pod vá para o tal nó.
	- Você diz que ele deve rodar naquele nó

---
- Quanto se têm mais de um scheduler no sistema, é possível passar qual scheduler será usado pelo pod usando a opção `pod.spec.schedulerName`. O nome pode ser visto no `--config` scheduler

### Scheduler Profiles
 - Os pods quando são criados entram na fila do scheduler, e é necessário criar um priorityClass e definir uma `priorityClassName`para organizar a fila
 - Após a fila, os pods são filtrados, para saber em quais nós podem ser alocados
 - Após ele passa pela etapa de scoring, para saber qyal é o melhor nó pra ele ser alocado
 - Após ele passa para etapa de bind, onde o pod será associado a um nó

![[CleanShot 2024-09-30 at 12.37.18.png]]

- Cada etapa pode ser customizada