---
tags: K8s, kubernetes
---
# `KubeCtl`

*`kubectl`* *kubecontrol* *kubecâtâl*: Utilizado para implantar e gerenciar aplicações em um cluster `k8s`

>**Habilita o autocomplete** 
> `source <(kubectl completion bash)`
> `echo "source <(kubectl completion bash)" >> ~/.bashrc`

```shell
kubectl get --raw='/healthz?verbose'
`
```
### Recuperar informações sobre um determinado recurso
```shell
kubectl explain pod --recursive #explicação sobre qualquer conteudo de um objeto
```

### Criar um manifesto de pod
```bash
export kdry="--dry-run=client -o yaml"
kubectl run nginx --image nginx $kdry
```

### Editar informações de um recurso
```bash
kubectl edit pod meu-pod
```

### Editar informações com replace
```bash
export kdry="--dry-run=client -o yaml"
kubectl get pod meu-pod $kdry > meu-pod.yaml
kubectl replace -f meu-pod.yaml
```

### Executa uma operação em todos os recursos filtrados
```bash
for i in $(k get po --namespace default  --output jsonpath="{.items[*].metadata.name}" ); do; echo $i ; done;
```

### Executar um comando em um pod
```bash
kubectl exec -ti meu-pod -- command
```

### Remover recurso sem esperar

```bash
kubectl delete pod sleep --force --grace-period 0 #ignorará o pod.spec.terminationGracePeriodSeconds
```

### Replace sem esperar
```bash
kubectl replace -f pod-sleep.yaml --force --grace-period 0
```

### Efetua um patch em um recurso

``` yaml
metadata:
  labels:
    labelaaaa: dsds
    dlsldslds: asda
```

```bash
kubectl patch -f pod-sleep-patch.yaml pod sleep
```

### Recuperar informações mais informações dos pods
``` bash
kubectl get pods -o wide
```


### Aumentar o número de replicas de um replicationController
``` bash
kubectl scale --replicas NUMREPLICAS -f arquivoreplicationcontroller.yaml
kubectl scale rs replicaset-teste --replicas NUMREPLICAS
```

### Cria um pod com um command definido
``` bash
export kdry="--dry-run=client -o yaml"
kubectl run --image nginx $kdry --command -- /bin/bash -c sleep
```


```shell title:"Recupera todas as variaveis de ambiente disponíveis em um pod"
kubectl exec -ti pod-with-configmap -- env
```



```shell
kubectl port-forward pod/svc resource 8080:80 # A primeira porta é a do host, a segunda do POD/SERVICE
```