
# Arquitetura

## Nó (nodes)
* É uma máquina onde o `k8s` lançará containers;
* É uma máquina onde o `k8s` e o container runtime será instalado;
* Um nó é uma máquina que aumentará a capacidade física de recursos do cluster;
* Os nós são transparentes ao cluster. A aplicação verá apenas uma máquina gigante.
* No passado eram referidas como `minion`;
* Um nó é uma máquina(virtual ou física) em que é instalado os componentes do `k8s` e a container runtime;
* Existem dois tipos de nós disponíveis: _master_ e _worker_;
* Deve existir pelo menos um nó `master`(1..\*) e 0..\* nós `worker`;
* Cada nó contêm [[Pods]] que contêm um ou mais containers de uma aplicação;
* Por padrão, a informação da localização de implantação dos componentes não possuem importância;
* O kubernetes pode transferir todos os componentes de um nó para outro sem que os usuários notem;
* Um `cluster` é um conjunto de nós agrupados, garantindo que se um nó falhar, outro nó responderá pela requisição. Além disso, quando se está utilizando nós, existe a premissa de compartilhar o `load(processamento)`. 

### Master - Control Plane
* Responsável por gerenciar o cluster;
* É onde todos os componentes do core do Kubernetes estão rodando
* Conhecido como master plane;
* Pode-se haver mais de um master para manter a alta disponibilidade
* Guarda as informações dos membros(nodes), do cluster;
* Monitora os nós;
* Quando um nó falha, é responsável por mover o processamento para outros nós, garantindo a resiliência;
* Responsável pela orquestração dos containers nos `worker` nodes;
 - `master` possui o `kube-api-server`.
 * Todas as informações capturadas(do worker node) são guardadas no `etcd` do master
 * Possui o `controller manager` e o `scheduller`;
 * É responsável por iniciar e executar as instruções de um `spec` para implantar uma aplicação

#### Componentes do master-plane
* **API Server(`kube-apiserver`):** Atua como uma fachada do Kubernetes. Os usuários, gerenciadores de dispositivos, ferramentas cli, conversam com o API Server para interagir com o Kubernetes; Funciona como um hub de comunicação entre todos os outros elementos. É o único componente que se comunica com o `etcd`. Todos os outros componentes se comunicarão com a API para modificar o estado do cluster.
	* É o componente ao qual se comunica quando executa um comando com `kubectl`
*  **Scheduler(`kube-scheduler`):** Responsável por distribuir o processamento entre os nós. Observa por novas requisições de containers e os atribui a nós. Atribui as aplicações a um node `worker`. Automaticamente colocará o pod baseado em seus prerequisitos(hardware);
* **Controller Manager(`kube-controller-manager`):** É o cérebro por trás da orquestração. É responsável por sinalizar quando nós ou containers morrem. Toma decisões para criar novos containers nestes cenários. Mantem a replicação de componentes e a quantidade de [[Pods]] correta
	* Gerencia os processos do Core do kubernetes
* **Etcd service:**  `key-value store` distribuído utilizado pelo `k8s` para guardar todos os dados gerenciados pelo cluster. É responsável por implementar travas entre os nós `master` para não haver conflitos; Guarda as configurações do cluster. É importante manter um backup dessas informações.
* **Container Runtime:** (RKT, Docker, CRI-O, containerd): É o software responsável por rodar os containers nos nós.
* **Kubelet service:** Agente que roda em todos os nós do cluster. É responsável  por garantir que os containers estão rodando nos nós, como esperado.  Executa e gerenciar os containers em um nó, e se comunica com o API Server. Além disso, se comunicará com o Container Runtime para que baixe imagens para rodar um pod

### Worker
* Responsável por executar containers([[Pods]]);
* Responsável por rodar as aplicações
* Responsável por monitorar as aplicações, e prover os serviços que ela necessitar
 * `worker` possui o kubelet, agente responsável por interagir com o master. Provê informações sobre a saúde do nó e executar tarefas requisitadas pelo master

#### Componentes do nó
* **Kubelet service:** Agente que roda em todos os nós do cluster. É responsável  por garantir que os containers estão rodando nos nós, como esperado.  Executa e gerenciar os containers em um nó, e se comunica com o API Server. Além disso, se comunicará com o Container Runtime para que baixe imagens para rodar um pod
* **kube-proxy**: Balanceia o trafego entre os componentes da aplicação. Garante que os containers em nós diferentes se comuniquem em problemas.
	* É quem vai criar as regras usando, geralmente, o `iptables` para que todos os pods no cluster possam se comunicar entre si.
* **Container Runtime:** (RKT, Docker, CRI-O, containerd): É o software responsável por rodar os containers nos nós.

Quando as especificações da sua aplicação estiverem completas, o `scheduler` notificará os nós, por intermédio do  `kubelet`, e o mesmo instruirá que o `container runtime` baixe as imagens necessárias da aplicação.

O `master` fará com que as aplicações sempre estejam no estado especificado, caso mude, o mesmo fará procedimentos para que isso seja alcançado.

**Declarative Intent**

[[Pods]] e Services, por exemplo, são entidades persistentes.


#### Comandos úteis
> Recupera o status dos componentes do control plane
> `kubectl get componentstatus`

 > Recupera os nós do cluster
 > `kubectl get nodes`

> Recupera informações sobre todos os nós
> `kubectl describe nodes`

> Lista todos os tipos de objetos disponíveis no cluster
> `kubectl api-resources`