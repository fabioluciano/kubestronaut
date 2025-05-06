# API

- O Kubernetes fornece uma API para interagir com o cluster
- Todos os recursos são acessíveis usando Restful resources
- A API representa recursos dentro do cluster
- Suporta configuração declarativa usando `JSON`ou `YAML`.
- Permite a autenticação e autorização usando diferentes soluções
- É extensível, permitindo a criação de outros recursos
- O que está na versão v1 é GA
- Os grupos podem ter mais de uma versão ativa
- O [kube-proxy](nodes-components/kube-proxy.md) roda na máquina cliente, permitindo a comunicação com o apiserver utilizando as mesmas configurações do `.kube/config`

## Api Groups

As APIs são divididas em grupos:

- `/metrics` e`/healthz`: Usadas para monitorar a saúde do cluster
- `/version`: Visualizar a versão do cluster
- `/api/v1`: Core group
  - `ns`, `po`, `rc`,`events`,`endpoints`, `nodes`, `bindings`, `pv`, `pvc`, `cm`, `sercrets`, `services`
- `/apis`: Named group
  - É mais organizado, logo, todas as novas funcionalidades serão adicionadas a essa lista organizada por nome
  - API GROUPS: `/apps`, `/extensions`, `networking.k8s.io`, `storage.k8s.io`, `authentication.k8s.io`, `certificates.k8s.io`
  - apps/v1: RESOURCES
    - deployments
    - replicasets
    - statefulsets
  - networking.k8s.io/v1
    - networkpolicies
  - Cada recurso possui um verbo RESTful associado:
    - list, get, create, delete, update e watch
- `/logs`: Integração com aplicações de terceiros

```shell title:"Recupera a versão usando uma requisição HTTP"
# Primeio ddescobre-se o endereço do control plane
k get nodes -o wide

## Faz-se uma requisição para o endpoint de versão
curl https://172.18.0.4:6443/version -k
```

```shell title:"Recupera a lista de recursos disponíveis para criação no cluster"
kubectl api-resources
```

```shell title:"Retorna todas as versões dos recursos intalados"
kubectl api-versions
```

```shell title:"Acessar o endpoint do kubeapiserver com as configurações de kubeconfig"
kubectl proxy
```

```shell
curl 127.0.0.1:8001/api/v1/namespaces/default/pods | jq '.items[].metadata.name'
```

## API Deprecations

- Com o lançamento de novas versões do kubernetes, as APIs de recursos podem ser depreciadas
- O padrão é o Kubernetes manter a versão com suporte por mais duas versões

```shell title:"Habilita a uma versão/Desabilita uma versão"
apiserver --runtime-config=rbac.authoraization.k8s.io/v1alpha1,batch/v1beta1=false
```

```shell
kubectl-convert -f ARQUIVOANTIGO --output-version GROUP/VERSIONNOVO
```

## API Extensions

- Api pode ser ser estendida de diversas maneiras:
  - CustomResourceDefinitions
  - Controllers customizados
  - Agregação de API

### Custom Resource Definition

- Permite a adição de recursos a API de maneira simples
- É adicionado ao servidor do kubernetes e segue seu mecanismo de atualização
- É o padrão _de facto_, para adição de recursos a API
- São adicionads como extensões da API do Kubernetes

### Controller customizados

- É um processo que monita modificações na APi do kubernetes
- Quando as modificações acontecem, o controller garante que o estado desejado seja mantido\
- Permite a automação de tarefas no cluster
- Os ontroler utilizam bibliotecas (SDKs) para se comunicarem com a API

### Agregação de API

- Adiciona funcionalidades a API do Kubernetes por extensão
- Permite um alto nível de cuustomização
- Permite a integração de recursos de diferentes fontes

```shell
kubectl get crd
```

## Operators

- Aplicações customizadas que se baseaim no CustomResourceDefinition
- Pode ser visto como uma maneira de empacotar, rodar e gerenciar aplicações no Kubernetes
- Utiliza controller para continuamente operar dinamicamente o sistema
