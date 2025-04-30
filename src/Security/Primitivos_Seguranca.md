
## Primitivos de segurança

**Host**
- Todos os hosts precisam ser seguros
- Desabilitar o acesso root
- Desabilitar a autenticação baseada em user/pass
- Autorizar somente usando chaves
- A primeira linha de defesa é o [[kube-apiserver]]. Como ele recebe todas as requisições sobre o que acontecerá no cluster
	- Quem acessa o cluster [[Primitivos de Segurança#Autenticação]]
	- O que, quem acessa o cluster, pode fazer [[Primitivos de Segurança#Autorização]]
- A comunicação entre todos os componentes é assegurada utilizando certificados TLS

## Autenticação
- O kubernetes não gerencia usuários por padrão. Ele depende de outras fontes externas para sua administração
- Todo acesso de usuários é gerenciado pelo `kube-apiserver`. Seja pelo `kubectl`, ou pela API. O `kube-apiserver`, autentica as requisição antes de processá-la.
- Existem diversas maneiras de autenticação:
	- Arquivo com usuarios e senhas
	- Arquivo com usuários e tokens
	- Certificados
	- Serviço de identidade(LDAP)
 
### Arquivo com usuarios e senhas e token
- Cria um arquivo csv com quatro(a última e opcional) columas: `password`, `username`, `userid` ,`group` e se passa como opção para o kube-api server `--basic-auth-file=user-datails.csv`
- Tanto a lista de usuários, quanto a lista de tokens não são recomendadas

```shell
curl -v -k https://localhost:6443/api/v1/pods -u "user1:password123"
```

### KubeConfig
- Localização padrão `~/.kube/config`, pode ser utilizar a variável $KUBECONFIG
- Arquivo de configuração que guarda informações relativas aos clusters e autenticação a eles.
- São configuradas três informações:
	- `current-context`: Contexto utilizado no momento
	- `Clusters`: Informações referentes ao cluster disponíveis para conexão
		- server: Endereço do servidor do cluster
		- certificate-authority: Certificado
	- `Users`: Usuários autorizado a se conectar ao cluster
		- client-certificate
		- client-key
	- `Contexts`: União entre os Clusters e os Usuários
		- Cluster
		- User
		- Namespace

```shell title:"merge de kubeconfig"
export KUBECONFIG=~/.kube/config**:**/path/cluster1:/path/cluster2

kubectl config view --flatten > all-in-one-kubeconfig.yaml
```



## Autorização

- Como administrador, você pode performar qualquer operação
- Há diversos mecanismos de autorização disponíveis no kubernetes
	- Node
		- O Kubelet acessa o kube-api server para gerenciar, assim como nós usuários
		- O Kubelet acessa o kube api para ler informações sobre servi;os , endpoints nós e pods
		- O kubelet também informa o kube-api com informações sobre nós pods e events
		- Todas essas requisições são manipuladas pelo `Node Authorizer`
			- Qualquer requisição provinda de um usuário prefixado com `system:node:` é autorizado pelo `Node Authorizer`
	- Attribute Based Authorization (ABAC)
		- Quando você autoriza um usuário ou um grupo de usuários a um conjunto de permissões 
		- É feito utilizando um arquivo `Policy` json com o que o dado usuário pode fazer
		- Toda vez que há edição nesse arquivo, você precisa reiniciar o `kube-apiserver`
	- RoleBased Authorization ([[RBAC]])
		- É definido um papel, e quais permissões aquele papel possui, então todos os usuários que precisam daquela role é associado
	- Webhook
		- Permite a externalização da autorização do kubernetes
	- AlwaysAllow - autoriza qualquer requisição sem fazer qualquer filtro de autorização
	- AlwaysDeny - nega qualquer requisição sem fazer qualquer filtro de autorização
- Se você não definir o `--authorization-mode` no `kube-apiserver`, ele é setado automaticamente para `AlwaysAllow`. É possível ter multiplos authorization mode, separador por vírgula.
	- Caso seja provido mais que um, ele vai autorizar em cada um, de modo separado e sequencial
	- O apiserver vai testar a requisição para cada authorization mode informado, até que um retorne TRUE, se não, passa para o próximo

