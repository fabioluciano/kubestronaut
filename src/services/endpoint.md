# Endpoints e EndpointSlices

<span class="badge badge-ckad">CKAD</span> <span class="badge badge-cka">CKA</span>

---

## O que são Endpoints?

```admonish info title="Endpoints"
Endpoints são objetos do Kubernetes que mapeiam um Service para os IPs dos Pods que ele seleciona. Sempre que um Pod é adicionado ou removido, o Endpoint é automaticamente atualizado.
```

### Como funciona

```
Service (selector: app=web)
        ↓
   Endpoints
        ↓
┌───────┬───────┬───────┐
│Pod IP │Pod IP │Pod IP │
│:8080  │:8080  │:8080  │
└───────┴───────┴───────┘
```

### Características

| Aspecto | Descrição |
|---------|-----------|
| **Criação** | Automática quando Service tem selector |
| **Atualização** | Dinâmica conforme Pods sobem/descem |
| **Limite** | Máximo 1000 IPs por Endpoint |
| **Nome** | Mesmo nome do Service associado |

---

## EndpointSlices

```admonish tip title="EndpointSlices"
EndpointSlices foram criados para resolver limitações dos Endpoints tradicionais, oferecendo melhor escalabilidade e performance.
```

### Por que EndpointSlices?

| Problema com Endpoints | Solução com EndpointSlices |
|------------------------|----------------------------|
| Limite de 1000 IPs | Múltiplos slices, 100 endpoints cada |
| Atualização do objeto inteiro | Atualizações incrementais |
| Sem info de topologia | Inclui informações do Node |
| Alto uso de memória | Objetos menores e distribuídos |

### Estrutura do EndpointSlice

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: my-service-abc123
  labels:
    kubernetes.io/service-name: my-service
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 80
endpoints:
  - addresses:
      - "10.1.2.3"
    conditions:
      ready: true
      serving: true
      terminating: false
    nodeName: node-1
    zone: us-east-1a
```

---

## Comandos Úteis

```bash
# Ver endpoints de um service
kubectl get endpoints <service-name>

# Ver endpoints de todos os services
kubectl get endpoints -A

# Detalhes do endpoint
kubectl describe endpoints <service-name>

# Ver EndpointSlices
kubectl get endpointslices

# EndpointSlices de um service específico
kubectl get endpointslices -l kubernetes.io/service-name=<service-name>
```

---

## Endpoints Manuais (Sem Selector)

Quando o Service não tem `selector`, você pode criar Endpoints manualmente para apontar para serviços externos:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  ports:
    - port: 3306
---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-db  # Mesmo nome do Service
subsets:
  - addresses:
      - ip: 192.168.1.100
      - ip: 192.168.1.101
    ports:
      - port: 3306
```

---

## Troubleshooting

### Service sem Endpoints

```bash
# Verificar se há endpoints
kubectl get endpoints <service-name>

# Se vazio, verificar:
# 1. Selector do Service bate com labels dos Pods?
kubectl get svc <service-name> -o yaml | grep -A5 selector
kubectl get pods --show-labels

# 2. Pods estão Ready?
kubectl get pods -l <selector>
```

### Endpoints não atualizam

```bash
# Verificar controller-manager
kubectl logs -n kube-system -l component=kube-controller-manager | grep endpoint
```

---

## Dicas para os Exames

```admonish tip title="Dicas CKA/CKAD"
1. **Endpoint vazio = problema de selector**: Verifique labels dos Pods
2. **Service externo**: Crie Endpoints manuais sem selector
3. **Debug**: `kubectl get endpoints` mostra os IPs dos Pods
4. **EndpointSlices**: API mais nova em `discovery.k8s.io/v1`
```

---

## Referências

- [Services](service.md) - Conceitos de Service
- [DNS](../networking/dns.md) - Resolução de nomes
