---
color: var(--mk-color-red)
---
## Role
- Pra definir uma role, você informa três parâmetros:
	- É por namespace
	- `rules.apiGroups`:  Informar o apiGroup que se deseja autorizar. Caso seja um recurso do api group core, não é necessário informar
	- `rules.resources`: Recursos a serem autorizados pela role
	- `rules.verbs`: Operações authorizadas pela role
	- `rules.resourceNames`: autoriza recursos específicos

## RoleBinding

- Anexa uma Role a um elemento `user`, `serviceaccount` `group`
	- É por namespace
	- `rolebinding.subject`: O usuario que se deseja associar
	- `rolebinding.roleRef`: A role que se deseja associar

## ClusterRole
- Para recursos que não são específicos de um namespace
- Você pode configurar, por exemplo, que um usuário possui uma clusterrole associada com pods. ele terá acesso a TODOS os pods em TODOS os namespaces
- Não fazem parte de NENHUM namespace

## ClusterRoleBinding

- Anexa uma Clusterrole a um usuário

```reference
filePath: "@/Attachments/Kubernetes/rbac/rbac-reader-test.yaml"
```

## Comandos úteis

```shell title:"Recupera a lista de todos os recursos que não são especificos de um namespace". Logo, são ClusterRole
kubectl api-resources --namespaced=false
```

```shell title:"Verificar se o usuário atual possui uma determinada permissão"
kubectl auth can-i create deployment
```


```shell title:"Verificar se um usuario possui uma determinada permissão"
kubectl auth can-i create deployment --as user
```

```shell
kubectl auth can-i get pods --as system:serviceaccount:default:reader
```


```shell title:"Retorna todos os verbos que "
kubectl api-resources -o wide
```

```shell title:"cria uma role"
kubectl create role developer --verb=create,list,delete --resource=pods
```

```shell title:"cria uma role"
kubectl create rolebinding user-x-developer --role=ROLE --user=USER
```


```shell
kubectl create rolebinding --serviceaccount NAMESPACE:SERVICEACCOUNT --role ROLE
```


```shell
kubectl set serviceaccount deployment SERVICEACCOUNT DEPLOYMENT
```


## Inspecting Secrets

```reference
filePath: "@/Attachments/Kubernetes/rbac/rbac-cli-access-pod.yaml"
```

```shell
kubectl get pod rbac-cli-access -o yaml | grep serviceAccountName
```

```shell
k get pod rbac-cli-access -o yaml | yq '.spec.containers[].volumeMounts[0].mountPath'
```

```shell
TOKEN=$(k exec -ti rbac-cli-access -- cat /var/run/secrets/kubernetes.io/serviceaccount/token)

 echo -n $TOKEN | jwt decode - --json | jq
```

---

```shell
curl -k -H "Authorization: Bearer $TOKEN"  https://kubernetes/api/v1 | jq '.resources[].name'

curl -k -H "Authorization: Bearer $TOKEN" https://kubernetes/api/v1/namespaces/default/pod

curl -k -H "Authorization: Bearer $TOKEN"  https://kubernetes/apis/authentication.k8s.io/v1/selfsubjectreviews -X POST --json '{"kind":"SelfSubjectReview","apiVersion":"authentication.k8s.io/v1"}'
```


```reference
filePath: "@/Attachments/Kubernetes/rbac/rbac-cli-access-sa.yaml"
```

```reference
filePath: "@/Attachments/Kubernetes/rbac/rbac-cli-access-role.yaml"
```


```reference
filePath: "@/Attachments/Kubernetes/rbac/rbac-cli-access-rolebinding.yaml"
```


```reference
filePath: "@/Attachments/Kubernetes/rbac/rbac-cli-access-pod-with-sa.yaml"
```


```shell
curl -k -H "Authorization: Bearer $TOKEN" https://kubernetes/api/v1/namespaces/default/pod

curl -k -H "Authorization: Bearer $TOKEN"  https://kubernetes/apis/authentication.k8s.io/v1/selfsubjectreviews -X POST --json '{"kind":"SelfSubjectReview","apiVersion":"authentication.k8s.io/v1"}'
```


### Combinações de Roles/Rolebindings

- `Role` + `RoleBinding` = A role estará disponivel no namespace, o rolebinding será aplicado no namespace
- `ClusterRole` + `ClusterRoleBinding` = A Role estará disponível em todos os namespaces, a ClusterRolebinding será dada em TODOS os namespaces
- `ClusterRole`+ `RoleBindind` = A role estará disponível em todos os namespaces, a permissão será dada em apenas um namespace 


EH POSSIVEL COM O VERBO LIST VER TODAS AS SECRETS, VISTO QUE VOCE PODE LISTAR USANDO JSON/JSONPATH