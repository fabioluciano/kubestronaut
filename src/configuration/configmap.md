# ConfigMaps

```admonish info title="Certificações"
CKAD (20%), CKA (10%)
```

## Conceitos Fundamentais

### O que são ConfigMaps

ConfigMaps são objetos para armazenar dados de configuração não sensíveis em pares chave-valor. Permitem separar configuração do código da aplicação.

```plantuml,format=png
!include ../assets/diagrams/configuration/configmap-configmap-overview.puml
```

### ConfigMap vs Secret

| Característica | ConfigMap | Secret |
|----------------|-----------|--------|
| **Dados** | Não sensíveis | Sensíveis |
| **Encoding** | Texto plano | Base64 |
| **Tamanho máx** | 1 MiB | 1 MiB |
| **Tipos** | Não tem | Vários (generic, tls, docker-registry) |

### Formas de Usar ConfigMap

```plantuml,format=png
!include ../assets/diagrams/configuration/configmap-formas-de-consumir-configmap.puml
```

---

## Comandos Essenciais

### Criar ConfigMaps

```bash
# A partir de literais
kubectl create configmap my-config --from-literal=key1=value1 --from-literal=key2=value2

# A partir de arquivo
kubectl create configmap my-config --from-file=config.txt

# A partir de arquivo com nome de chave específico
kubectl create configmap my-config --from-file=mykey=config.txt

# A partir de diretório (cada arquivo vira uma chave)
kubectl create configmap my-config --from-file=./config-dir/

# A partir de arquivo .env
kubectl create configmap my-config --from-env-file=app.env

# Com dry-run para YAML
kubectl create configmap my-config --from-literal=key=value --dry-run=client -o yaml

# Via arquivo YAML
kubectl apply -f configmap.yaml
```

### Gerenciar ConfigMaps

```bash
# Listar ConfigMaps
kubectl get configmaps
kubectl get cm          # forma curta

# Ver ConfigMaps de todos os namespaces
kubectl get cm -A

# Descrever ConfigMap
kubectl describe cm <name>

# Ver YAML do ConfigMap
kubectl get cm <name> -o yaml

# Ver apenas os dados
kubectl get cm <name> -o jsonpath='{.data}'

# Editar ConfigMap
kubectl edit cm <name>
```

### Deletar ConfigMaps

```bash
# Deletar ConfigMap
kubectl delete cm <name>

# Deletar por arquivo
kubectl delete -f configmap.yaml
```

---

## Exemplos Práticos

### ConfigMap Básico (YAML)

```yaml
{{#include ../assets/configmap/configmap-basico.yaml}}
```

### ConfigMap a Partir de Arquivo

```bash
# Conteúdo do arquivo config.properties
cat <<EOF > config.properties
database.host=mysql
database.port=3306
cache.ttl=300
EOF

# Criar ConfigMap
kubectl create configmap app-config --from-file=config.properties

# O resultado será:
# data:
#   config.properties: |
#     database.host=mysql
#     database.port=3306
#     cache.ttl=300
```

### Pod com Variável de Ambiente (valueFrom)

```yaml
{{#include ../assets/configmap/pod-env-valuefrom.yaml}}
```

### Pod com Todas as Variáveis (envFrom)

```yaml
{{#include ../assets/configmap/pod-envfrom.yaml}}
```

### Pod com Volume (Todos os Arquivos)

```yaml
{{#include ../assets/configmap/pod-volume.yaml}}
```

### Pod com Volume (Items Específicos)

```yaml
{{#include ../assets/configmap/pod-volume-items.yaml}}
```

### Pod com SubPath (Não Sobrescreve Diretório)

```yaml
{{#include ../assets/configmap/pod-subpath.yaml}}
```

### ConfigMap Imutável

```yaml
{{#include ../assets/configmap/configmap-imutavel.yaml}}
```

### Exemplo Completo: Aplicação com ConfigMap

```yaml
{{#include ../assets/configmap/webapp-completo.yaml}}
```

---

## Atualização de ConfigMaps

### Comportamento de Atualização

```plantuml,format=png
!include ../assets/diagrams/configuration/configmap-atualização-de-configmaps.puml
```

### Forçar Atualização com Rollout

```bash
# Método 1: Adicionar annotation com hash do ConfigMap
kubectl patch deployment <name> -p \
  '{"spec":{"template":{"metadata":{"annotations":{"configmap-hash":"'$(kubectl get cm <config> -o yaml | sha256sum | cut -d' ' -f1)'"}}}}}'

# Método 2: Usar kubectl rollout restart
kubectl rollout restart deployment/<name>
```

---

## Troubleshooting

### Problema: Variável de Ambiente Não Aparece

```bash
# Verificar se ConfigMap existe
kubectl get cm <name>

# Verificar chave existe no ConfigMap
kubectl get cm <name> -o jsonpath='{.data.MY_KEY}'

# Ver variáveis dentro do container
kubectl exec <pod> -- env | grep MY_KEY

# Verificar se key está correta no manifest do Pod
kubectl get pod <name> -o yaml | grep -A5 configMapKeyRef
```

### Problema: Arquivo Não Aparece no Volume

```bash
# Verificar se volume está montado
kubectl describe pod <name> | grep -A5 "Mounts:"

# Verificar conteúdo do diretório montado
kubectl exec <pod> -- ls -la /etc/config

# Verificar conteúdo do arquivo
kubectl exec <pod> -- cat /etc/config/<key>
```

### Problema: ConfigMap Não Atualiza no Pod

```bash
# Para volumes: aguardar ~1 minuto para sincronização

# Verificar timestamp do arquivo
kubectl exec <pod> -- stat /etc/config/<file>

# Se usando subPath ou env, restartar pod
kubectl delete pod <name>
# ou
kubectl rollout restart deployment/<name>
```

### Problema: Pod Não Inicia (ConfigMap Não Encontrado)

```bash
# Verificar eventos do Pod
kubectl describe pod <name>

# Mensagem típica:
# "configmap 'my-config' not found"

# Solução: criar ConfigMap ou adicionar optional: true
```

---

## Dicas para o Exame

### CKAD

```admonish tip title="Dicas CKAD"
1. **Criar ConfigMap rápido**:
   ```bash
   kubectl create cm my-config --from-literal=key=value
   ```

2. **Ver dados do ConfigMap**:
   ```bash
   kubectl get cm my-config -o jsonpath='{.data}'
   ```

3. **Três formas de consumir**:
   - `env.valueFrom.configMapKeyRef` - uma variável
   - `envFrom.configMapRef` - todas variáveis
   - `volumes.configMap` - arquivos

4. **Não esquecer o volumeMounts** ao usar volumes

5. **optional: true** para evitar falha se key não existir
```

### CKA

```admonish tip title="Dicas CKA"
1. **ConfigMaps são namespace-scoped**

2. **Limite de 1 MiB** para dados

3. **Atualizações automáticas** apenas para volumes (não subPath, não env)

4. **Imutável**: `immutable: true` para performance
```

### Comandos Úteis para o Exame

```bash
# Criar ConfigMap de literal
kubectl create cm my-cm --from-literal=key=value

# Criar ConfigMap de arquivo
kubectl create cm my-cm --from-file=config.txt

# Criar ConfigMap de env file
kubectl create cm my-cm --from-env-file=app.env

# Ver ConfigMap
kubectl get cm my-cm -o yaml

# Gerar YAML
kubectl create cm my-cm --from-literal=k=v --dry-run=client -o yaml

# Injetar em Deployment existente
kubectl set env deployment/<name> --from=configmap/<cm-name>
```

### Template Rápido: Pod com ConfigMap

```yaml
{{#include ../assets/configmap/pod-template-rapido.yaml}}
```

---

## Referências

- [Kubernetes - ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes - Configure Pod ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)

### Arquivos Relacionados

- [Secrets](secrets.md) - Para dados sensíveis
- [Pod](../workloads/pod.md) - Pods que consomem ConfigMaps
- [Deployment](../workloads/deployment.md) - Deployments com ConfigMaps


---

### Pod com ConfigMap via Env (chave específica)

```yaml
{{#include ../assets/configmap/pod-with-configmap-env-key.yaml}}
```


---

### Pod com ConfigMap via envFrom

```yaml
{{#include ../assets/configmap/pod-with-configmap-env-valuesfrom.yaml}}
```


---

### ConfigMap como Volume (items específicos)

```yaml
{{#include ../assets/configmap/pod-with-configmap-volume-items.yaml}}
```


---

### ConfigMap como Volume

```yaml
{{#include ../assets/configmap/pod-with-configmap-volume.yaml}}
```
