# Kustomize

```admonish info title="Certificações"
CKAD (20%), CKA (15%)
```

## 📖 Conceitos

### O que é

Kustomize é uma ferramenta para customização de configurações Kubernetes sem usar templates. Funciona com patches e overlays sobre recursos base.

### Kustomize vs Helm

| Aspecto | Kustomize | Helm |
|---------|-----------|------|
| Abordagem | Patches/Overlays | Templates |
| Complexidade | Simples | Mais complexo |
| Curva de aprendizado | Baixa | Média |
| Integração kubectl | Nativa (`-k`) | Separada |
| Variáveis | Não usa | Go templates |
| Casos de uso | Customização simples | Aplicações complexas |

### Estrutura de Diretórios

```
app/
├── base/                    # Recursos base
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── overlays/                # Customizações
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patch-replicas.yaml
    └── prod/
        ├── kustomization.yaml
        └── patch-replicas.yaml
```

## 🔧 Comandos Essenciais

```bash
# Aplicar diretamente
kubectl apply -k ./

# Aplicar de diretório específico
kubectl apply -k ./overlays/prod/

# Ver YAML gerado (sem aplicar)
kubectl kustomize ./

# Ou usando kustomize diretamente
kustomize build ./

# Deletar recursos
kubectl delete -k ./
```

## 📝 kustomization.yaml

### Campos Principais

```yaml
{{#include ../assets/kustomize/kustomization-main.yaml}}
```

## 💻 Exemplos Práticos

### Exemplo 1: Base Simples

```yaml
{{#include ../assets/kustomize/base-kustomization.yaml}}
```

```yaml
{{#include ../assets/kustomize/base-deployment.yaml}}
```

```yaml
{{#include ../assets/kustomize/base-service.yaml}}
```

### Exemplo 2: Overlay de Desenvolvimento

```yaml
{{#include ../assets/kustomize/overlay-dev-kustomization.yaml}}
```

### Exemplo 3: Overlay de Produção

```yaml
{{#include ../assets/kustomize/overlay-prod-kustomization.yaml}}
```

```yaml
{{#include ../assets/kustomize/patch-replicas.yaml}}
```

```yaml
{{#include ../assets/kustomize/patch-resources.yaml}}
```

### Exemplo 4: ConfigMap Generator

```yaml
{{#include ../assets/kustomize/configmap-generator.yaml}}
```

### Exemplo 5: Strategic Merge Patch

```yaml
{{#include ../assets/kustomize/strategic-merge-patch-kustomization.yaml}}
```

```yaml
{{#include ../assets/kustomize/add-sidecar.yaml}}
```

### Exemplo 6: JSON 6902 Patch

```yaml
{{#include ../assets/kustomize/json6902-patch.yaml}}
```

## 🐛 Troubleshooting

### Problema: Resource not found

**Causa**: Nome do recurso não corresponde

```bash
# Verificar nome gerado
kubectl kustomize ./ | grep "name:"

# Lembrar que namePrefix/nameSuffix alteram o nome
```

### Problema: Patch não aplicado

**Causa**: Target não corresponde ao recurso

```bash
# Verificar se o target está correto
# name, kind, group devem corresponder exatamente
```

### Problema: ConfigMap hash mudou

**Solução**: Usar `disableNameSuffixHash`

```yaml
{{#include ../assets/kustomize/configmap-hash-fix.yaml}}
```

## 🎓 Dicas para o Exame CKAD

### Comandos Rápidos

```bash
# Ver resultado sem aplicar
kubectl kustomize ./

# Aplicar
kubectl apply -k ./

# Deletar
kubectl delete -k ./
```

### Lembrar

1. `-k` para kustomize (não `-f`)
2. Patches podem ser inline ou arquivo
3. `namePrefix` e `nameSuffix` afetam referências
4. ConfigMapGenerator adiciona hash por padrão

### Estrutura Mínima

```yaml
{{#include ../assets/kustomize/minimal-kustomization.yaml}}
```

## 🔗 Referências

### Documentação
- [Kustomize docs](https://kustomize.io/)
- [kubectl kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- [Kustomize GitHub](https://github.com/kubernetes-sigs/kustomize)

### Arquivos Relacionados
- [Helm](helm.md) - Alternativa com templates
- [ConfigMap](../configuration/configmap.md) - ConfigMaps referenciados
- [Secrets](../configuration/secrets.md) - Secrets gerados
- [Deployment](../workloads/deployment.md) - Deployments customizados
