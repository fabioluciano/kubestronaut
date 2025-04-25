---
tags: kubernetes Pods Annotations softwarearchitecture 

---
# Api Objects

* São dados que representam o estado do cluster
* Quase tudo no K8s é representado como um objeto([[Arquitetura#Nó nodes | nós]], services, pods, e etc.)


Propriedades padrão de qualquer objeto definido no cluster: **`apiVersion`**, **`kind`**, **`metadata`** e **`spec`**
``` yml
apiVersion: v1 # Versão da API do Kubernetes, que está sendo utilizada para criar o objeto
kind: Pod # Referencia o tipo de objeto que está sendo descrito no documento
metadata: # Referencia informações sobre o objeto. É um dicionário
	name: myapp-prod # só pode conter 253 caracteres [.-a-z]
	annotations:
		dadsasd/res: "1"
	labels: # Pode-se colocar quantas labels achar necessário
		app: myapp
		enviroment: qa
spec: # Especificações do objeto a ser criado. Varia de objeto para objeto
	containers: # Lista / Array
		- name: nginx-container
		  image: nginx:latest
status: # DEscreve o status atual do objeto no cluster. É fornecido e atualizado pelo k8s
ApiObjects
```

spec:  Define o estado desejado do objeto
status: Define o estado atual do objeto

O que o `k8s` fará para alcançar o estado esperado.


## Comandos úteis
