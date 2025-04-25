---
sticker: emoji//1f4a5
color: var(--mk-color-red)
---

## Center for internet Security (CIS)
- Provê melhores práticas para proteção de ataques virtuais pervasivos
- Prove benchmarks para
	- Sistemas Operacionais
	- Cloud Providers
	- Mobile
	- Dispositivos de Rede
	- Aplicações de Desktop
	- Servidores de Aplicações
- É possível visualizar todas as ameaças possíveis em um sistema, quais sua descrição e como resolver.
- Também disponibiliza ferramentas para fazer a validação destes benchmarks 
	- CIS-CAT - Faz validações relacionadas a sistemas operacionais

## Kube-bench
- Diponibilizado azspela Aqua security
- É uma ferramenta utilizada para validar se o cluster que se pretende avaliar está usando as melhores práticas relacionadas a segurança
- A ferramenta não vai para os nós. É necessário executar o comando em cada um dos nós
- Ele vai avaliar os componentes do cluster, não objetos que são criados pelos usuários
- É possível fazer o check de uma opção em específico passando a opção -c/--check="1.1.1,1.1.2"

```shell
sudo ./kube-bench run --config-dir ./cfg --config ./cfg/config.yaml --targets=WHATTORUN --check="1.1.1"
```

```shell
kube-bench run --targets=node # RODAR NO WORKERNODE
kube-bench run --targets=master # RODAR NO CONTROLPLANE
```


## Resumão

### Control plane host

#### Arquivos

- Os arquivos de configuração do control plane devem estar com a permissão configurada para `600` e o dono e grupo configurado para `root:root`
	- `/etc/kubernetes/manifests/kube-apiserver.yaml`
	- `/etc/kubernetes/manifests/kube-controller-manager.yaml`
	- `/etc/kubernetes/manifests/kube-scheduler.yaml` 
	- `/etc/kubernetes/manifests/etcd.yaml`
	- `/etc/cni/net.d/arquivo-de-configuracao`
	- `/etc/kubernetes/admin.conf` 
	- `/etc/kubernetes/scheduler.conf`
	- `/etc/kubernetes/controller-manager.conf`
	- `/etc/kubernetes/pki/`
	- `/etc/kubernetes/pki/*.crt`
- O diretório de dados do etcd(`/var/lib/etcd`) deve estar com a permissão `700`e o dono/grupo para `etcd:etcd`

#### Api Server

- Desabilitar o acesso anônimo usando a flag `--anonymous-auth=false`
- Não utilizar autenticação baseada em tokens. Logo, não habilitar a flag `--token-auth-file`
- Habilitar o Admission Plugin `DenyServiceExternalIPs`
- Habilitar a comunicação com o Kubelet usando certificado/key usando as flags `--kubelet-client-certificate`e `--kubelet-client-key`
- Habilitar a comunicação com o Kubelet usando uma CA usando a flag `--kubelet-certificate-authority`
- Confirmar que a flag `--authorization-mode` seja configurada para usar `RBAC`e `Node` e não `AlwaysAllow`
- Para proteger a api do `api-server` de `DoS` é necessário o Admission Plugin `EventRateLimit` na flag `--enable-admission-plugins`, bem como, configurar o plugin, usando um arquivo informando a flag `--admission-control-config-file`
- Garantir que o Admission Plugin `AlwaysAdmit` não está configurado na flag `--enable-admission-plugins`
- Garantir que o Admission Plugin `AlwaysPullImages` não está configurado na flag `--enable-admission-plugins`. O plugin garante que a imagem será sempre baixada, mesmo que ela já esteja presente no servidor. Já que pode existir um pod que não tem permissão de usá-la, mas ela já está lá.
- Garantir que o Admission Plugin `ServiceAccount` não está configurado na flag `--enable-admission-plugins`. O plugin garante que quando um pod seja criado, a service account `default`seja associada a ele.
- Garantir que o Admission Plugin `NamespaceLifecycle` não está configurado na flag `--enable-admission-plugins`. O plugin garante  nenhum objeto será criado em um namespace que está no estado de remoção, ou inexistente.
- Garantir que o Admission Plugin `NodeRestriction` não está configurado na flag `--enable-admission-plugins`. O plugin garante que o Kubelet pode gerenciar apenas objetos `Node`e `Pod`presentes no nó que toma de conta
- Garantir que a flag `--profiling` esteja configurada para `false`
- Garantir que as opções de auditoria sejam informadas:
	- `--audit-log-path` - Informa a localização onde os logs de auditoria serão salvos
	- `--audit-log-maxage` - Informa por quantos dias os logs serão guardados. O recomendado são 30 dias
	- `--audit-log-maxbackup` - Informa quantos arquivos de rotação serão retidos. O recomendado são 10.
	- `--audit-log-maxsize`- Informa o tamanho máximo que o arquivo poderá ter. O recomendado são 100
- Garantir que a flag `--request-timeout` seja configurada para utilizar um valor que considere conexões mais lentas.
- Garantir que a flag `--service-account-lookup` está configurada para `true`. Se não estiver habilitada, o api-server apenas verifica que o token de autenticação é válido e não verificará se o token está presente no etcd
- Garantir que a flag `--service-account-key-file`, seja informada. Por padrão o apiserver utiliza a fave privada TLS para verificar os tokens. 
- Garantir que as flags `--etcd-certfile`e `--etcd-keyfile`  para que o apiserver se comunique com o `etcd` de maneira segura
- Para garantir que a comunicação com os clientes sejam segura em transito, é necessário informar as flags `--tls-cert-file` e `--tls-private-key-file`
- Garantir que a flag `--client-ca-file` seja configurada com a CA utilizada
- Garantir que a flag `--etcd-cafile` seja configurada com a CA utilizada
- Garantir que a flag `--encryption-provider-config` seja configurada. A flag aceita um arquivo do tipo `EncryptionConfig`
- Garantir que os provedores de criptogradia sejam configurados. Usando a um arquivo do tipo `EncryptionConfig`, garantir que esteja usando uma das opções `aescb`, `kms` ou `secretbox`
- Garantir que o apiserver esteja usando apenas cifras de criptografia fortes usando a flag `--tls-cipher-suites`

#### Controller Manager

- Garantir que a flag `--terminated-pod-gc-threshold` seja configurada com um valor apropriado. O valor padrão é muito alto(12500), o que pode ser desnecessário para muitos usuários
-  Garantir que a flag `--profiling` esteja configurada para `false`
- Garantir que a flag `--use-service-account-credentials`, fazendo que cada controller manager use uma sa diferente para interagir com o apiserver
- Garantir que a flag `--service-account-private-key-file` seja configurada, fazendo com que uma chave privada seja usada pelas services accounts do controller manager
- Garantir que a flag `--root-ca-file`seja informada, garantindo que os pods façam verificações do certificado antes de estabelecer uma conexão
- Garantir que a opção `RotateKubeletServerCertificate=true`, seja configurada na flag `--feature-gates`, garantirndo que os certificados do kubelet sejam rotacionados
- Garantir que a flag `--bind-address` seja configurada para `127.0.0.1`. Esta configuração garante que o controller manager não se comunique com endereços externos

#### Scheduler

- Garantir que a flag `--profiling` esteja configurada para `false`
-  Garantir que a flag `--bind-address` seja configurada para `127.0.0.1`. Esta configuração garante que o scheduller não se comunique com endereços externos

#### etcd

- Garantir que as flags `--cert-file` e  `--key-file`, sejam configuradas, para que a criptografia TLS do etcd seja ativada
- Garantir que a flag `--client-cert-auth`seja configurada para `true`. Garante que a autenticação de clientes usando certificados
- Garantir que a flag `--auto-tls`  não seja configurada para `true`. Caso seja informada como true, somente certificados que não sejam auto assinados serão aceitos
- Garantir que as flags `--peer-cert-file` e `--peer-key-file` sejam configuradas. Garantindo que as conexões peer utilizem criptografia TLS
- Garantir que a flag `--peer-client-cert-auth` seja configurada para `true`, garantindo que as conexões peer sejam autenticadas utilizando certificados
-  Garantir que a flag `--peer-auto-tls`  não seja configurada para `true`. Caso seja informada como true, somente certificados que não sejam auto assinados serão aceitos
- Garantir que a flag `--trusted-ca-file` seja configurada com um certificado CA diferente do que é utilizado pelos componentes do kubernetes

#### Autenticação e autorização

- Não permitir que certificados de client para serem usados como métodos de autenticação. Não há como revogar a permissão de certificados, uma vez que emitidos. É necessário utilizar mecanimos como OIDC(Como funciona?)
- Tokens fornecidos por service accounts não podem ser utilizados por usuários para fazer interações com o apiserver
- Tokens bootstrap não podem ser utilizado por usuários, visto que são projetados para que novos nós sejam incluídos ao cluster

#### Logging

- Garantir que a policy de auditoria seja configurada de maneira a expor apenas informações necessárias.
- Garantir que as políticas de auditoria incluam somente objetos que se seja observer preocupações com segurança, como secret, configmaps e tokenreviews. Modificações a pods e deployments. Utilizaçào de pods/exec, pods/portforward , pods/proxy e service/proxy


### Worker node

#### Arquivos

- Os arquivos de configuração do worker node devem estar com a permissão configurada para `600` e o dono e grupo configurado para `root:root`:
	- `/etc/systemd/system/kubelet.service.d/kubeadm.conf`
	- `/etc/kubernetes/kubelet.conf`
	- `/etc/kubernetes/pki/ca.crt`
	- `/var/lib/kubelet/config.yaml`

#### Kubelet

- Desabilitar o acesso anônimo usando a flag `--anonymous-auth=false`
- Garantir que a flag `--authorization-mode`, não esteja configurada para `AlwaysAllow`. De preferencia esteja configurada para `Webhook`, fazendo com que a autorização das requisições sejam passadas ao apiserver
- Garantir que a configuração `authentication.x509.clientCAFile`esteja presente no arquivo de configuração do kubelet `/var/lib/kubelet/config.yaml`, garantindo que as conexões serão validadas usando a CA
- Garantir que a flag `--read-only-port` seja configurada para 0, não permitindo que nenhuma informação do kubelet seja exposta sem autenticação
- Garantir que a flag `--streaming-connection-idle-timeout` não esteja configurada para 0, desabilitando o timeout, possibilitando ataques DOS. Por padrão está configurado para 4 horas, o que pode ser muito para muitos sistemas
- Garantir que a flag `--make-iptables-util-chains` seja configurada para true, fazendo com que o kubelet manipule  o iptables
- Garantir que a flag `--hostname-override` não seja configurada, possibilitando a quebra de conexões TLS
- Garantir que a configuração `eventRecordQPS`esteja presente no arquivo de configuração do kubelet `/var/lib/kubelet/config.yaml`, garantindo o limit que eventos são capturados.
- Garantir que as flags `--tls-cert-file` e `--tls-private-key-file`sejam informadas, garantindo a conexão segura entre o kubelet e o apiserver
- Garantir que a flag `--rotate-certificates` não esteja setada para false, fazendo com que os certificados não sejam rotacionados
-  Garantir que a opção `RotateKubeletServerCertificate=true`, seja configurada na flag `--feature-gates`, garantirndo que os certificados do kubelet sejam rotacionados
-  Garantir que o apiserver esteja usando apenas cifras de criptografia fortes usando a flag `--tls-cipher-suites`
- Garantir que um limit de `PID`seja configurado, usando a flag `--pod-max-pids` ou `PodPidsLimit`

#### Kube-proxy

- Garantir que o serviço de métricas seja bindado ao localhost usando a opção `--metrics-bind-address=127.0.0.1`


### Políticas

### RBAC e SA

- Garantir que a role `cluster-admin` seja utilizada apenas onde for necessária
- Minimizar o acesso a secrets. Quando possível remova os verbos `get`, `list`, e `watch` do acesso ao recurso `secret`.
- Minimizar a utilização de wildcards em Roles e ClusterRoles ao escolher quais são os recursos que o objeto interagirá
- Minimizar o acesso à criação de pods dimiuindo a possibilidade de escalonamento de privilégio
- Garantir que a service account não seja ativamente utilizada. Se um pod precisar acessar a API do kubernetes uma nova SA deve ser criada.
- Garantir que a montagem dos tokens de uma SA sejam montadas apenas quando realmente necessária. Sempre que possível informe a opção `automountServiceAccountToken: false`
- Evite a utilização do grupo `system:masters` para permissionar usuários ou service accounts a não ser que necessário
- Limite a utilização das permissões `Bind`, `Impersonate` e `Escalate`, a não ser que seja realmente necessário
	- `Bind` - Permite que o Subject adicione um binding a uma clusterrole ou role, permitindo que sua permissão seja escalada
	- `Impersonate` - Como o nome já diz, permite que um usuário aja como um usuário, ganhando suas permissões
	- `Escalate` - Permite que o subject modificar roles as quais seja anexado, aumentando seus privilégios
- Minimize o acesso à criação de PVs, visto que utilizando `hostPath`é possível montar um diretório qualquer dentro do sistema operacional. 
- Minimize o acesso ao subrecurso approval do objeto `certificatesigningrequests`, visto que esse pode aprovar certificados a serem autorizados a interagir com o apiserver
- Minimize o acesso a objetos webhook, visto que permissões aos objetos `validatingwebhookconfigurations` ou `mutatingwebhookconfigurations` podem ler qualquer objeto admitidos pelo cluster, em no caso do mutate, pode modificar objetos. Por exemplo, mutar uma role criada para dar permissão a um objeto
- Minimize o acesso ao subrecurso token de service accounts, visto que esses podem criar long lived tokens que podem ser utilizados para interagir com a API, dado um certo nível de permissão 

#### Padrões de Segurança do POD

- Garantir que ao menos um mecanismo de política de controle seja implementado. Pod Security Admission
	- No namespace, utilizando a label `pod-security.kubernetes.io/<MODE>: <LEVEL>`. Sendo:
		- Modes:
			- `enforce`: Violações a política farão com que a requisição seja rejeitada;
			- `audit`: Violações a política farão com que auditadas e o evento guardado, porém permitida;
			- `warn`:  Dispararão um Warning para o usuário, mas serão permitidas
		- Level:
			- `privileged`:  Propositalmente aberta, e irrestrita;
			- `baseline`: Prevê o prevenimento de escalação de privilégios
			- `restricted`: Complemetamente restrita. Segue as melhores práticas de hardening de pods
- Minimizar a admissão de containers privilegiados. Visto que um container privilegiado têm acesso a todas as capacidades que um host tem
- Minimizar a admissão de containers que permitem a intenção de compartilhar o PID do host usando a opção `hostPID`. Visto que este pode inspecionar processos que estão rodando fora do container
- Minimizar a admissão de containers que permitem a intenção de compartilar o IPC namespace usando a opção `hostIPC`. Visto que este pode inspecionar processos que estão rodando fora do container
- Minimizar a admissão de containers que permitem a intenção de compartilhar a rede do host utilizando a opção `hostNetwork`, visto que este pode acessar a rede loopback, permitindo observar o tráfego de rede de outros pods\
- Minimizar a admissão de containers que utiliza a opção `allowPrivilegeEscalation`. Faz com que um processo de um container tenha mais permissão do que deveria. Permitir o `sudo`
- Minimiar a admissão de containers que rodem com o usuário root. Que é o padrão. MustRunAsNonRoot or MustRunAs
- Minimizar a admissão de containers que utilizem capabilities fora do pacote padrão.
- Minimizar a admissão de containers que utilizem volumes do tipo hostPath
- Minimizar a admissão de containers que utilizem hosts ports

#### CNI e Network Policies

- Garantir que a CNI utilizada suporte a utilização de network policies
- Garantir que todos os namespaces tenham  Network Policies definida, visto que um pod de outro namespace pode acessar pods neste namespace

#### Secrets

- Prefira secrets montadas como arquivos em um container que variáveis de ambiente. É comum aplicações cuspirem as variaveis de ambiente configuradas, e a secret estará lá
- Considere a utilização do armazenamento de secrets externamente.

### Admission Control Extensível

- Configure a proviniencia de imagens utilizando o admission controller `ImagePolicyWebhook`, garantindoq ue apenas imagens aprovadas sejam implantadas no cluster

### Políticas gerais

- Crie barreiras administrativas entre recursos usando namespaces. 
- Garanta que o profile seccomp está configurado para docker/default nas definições do pods. Restringindo o conjunto de systemcalls que uma aplicação pode executar.
- Aplique securityContext aos seus pods e containers
- O namespace default não deve ser utilizado