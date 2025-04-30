# Introdução 
Num modelo sem kubernetes, onde implementamos um _pseudo-cluster_, como resolver os seguintes problemas:
* O que fazer quando um container apresenta problemas?
* O que fazer quando um nó, de seu _pseudo-cluster_ morrer?
* O que fazer quando um nó, não renponder a uma requisição?

> Quanto mais de um artefato está implantando para construir uma aplicação(microserviços);

* Naked Pod, executado pelo K8s, mas não gerenciado por ele
* O replicaset guarda a quantidade de replicas que um container deve rodar, o deployment, fica em cima do replicaset... O deployment guarda as versões dos containers que estão rodando.
* O service é um balanceador de carga para os deployments


É necessário a criação de mecanismos de monitoramento do estado de todos os elementos do _pseudo-cluster_, implementação de lógicas complexas e customizadas para garantir a disponibilidade de sua aplicação.

* Também conhecido como `K8s` é um orquestrador de aplicações containerizadas.

* Provê mecanismos para construção e implantação de aplicações distribuídas de maneira a manter a confiabilidade e escalabilidade

## Conceitos

**Confiabilidade:** Os serviços não podem falhar. Se partes do sistema falhar, outras deverão continuar a funcionar.

**Disponibilidade:** O sistema deve se manter disponível mesmo em atualizações/manutenções.

**Escalabilidade:** Estratégia de alocação de recursos em operação. Controlar o aumento e diminuição de recursos de acordo com a demanda.

- **Horizontal:** Adição ou remoção de nós
- **Vertical:** Adição de mais recursos computacionais aos nós 

**Elasticidade:** Adapta a capacidade em relação a demanda. Geralmente está diretamente associada ao monitoramento e automação de disponibilização de recursos

A utilização de um orquestrador como `K8s` habilita, entre outras: _velocidade_, _escalabilidade_, _abstração da infraestrutura_ e eficiência.

## Velocidade
Não é o número de funcionalidades entregues, mas sim o número de `coisas` entregues, enquanto o sistema se mantêm altamente disponível.

A interrelação entre **imutabilidade**, **configuração declarativa** e **self-healing**, aumenta a velocidade com que se implanta aplicações de maneira confiável.

### Imutabilidade
A utilização de containers e um orquestrador como o `K8s` encoraja o desenvolvimento de sistemas distribuídos que aderem ao princípio de **infraestrutura imutável**

**Infraestrutura mutável:** O estado da infraestrutura é representado como um acúmulo de mudanças e atualizações, ou seja, as atualizações, mesmo que feitas de maneira automatizadas, seguem uma sequência definida de procedimentos que devem ser executados.

**Infraestrutura imutável:** É representado com um único artefato. Para trocar a versão de uma biblioteca ou VM ou container toda a imagem será refeita, enquanto que a antiga permanece disponível para casos de necessidade de um rollback. Containers imutáveis estão no cerne do kubernetes. Apesar de possível, não é recomendado a modificação de containers em execução.

### Configuração Declarativa
É o contrário da configuração imperativa. A configuração no `K8s` é feita com a definição de objetos de configuração de como a aplicação deve existir. A configuração declarativa descreve o [[Desired State#Definição | estado desejado]] de algo.

**Imperativa:** Descreve ações que devem ser executadas para se alcançar o estado esperado da aplicação;
**Declarativa:** Descreve todos os elementos necessários para que o estado esperado seja alcançado;

É possível utilizar ferramentas e metodologias utilizadas no desenvolvimento de software, tais como controle de versão, revisão de código e testes unitários.

### Self Healing
Continuamente executa ações para alcançar o estado desejado(idempotência). O daemon não somente criará o que foi declarado, mas continuamente garantirá que o estado desejado seja mantido/ancaçado.

## Escalonamento
A utilização do `k8s` habilita o fácil escalonamento, tanto da solução desenvolvida, quanto da equipe envolvida.

**Desacoplamento:** Permite separar cada parte do sistema de forma a aumentar a facilidade de identificação da necessidade de escalonamento das partes. O Desacoplamento dos times permite a construção de soluções robustas por conta do foco empregado por cada time.

* O tamanho ideal de uma equipe pode ser mensaurada utilizando a técninca `two-pizza team`;
* Para ajudar na implantação de micro serviços, o `k8s` dispõem das seguintes abstrações:
  * **[[Pods]]**: Grupo de containers;
  * **Namespace**:  Provê isolamento e controle de acesso para restringir a interação com os recursos;
  * **Service**: Provê o lanceamento de carga, nomeação e descoberta para isolamento de um microserviço de outro;
  * **Ingress**: Frontend que combina múltiplos micro serviços em uma única API externalizada;

> SE uma parte dos sistema não é escalável, toda a aplicação não é escalável

[[Pods#Conceitos| Vou te contar viu]]
## Abstração da infraestrutura
A infraestrutura é abstraída pois os elementos presentes em uma solução são descritos de maneira abstrata, separando o desenvolvimento da implementação e aproximando as equipes dos conceitos relacionados. A utilização do `k8s` habilita a portabilidade entre infraestrutura _on premises_ e provedores de cloud computing.
> Service -> ALB
> PersistentVolume -> EBS