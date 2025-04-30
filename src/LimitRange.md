- É utilizado para definir valores padrão para containers, [[Pods]] e [[PersistentVolumes]]
- É aplicável a nível de namespace
- Afetará somente containers, [[Pods]] e [[Storage]] criados após a sua criação. Pods preexistentes não serão afetados pelo limit range; Por que a validação será feita pelo admission controller.
- É importante notar que, ao definir um limit range, e não definir um resource para seu recurso, ele vai pegar automaticamente o que foi definido no limitrange
- Caso editado, os valores definidos no limitrange só serão refletidos nos pods do namespace caso sejam recriados.
- Caso o tipo seja pod, os valores de CPU/Memoria serão da soma de requests/limits de todos os containers,
- Quando você definir um LimitRange, será obrigatória o preenchimento do resources para PODS

### Propriedades importantes

`spec.limits.type`: O tipo de componente a ser configurado. Pode ser `Pod`, `Container` ou `PersistentVolumeClaim`.
`spec.limits.default`: Define o limit default que será implementado caso não seja fornecido. Não funciona para pods
`spec.limits.defaultRequest`: Define o requests default que será implementado caso não seja fornecido. Não funciona para pods
`spec.limits.min`: Define o mínimo de recurso sque pode ser declarado `cpu`, `memory` `storage`
`spec.limits.max`: Define o máximo de recurso sque pode ser declarado `cpu`, `memory` `storage`


> [!NOTE]- LimitRange de recursos de um container
```reference
filePath: "@/Attachments/Kubernetes/limitrange/limitrange-container-test.yaml"
```


> [!NOTE]- LimitRange de recursos de um pod
```reference
filePath: "@/Attachments/Kubernetes/limitrange/limitrange-pod-test.yaml"
```


> [!NOTE]- LimitRange de recursos de um pvc
```reference
filePath: "@/Attachments/Kubernetes/limitrange/limitrange-pvc-test.yaml"
```