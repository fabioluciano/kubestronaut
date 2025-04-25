# Pods 

## Conceitos
* O `k8s` não implanta containers diretamente no nós `worker`. Os containers são encapsulados em objeto interno, conhecido como `Pod`;
* É uma instância de uma aplicação
* É o menor objeto que se pode criar no k8s;
* Para escalar uma aplicação para aguentar uma maior quantidade de trafego, aumenta-se o número de `Pods`(réplicas) e não de containers em um `Pod`;
* Caso o [[Arquitetura#Nó nodes | nó]], não tenha recursos necessários para rodar mais que uma instância da aplicação, é possível subir o `pod` em um novo [[Arquitetura#Nó nodes | nó]].
* `.spec.volumes.projected` são para montar vários arquivos dentro de uma mesma localização
* Todo pod requer uma certa quantidade de recursos para rodar

## Multi-container pods
* Geralmente um `pod` possui uma relação `1:1` com containers rodando a aplicação. Para `scale up` você adiciona um pod, para `scale down` remove-se o pod.
* Um `pod` pode conter mais que um container, geralmente com tarefas de suporte ao container principal da aplicação; Os containers dentro do `pod` escalarão juntos.
* Pode-se referenciar os containers por `localhost` para comunicação, já que compartilham o mesmo namespace de rede. Assim como o namespace de storage (IPS?) 
* Existem alguns tipos de padrões para pods com multicontainers, os principais são:
	* Ambassor - Funciona como um proxy do cotainer principal com outros componentes. funciona como faixada para o container principal
	* Adapter - Padroniza e normaliza as saidas do container principal
	* Sidecar - Extende e melhora o container principal
		* **É um initcontainer que têm o restartPolicy set to Always** DESDE a versão 1.29 - PESQUISAR SIDECAR NA DOCUMENTAÇÃO

### InitContainer
- São containers que rodarão antes dos containers normais
- Geralmente executarão tasks 
- Se existir mais de um, vai rodar em sequência
- Caso falhe, o pod entrará em Crashloop, e  o container principal nunca se iniciará  


> [!NOTE]- Pod with multiple containers
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-with-initcontainer.yaml"
```


## Pod Definition
```yml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    application: myapp
    tier: frontend
spec:
  containers:
  	- name: nginx
	  image: nginx:latest
	- name: redis
	  image: redis:latest
```


- Os valores editáveis de um pod são: 
	- `spec.containers[*].image`
	- `spec.initContainers[*].image`
	- `spec.tolerations`
	- `spec.terminationGracePeriodSeconds`


Quando há mais de um container no mesmo Pod, eles sempre compartilharão o mesmo nó, visto que compartilharão a mesma camada de rede(namespace?)

- `spec.containers[*].command` é uma alternativa para sobrescrever o entrypoint dos containers que estiverem rodando em um pod.
- `spec.containers[*].command` é o programa a ser executado ao container subir, e `spec.containers[*].args` são os argumentos a serem passados para o `spec.containers[*].command`
- `spec.containers[*].command` vai substituir o `entrypoint`definido no `Dockerfile` da imagem utilizada e `spec.containers[*].args` vai substituir o `CMD` do `Dockerfile`.


> [!NOTE]- Pod with multiple containers
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-multiple-containers.yaml"
```



> [!NOTE]- Pod with arguments
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-sleep.yaml"
```


> [!NOTE]- Pod patch
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-sleep-patch.yaml"
```

## Security Context

* As configurações de segurança podem ser feitas ao nível de pod, ou container
* Somente containers possuem capabilities. `pod.spec.containers.securityContext.capabilities`
* As definições feitas ao nível de container vão sobrescrever as definições feitas ao nível de pod.
* Quando o container é privilegiado, são habilidatas TODAS as capabilities to linux
* `pod.spec.securityContext.runAsUser`: Faz com que o usuário seja um numero especfico
* `pod.spec.securityContext.runAsGroup`: Faz com queo grupo seja um numero especifico
* `pod.spec.securityContext.fsGroup`: Faz com que o sistema de arquivos esteja em um numero especifico
* `pod.spec.containers.securityContext.readOnlyFilesystem`

> [!NOTE]- Pod security context
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-with-security-context.yaml"
```


> [!NOTE]- Pod com volumes projetados
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-with-projected-volumes.yaml"
```

##  Resource Request

* Por padrão um container não possui limite de recursos consumidos
* O scheduler vai olhar para esses recursos para determinar onde ele alocará o workload
* Os recursos são por container, e não por pod
* CPU = 1 Cores 1000m == 1 Core
* Memory = G = 1000M Gi=1024M
* O request serve para saber em qual nó ele vai alocar os container, baseado nos recursos necessários, o limit, limita o quanto ele pode chegar
* Caso o container comece a usar mais CPU que o limit, o pod começará a limitar os recursos utilizados pelo container. No caso do container começar a utilizar mais memória que o limit, ele matará o pod com a message OOM(Out of memory)
* Se você setar somente o limit, o kubernetes encarará como sendo o request=limit
* Para CPU, o melhor cenário é fazer o request necessário de CPU, mas não limitar, visto que pode haver recursos não utlizados, que podem ser utilizados pelo POD.
* É possível definir que um pod tenha um conjunto de recursos garantidos. Para isso é necessário definir um [[LimitRange]]]

> [!NOTE]- Pod with resource requests
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-with-resource-request.yaml"
```


> [!NOTE]- Pod security context
```reference
filePath: "@/Attachments/Kubernetes/pod/pod-with-resource-request-and-limits.yaml"
```


```shell
kubectl set resources deployment nginx -c=nginx --limits=cpu=200m,memory=512Mi
```


## Restart Policy

- Gerencia o que acontece com um container quando ele crasha
- O valor padrão é `Always`, fazendo com que o container continue reiniciando

## Comandos úteis

```shell title:"Encapsula uma docker image em um Pod e a executa no cluster"
kubectl run nginx --image nginx`
```
> 
> 
> Recupera a lista de todos os Pods
> `kubectl get pods`

> Edita um pod a partir de sua definição
>  `kubectl edit pod podname`

> Aplica(cria ou atualiza) uma [[ApiObjects | definição de um objeto]] no cluster
> `kubectl apply -f pod-definition.yaml`
 
 > Cria uma [[ ApiObjects | definição de um objeto]] no cluster
> `kubectl create -f pod-definition.yaml`
 
 
> Descreve todas as informações de todos os pods em um determinado namespaces (padrão: default)
> `kubectl describe pod`

> Descreve todas as informações de um pod em um determinado namespaces (padrão: default)
>  `kubectl describe pod/pod-name`

> Recupera todos os pods de todos os [[Namespace | `namespaces`]] e imprime mais informações
> `kubectl get pods --all-namespaces -o wide`

> Recupera todos os pods com a informação das labels
> `kubectl get pods --show-labels`

> Recupera todos os pods que estão estão rodando
> `kubectl get pods --field-selector status.phase==Running`

> Recupera todos os pods que estão estão rodando no namespace default
> `kubectl get pods --field-selector status.phase==Running,metadata.namespace=default`

kubectl exec -ti nginx -c container -- bash

curl telnet://localhost:porta WTFFFFF




Para garantir a imutabilidade do container, deve-se aplicar `pod.spec.securityContext.readOnlyRootFilesystem`para true, e o que for modificável, montar um volume `emptyDir`