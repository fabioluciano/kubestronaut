# kubectl

```admonish info title="Certificações"
KCNA (18%), CKA (25%), CKAD (25%), CKS (10%)
```

## 📖 Conceitos Fundamentais

### O que é kubectl

`kubectl` é a CLI oficial para interagir com clusters Kubernetes. Comunica-se com o API Server usando REST API sobre HTTPS.

```plantuml,format=png
!include ../assets/diagrams/tools/kubectl-fluxo-do-kubectl-1.puml
```

### Configuração Essencial para Exames

```bash
# PRIMEIRO COMANDO NO EXAME - habilitar autocomplete
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc

# Criar alias (economiza MUITO tempo)
alias k=kubectl
complete -o default -F __start_kubectl k

# Alias para dry-run (usar sempre!)
export do="--dry-run=client -o yaml"

# Exemplos de uso do alias
k run nginx --image=nginx $do > pod.yaml
k create deploy nginx --image=nginx $do > deploy.yaml
```

## 🔧 Comandos por Categoria

### Operações CRUD Básicas

```bash
# CREATE - Criar recursos
kubectl create -f arquivo.yaml
kubectl create deployment nginx --image=nginx
kubectl create namespace dev
kubectl create configmap config --from-literal=key=value
kubectl create secret generic secret --from-literal=pass=123

# READ - Listar/Ler recursos
kubectl get pods                    # listar pods
kubectl get pods -o wide            # com mais info (IP, Node)
kubectl get pods -o yaml            # formato YAML completo
kubectl get pods -o json            # formato JSON
kubectl get pods --show-labels      # mostrar labels
kubectl get all                     # todos os recursos básicos
kubectl get all -A                  # em todos namespaces

# UPDATE - Atualizar recursos
kubectl apply -f arquivo.yaml       # criar ou atualizar
kubectl edit pod nginx              # editar interativamente
kubectl patch pod nginx -p '{"spec":{"containers":[{"name":"nginx","image":"nginx:1.21"}]}}'
kubectl replace -f arquivo.yaml     # substituir completamente

# DELETE - Remover recursos
kubectl delete pod nginx
kubectl delete -f arquivo.yaml
kubectl delete pod nginx --force --grace-period=0  # forçar remoção
kubectl delete pods --all           # todos os pods do namespace
```

### Gerar YAML (Dry-Run)

```bash
# CRÍTICO PARA O EXAME - nunca escreva YAML do zero!

# Pod
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml

# Pod com comando
kubectl run busybox --image=busybox --dry-run=client -o yaml \
  --command -- sleep 3600 > pod-command.yaml

# Pod com porta
kubectl run nginx --image=nginx --port=80 --dry-run=client -o yaml

# Deployment
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deploy.yaml

# Deployment com replicas
kubectl create deployment nginx --image=nginx --replicas=3 --dry-run=client -o yaml

# Service ClusterIP
kubectl create service clusterip nginx --tcp=80:80 --dry-run=client -o yaml

# Service NodePort
kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml

# Job
kubectl create job myjob --image=busybox --dry-run=client -o yaml -- echo "hello"

# CronJob
kubectl create cronjob mycron --image=busybox --schedule="*/5 * * * *" --dry-run=client -o yaml -- date

# ConfigMap
kubectl create configmap config --from-literal=key=value --dry-run=client -o yaml

# Secret
kubectl create secret generic secret --from-literal=pass=123 --dry-run=client -o yaml

# ServiceAccount
kubectl create serviceaccount mysa --dry-run=client -o yaml

# Role
kubectl create role pod-reader --verb=get,list --resource=pods --dry-run=client -o yaml

# RoleBinding
kubectl create rolebinding pod-reader-binding --role=pod-reader --user=jane --dry-run=client -o yaml

# ClusterRole
kubectl create clusterrole pod-reader --verb=get,list --resource=pods --dry-run=client -o yaml

# Ingress (requer namespace)
kubectl create ingress myingress --rule="host/path=service:80" --dry-run=client -o yaml
```

### Expor Serviços

```bash
# Expor deployment como ClusterIP
kubectl expose deployment nginx --port=80 --target-port=80

# Expor como NodePort
kubectl expose deployment nginx --port=80 --type=NodePort

# Expor como LoadBalancer
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Expor pod diretamente
kubectl expose pod nginx --port=80 --name=nginx-svc

# Com dry-run para YAML
kubectl expose deployment nginx --port=80 --dry-run=client -o yaml > svc.yaml
```

### Scaling e Rollouts

```bash
# Escalar replicas
kubectl scale deployment nginx --replicas=5
kubectl scale replicaset myrs --replicas=3

# Autoscaling (HPA)
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80

# Ver histórico de rollout
kubectl rollout history deployment nginx
kubectl rollout history deployment nginx --revision=2

# Status do rollout
kubectl rollout status deployment nginx

# Rollback
kubectl rollout undo deployment nginx
kubectl rollout undo deployment nginx --to-revision=1

# Pausar/Retomar rollout
kubectl rollout pause deployment nginx
kubectl rollout resume deployment nginx

# Restart dos pods (nova imagem)
kubectl rollout restart deployment nginx
```

### Debug e Troubleshooting

```bash
# Ver logs
kubectl logs pod-name
kubectl logs pod-name -c container-name    # container específico
kubectl logs pod-name --previous           # container anterior (crash)
kubectl logs pod-name -f                   # follow (tempo real)
kubectl logs pod-name --tail=100           # últimas 100 linhas
kubectl logs -l app=nginx                  # por label

# Executar comandos no container
kubectl exec pod-name -- ls /
kubectl exec -it pod-name -- /bin/bash     # shell interativo
kubectl exec -it pod-name -c container -- sh  # container específico

# Port-forward (acesso local)
kubectl port-forward pod/nginx 8080:80     # localhost:8080 -> pod:80
kubectl port-forward svc/nginx 8080:80     # via service
kubectl port-forward deployment/nginx 8080:80

# Copiar arquivos
kubectl cp pod-name:/path/file ./local-file
kubectl cp ./local-file pod-name:/path/file

# Debug com container efêmero (k8s 1.25+)
kubectl debug pod-name -it --image=busybox --target=container-name

# Debug de node
kubectl debug node/worker-1 -it --image=busybox

# Top (requer metrics-server)
kubectl top nodes
kubectl top pods
kubectl top pods --containers

# Describe (eventos e erros)
kubectl describe pod nginx
kubectl describe node worker-1
kubectl describe pvc my-pvc

# Ver eventos do namespace
kubectl get events --sort-by='.lastTimestamp'
kubectl get events --field-selector type=Warning
```

### Seletores e Filtros

```bash
# Por label
kubectl get pods -l app=nginx
kubectl get pods -l 'app in (nginx,apache)'
kubectl get pods -l app!=nginx
kubectl get pods -l 'env in (prod,staging)'

# Por field selector
kubectl get pods --field-selector status.phase=Running
kubectl get pods --field-selector spec.nodeName=worker-1
kubectl get pods --field-selector metadata.namespace=default

# Combinar label e field selector
kubectl get pods -l app=nginx --field-selector status.phase=Running

# Todos namespaces
kubectl get pods -A
kubectl get pods --all-namespaces

# Com custom columns
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP

# Sort
kubectl get pods --sort-by='.status.startTime'
kubectl get pods --sort-by='.metadata.creationTimestamp'
kubectl get pv --sort-by='.spec.capacity.storage'
```

### JSONPath e Formatação

```bash
# JSONPath básico
kubectl get pods -o jsonpath='{.items[*].metadata.name}'

# Com quebra de linha
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'

# Múltiplos campos
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'

# Filtrar por condição
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'

# Custom columns (alternativa a jsonpath)
kubectl get pods -o custom-columns='NAME:.metadata.name,NODE:.spec.nodeName'

# Pegar apenas o valor de um campo
kubectl get secret mysecret -o jsonpath='{.data.password}' | base64 -d

# Listar todas as imagens
kubectl get pods -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u

# Pegar IP do node
kubectl get node worker-1 -o jsonpath='{.status.addresses[?(@.type=="InternalIP")].address}'
```

### Labels e Annotations

```bash
# Adicionar label
kubectl label pod nginx env=prod
kubectl label pods --all env=prod

# Sobrescrever label
kubectl label pod nginx env=staging --overwrite

# Remover label
kubectl label pod nginx env-

# Adicionar annotation
kubectl annotate pod nginx description="my pod"

# Remover annotation
kubectl annotate pod nginx description-
```

### Taints e Tolerations

```bash
# Adicionar taint
kubectl taint node worker-1 key=value:NoSchedule
kubectl taint node worker-1 dedicated=gpu:NoExecute

# Remover taint
kubectl taint node worker-1 key=value:NoSchedule-
kubectl taint node worker-1 key-

# Ver taints do node
kubectl describe node worker-1 | grep Taint
```

### Cordon, Drain, Uncordon

```bash
# Cordon - marcar node como unschedulable
kubectl cordon worker-1

# Drain - evacuar pods do node
kubectl drain worker-1 --ignore-daemonsets --force
kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data

# Uncordon - permitir scheduling novamente
kubectl uncordon worker-1
```

### Contextos e Namespaces

```bash
# Ver contexto atual
kubectl config current-context

# Listar contextos
kubectl config get-contexts

# Mudar contexto
kubectl config use-context prod-cluster

# Ver configuração
kubectl config view
kubectl config view --minify  # apenas contexto atual

# Setar namespace padrão
kubectl config set-context --current --namespace=dev

# Criar contexto
kubectl config set-context dev-context --cluster=dev --user=dev-user --namespace=dev
```

### API Resources e Explain

```bash
# Listar todos os recursos disponíveis
kubectl api-resources

# Recursos com shortnames
kubectl api-resources --namespaced=true   # só namespaced
kubectl api-resources --namespaced=false  # cluster-scoped
kubectl api-resources -o wide             # com verbos

# Versões da API
kubectl api-versions

# Explain - documentação inline
kubectl explain pod
kubectl explain pod.spec
kubectl explain pod.spec.containers
kubectl explain pod.spec.containers.resources
kubectl explain pod --recursive  # estrutura completa
kubectl explain pod --recursive | less
```

### Verificar Saúde do Cluster

```bash
# Status dos componentes
kubectl get componentstatuses  # deprecated, mas ainda funciona
kubectl get cs

# Verificar API Server
kubectl cluster-info
kubectl get --raw='/healthz?verbose'
kubectl get --raw='/readyz?verbose'

# Verificar nodes
kubectl get nodes
kubectl describe nodes

# Verificar pods do sistema
kubectl get pods -n kube-system
```

## 📝 Exemplos Práticos para Exame

### Criar Pod com Recursos

```bash
# Gerar YAML base
kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml

# Editar para adicionar recursos
vi pod.yaml
```

```yaml
{{#include ../assets/kubectl/pod-com-recursos.yaml}}
```

### Criar Service para Pod Existente

```bash
# Pod já existe
kubectl get pod nginx

# Criar service apontando para ele
kubectl expose pod nginx --port=80 --name=nginx-svc --type=ClusterIP
```

### Troubleshooting Rápido

```bash
# 1. Pod não inicia - verificar eventos
kubectl describe pod failing-pod | tail -20

# 2. Ver logs do pod anterior
kubectl logs failing-pod --previous

# 3. Verificar se imagem existe
kubectl run test --image=nginx:wrongtag --dry-run=server

# 4. Verificar recursos do node
kubectl top nodes
kubectl describe node worker-1 | grep -A5 "Allocated resources"

# 5. Verificar se PVC está bound
kubectl get pvc
kubectl describe pvc my-pvc
```

## 💡 Dicas para Exame

### Atalhos Essenciais

```plantuml,format=png
!include ../assets/diagrams/tools/kubectl-setup-inicial-do-exame-1.puml
```

### Shortnames Importantes

| Recurso | Shortname | Comando |
|---------|-----------|---------|
| pods | po | `k get po` |
| services | svc | `k get svc` |
| deployments | deploy | `k get deploy` |
| replicasets | rs | `k get rs` |
| namespaces | ns | `k get ns` |
| nodes | no | `k get no` |
| configmaps | cm | `k get cm` |
| secrets | - | `k get secrets` |
| persistentvolumes | pv | `k get pv` |
| persistentvolumeclaims | pvc | `k get pvc` |
| serviceaccounts | sa | `k get sa` |
| ingresses | ing | `k get ing` |
| networkpolicies | netpol | `k get netpol` |
| storageclasses | sc | `k get sc` |

### Comandos Mais Usados no Exame

```bash
# Gerar YAML rapidamente
k run pod --image=img $do > pod.yaml
k create deploy name --image=img $do > deploy.yaml
k expose deploy name --port=80 $do > svc.yaml

# Verificar erros
k describe pod name | tail -20
k logs pod-name --previous
k get events --sort-by='.lastTimestamp'

# Edição rápida
k edit pod name
k set image deploy/name container=newimage

# Forçar recriação
k replace -f file.yaml --force
k delete pod name --force --grace-period=0
```

## 🔍 Troubleshooting

### kubectl não conecta

```bash
# Verificar kubeconfig
echo $KUBECONFIG
cat ~/.kube/config

# Testar conectividade
kubectl cluster-info
curl -k https://<api-server>:6443/healthz

# Verificar certificados
kubectl config view --raw
```

### Comando lento

```bash
# Especificar namespace (evita buscar em todos)
kubectl get pods -n specific-namespace

# Usar field selectors para filtrar no server
kubectl get pods --field-selector status.phase=Running
```

## 📚 Referências

### Links Internos
- [API](api/api.md)
- [kubeadm](kubeadm.md)
- [crictl](crictl.md)
- [Kustomize](kustomize.md)
- [Helm](helm.md)
- [RBAC](../security/rbac.md)

### Documentação Oficial
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [JSONPath Support](https://kubernetes.io/docs/reference/kubectl/jsonpath/)
- [Managing Resources](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/)

---

> **Resumo**: kubectl é a ferramenta CLI essencial para todos os exames Kubernetes. Configure autocomplete e aliases no início do exame. Use `--dry-run=client -o yaml` para gerar YAML. Domine os comandos de debug (logs, describe, exec) e os seletores (labels, field-selectors, jsonpath). Shortnames economizam tempo: `k get po`, `k get svc`, `k get deploy`.
