# Namespace

## Definição
- É um recurso para separar as entidades em ambientes
- Para recursos de um namespace acessar conteúdo de outro namespace, é necessário passar a URL fqnd, visto que a service sempre vai criar `service.name.namespace.svc.cluster.local`
- Usa os conceitos do Kernel do Linux para isolar recursos 

## Comandos úteis

### Troca de namespace
``` bash
kubectl config set current-context kind-teste --namespace resource-quota
```

```shell\
kubectl get pods -A # Mesmo que --all-namespaces
```