# ReplicaSet

> **Certificacoes**: CKAD, CKA | **Peso no Exame**: ~5-10%

## Conceitos Fundamentais

Um **ReplicaSet** e um controller do Kubernetes responsavel por garantir que um numero especificado de replicas de um Pod esteja sempre em execucao. Ele e o mecanismo principal por tras da alta disponibilidade de aplicacoes no Kubernetes.

### O que e e Para que Serve

O ReplicaSet tem como objetivo principal:

- **Garantir disponibilidade**: Manter sempre o numero desejado de Pods em execucao
- **Self-healing**: Recriar Pods automaticamente quando falham ou sao deletados
- **Escalabilidade**: Permitir escalar aplicacoes horizontalmente
- **Substituicao de Pods**: Criar novos Pods quando os existentes tornam-se indisponiveis

```admonish info title="Importante"
Na pratica, voce raramente criara ReplicaSets diretamente. O objeto **Deployment** e recomendado para gerenciar ReplicaSets de forma declarativa, pois oferece funcionalidades adicionais como rollbacks e atualizacoes controladas.
```

### Arquitetura do ReplicaSet

```plantuml,format=png
!include ../assets/diagrams/workloads/replicaset-arquitetura-do-replicaset-1.puml
```

## ReplicaSet vs ReplicationController

O **ReplicationController** foi o predecessor do ReplicaSet e ainda funciona, porem e considerado **legado**. As principais diferencas sao:

| Caracteristica | ReplicationController | ReplicaSet |
|----------------|----------------------|------------|
| API Version | `v1` | `apps/v1` |
| Selector | Apenas `equality-based` | `equality-based` e `set-based` |
| Operadores | Apenas `=`, `==`, `!=` | `In`, `NotIn`, `Exists`, `DoesNotExist` |
| Usado por Deployments | Nao | Sim |
| Status | Legado | Recomendado |

### Exemplo de ReplicationController (Legado)

```yaml
{{#include ../assets/replicaset/teste-replicationcontroller.yaml}}
```

```admonish warning title="Atencao"
O ReplicationController e considerado **obsoleto**. Use sempre ReplicaSet ou, preferencialmente, Deployment.
```

## Labels e Selectors

Os selectors sao fundamentais para o funcionamento do ReplicaSet, pois determinam quais Pods serao gerenciados.

### Diagrama de Selecao de Pods

```plantuml,format=png
!include ../assets/diagrams/workloads/replicaset-selecao-de-pods-pelo-replicaset-1.puml
```

### matchLabels

O `matchLabels` usa correspondencia exata de chave-valor:

```yaml
{{#include ../assets/workloads/replicaset-example-1.yaml}}
```

Isso seleciona Pods que tenham **AMBAS** as labels com os valores exatos.

### matchExpressions

O `matchExpressions` oferece mais flexibilidade com operadores logicos:

```yaml
{{#include ../assets/replicaset/replicaset-operadores.yaml}}
```

#### Operadores Disponiveis

| Operador | Descricao | Exemplo |
|----------|-----------|---------|
| `In` | Valor deve estar na lista | `operator: In, values: [v1, v2]` |
| `NotIn` | Valor NAO deve estar na lista | `operator: NotIn, values: [deprecated]` |
| `Exists` | A chave deve existir (valor ignorado) | `operator: Exists` |
| `DoesNotExist` | A chave NAO deve existir | `operator: DoesNotExist` |

### Exemplo Completo com matchExpressions

```yaml
{{#include ../assets/replicaset/replicaset-match-expressions.yaml}}
```

## Relacao com Deployments

Os Deployments gerenciam ReplicaSets automaticamente. Quando voce cria um Deployment, ele cria um ReplicaSet por baixo dos panos.

```plantuml,format=png
!include ../assets/diagrams/workloads/replicaset-hierarquia-deployment-replicaset-pod-1.puml
```

```admonish tip title="Dica para o Exame"
Na prova, sempre pergunte a si mesmo: "Devo usar um ReplicaSet diretamente ou um Deployment?" Na maioria dos casos, a resposta e **Deployment**.
```

## Exemplos YAML Completos



### ReplicaSet com matchExpressions

```yaml
{{#include ../assets/replicaset/teste-replicaset-matchexpressions.yaml}}
```
### ReplicaSet com matchLabels

```yaml
{{#include ../assets/replicaset/teste-replicaset-matchlabels.yaml}}
```
### ReplicaSet Basico

```yaml
{{#include ../assets/replicaset/replicaset-basico.yaml}}
```

### Template Rapido para Exame

```yaml
{{#include ../assets/replicaset/replicaset-template.yaml}}
```

### ReplicaSet com Probes

```yaml
{{#include ../assets/replicaset/replicaset-probes.yaml}}
```

## Orphan Pods e Adocao

### O que sao Orphan Pods?

Quando um ReplicaSet e deletado com a flag `--cascade=orphan`, os Pods criados por ele continuam existindo, mas sem "dono". Esses sao chamados de **Orphan Pods**.

### Adocao de Pods

Um ReplicaSet pode "adotar" Pods existentes que correspondam ao seu selector, mesmo que nao tenham sido criados por ele:

```yaml
{{#include ../assets/replicaset/replicaset-adopt-pods.yaml}}
```

```plantuml,format=png
!include ../assets/diagrams/workloads/replicaset-processo-de-adocao-de-pods-1.puml
```

### Demonstracao Pratica

```bash
# 1. Criar um Pod standalone com a label
kubectl run orphan-pod --image=nginx --labels="app=adopt-me"

# 2. Verificar que o Pod nao tem ownerReferences
kubectl get pod orphan-pod -o jsonpath='{.metadata.ownerReferences}'
# Resultado: vazio

# 3. Criar o ReplicaSet com selector correspondente
kubectl apply -f replicaset-adopt-pods.yaml

# 4. Verificar que o Pod foi adotado
kubectl get pod orphan-pod -o jsonpath='{.metadata.ownerReferences[0].kind}'
# Resultado: ReplicaSet

# 5. O ReplicaSet criara apenas 2 novos Pods (3 - 1 existente)
kubectl get pods -l app=adopt-me
```

```admonish warning title="Cuidado com Adocao Indesejada"
Se voce criar um ReplicaSet com um selector muito generico, ele pode adotar Pods que voce nao pretendia gerenciar. Sempre use selectors especificos!
```

## Scaling Manual

### Via kubectl scale

```bash
# Escalar para 5 replicas
kubectl scale replicaset my-rs --replicas=5

# Escalar usando arquivo
kubectl scale -f replicaset.yaml --replicas=10
```

### Via kubectl edit

```bash
# Editar o ReplicaSet diretamente
kubectl edit replicaset my-rs
# Alterar spec.replicas e salvar
```

### Via kubectl patch

```bash
# Patch para alterar replicas
kubectl patch replicaset my-rs -p '{"spec":{"replicas":7}}'

# Ou usando JSON patch
kubectl patch replicaset my-rs --type='json' \
  -p='[{"op": "replace", "path": "/spec/replicas", "value":7}]'
```

## Comandos kubectl Essenciais

### Operacoes Basicas

```bash
# Listar ReplicaSets
kubectl get replicaset
kubectl get rs  # forma curta

# Listar com mais detalhes
kubectl get rs -o wide

# Descrever um ReplicaSet
kubectl describe rs my-replicaset

# Criar a partir de arquivo
kubectl apply -f replicaset.yaml
kubectl create -f replicaset.yaml

# Deletar ReplicaSet (e seus Pods)
kubectl delete rs my-replicaset

# Deletar ReplicaSet mantendo Pods (orphan)
kubectl delete rs my-replicaset --cascade=orphan
```

### Scaling e Monitoramento

```bash
# Escalar
kubectl scale rs my-rs --replicas=5

# Ver eventos do ReplicaSet
kubectl describe rs my-rs | grep -A 10 Events

# Ver Pods do ReplicaSet
kubectl get pods -l app=my-app

# Ver logs de todos os Pods do ReplicaSet
kubectl logs -l app=my-app --all-containers
```

### Geracao de Template

```bash
# Gerar YAML de ReplicaSet a partir de Pod existente (nao existe diretamente)
# Use Deployment e extraia o ReplicaSet:
kubectl create deployment temp --image=nginx --dry-run=client -o yaml | \
  sed 's/Deployment/ReplicaSet/' | \
  grep -v 'strategy\|status'
```

## Troubleshooting

### Pods nao estao sendo criados

```bash
# Verificar eventos do ReplicaSet
kubectl describe rs my-rs

# Verificar se ha recursos disponiveis
kubectl describe nodes | grep -A 5 "Allocated resources"

# Verificar ResourceQuotas
kubectl get resourcequota -A
```

### Pods em estado Pending

```bash
# Verificar eventos do Pod
kubectl describe pod <pod-name>

# Causas comuns:
# - Insufficient CPU/Memory
# - No nodes match nodeSelector
# - PersistentVolumeClaim not bound
```

### ReplicaSet nao escala

```bash
# Verificar se ha LimitRange ou ResourceQuota
kubectl get limitrange,resourcequota -A

# Verificar PodDisruptionBudget
kubectl get pdb -A
```

### Selector nao corresponde

```bash
# Verificar labels dos Pods
kubectl get pods --show-labels

# Verificar selector do ReplicaSet
kubectl get rs my-rs -o jsonpath='{.spec.selector}'

# Labels do template devem corresponder ao selector!
```

## Dicas para o Exame

```admonish tip title="Dicas CKAD/CKA"
1. **Nao crie ReplicaSets diretamente** - Use Deployments na maioria dos cenarios do exame

2. **Memorize o template basico**:
   - `apiVersion: apps/v1`
   - `kind: ReplicaSet`
   - `spec.replicas`, `spec.selector`, `spec.template`

3. **Labels DEVEM corresponder**:
   - `spec.selector.matchLabels` DEVE corresponder a `spec.template.metadata.labels`

4. **Comando rapido de scaling**:
   ```bash
   kubectl scale rs <nome> --replicas=<n>
   ```

5. **Verificar rapidamente replicas**:
   ```bash
   kubectl get rs
   # DESIRED  CURRENT  READY
   ```

6. **Se o exame pedir ReplicaSet especificamente**, pode ser para testar conhecimento de selectors avancados (matchExpressions)
```

## Best Practices

1. **Use Deployments em vez de ReplicaSets diretos** para ter controle de versao e rollback

2. **Defina sempre resource requests e limits** nos containers do template

3. **Use labels descritivas e consistentes** para facilitar selecao e organizacao

4. **Configure probes (liveness e readiness)** para garantir que apenas Pods saudaveis recebam trafego

5. **Evite selectors muito genericos** para prevenir adocao indesejada de Pods

6. **Monitore eventos do ReplicaSet** para identificar problemas de scheduling

## Referencias

- [Documentacao Oficial - ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- [Documentacao Oficial - Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
- [Documentacao Oficial - ReplicationController (Legado)](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/)
