---
tags:
  - Kubernetes
  - Pods
  - Annotations
  - Labels
---
## Labels
- Utilizado para categorizar os recursos do kubernetes. 
- Usa-se seletores para selecionar recursos baseados em labels
- Todos os recursos criados usando `kubectl create deployment RESOURCENAME`vão criar uma label `app=RESOURENAME` e  e `kubectl run RESOURCENAME` `run=RESOURCENAME`
- Labels adicionadas após a criação de um objeto, não serão herdadas automaticamente pelos filhos. Será necessário recriá-la.


```shell title:"Adiciona uma Label"
kubectl label RESOURCE LABEL=VALUE
```

```shell title:"Remove uma label"
kubectl label RESOURBE LABEL-
```

```shell title:"Recupera todos os LABELS que uma determina LABEL tenha um determinado VALUE"
kubectl get pods --selector LABEL=VALUE
```

```yaml
apiVersion: v1
metadata: 
	labels:
		teste: dsdlsdlsl
```
## Annotation
* Provê informações adicionais ao objeto a ser criado

```yaml
apiVersion: v1
metadata: 
	annotations:
		teste: dsdlsdlsl
```

```shell
kubectl annotate pod podname annotation="value"
```
