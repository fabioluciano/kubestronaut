# Minimizar Acesso à GUI e Elementos Externos

## Conceitos Fundamentais

### Por que Minimizar Acesso GUI?

O Kubernetes Dashboard e outras interfaces gráficas representam **superfícies de ataque adicionais**. No contexto do CKS, a recomendação é:

1. **Evitar expor** o Dashboard publicamente
2. **Usar kubectl proxy** para acesso local quando necessário
3. **Aplicar RBAC restritivo** para limitar permissões
4. **Preferir kubectl** sobre interfaces gráficas em produção

### Riscos do Dashboard

```plantuml,format=png
!include ../assets/diagrams/security/minimizar-acesso-gui-riscos-do-dashboard-1.puml
```

---

## Instalação Segura do Dashboard

### Verificar se Dashboard está Instalado

```bash
# Verificar deployment
kubectl get deployment -n kubernetes-dashboard

# Verificar se está exposto externamente
kubectl get svc -n kubernetes-dashboard
```

### Tipo de Serviço Recomendado

```yaml
{{#include ../assets/security/dashboard/service-nodeport-inseguro.yaml}}
```

```yaml
{{#include ../assets/security/dashboard/service-clusterip-seguro.yaml}}
```

---

## Métodos de Acesso Seguro

### 1. kubectl proxy (Recomendado)

```bash
# Iniciar proxy local
kubectl proxy

# Acessar via localhost (autenticação automática)
# http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

### 2. kubectl port-forward

```bash
# Port-forward direto para o pod
kubectl port-forward -n kubernetes-dashboard svc/kubernetes-dashboard 8443:443

# Acessar via https://localhost:8443
```

### 3. Token de Acesso (se necessário)

```bash
# Criar ServiceAccount dedicado
kubectl create serviceaccount dashboard-admin -n kubernetes-dashboard

# Criar token (Kubernetes 1.24+)
kubectl create token dashboard-admin -n kubernetes-dashboard --duration=1h

# Para versões anteriores
kubectl -n kubernetes-dashboard describe secret \
  $(kubectl -n kubernetes-dashboard get secret | grep dashboard-admin | awk '{print $1}')
```

---

## RBAC para Dashboard

### ServiceAccount com Permissões Mínimas

```yaml
{{#include ../assets/security/dashboard/rbac-dashboard-viewer.yaml}}
```

```admonish danger title="EVITAR: Admin ClusterRoleBinding"
Este exemplo mostra o que **NÃO** fazer - conceder acesso admin irrestrito ao Dashboard é um risco de segurança grave.
```

```yaml
{{#include ../assets/security/dashboard/rbac-admin-inseguro.yaml}}
```

---

## Configurações de Segurança do Dashboard

### Argumentos Recomendados

```yaml
{{#include ../assets/security/dashboard/deployment-args-seguros.yaml}}
```

---

## Outras GUIs e Ferramentas Externas

### Lens, Octant, K9s

| Ferramenta | Tipo | Risco | Recomendação |
|------------|------|-------|--------------|
| **Lens** | Desktop | Baixo | Usa kubeconfig local |
| **Octant** | Desktop | Baixo | Usa kubeconfig local |
| **K9s** | Terminal | Baixo | Usa kubeconfig local |
| **Rancher** | Web | Alto | Requer hardening |
| **Portainer** | Web | Alto | Evitar em prod |

### Princípio Geral

```plantuml,format=png
!include ../assets/diagrams/security/minimizar-acesso-gui-princípio-de-minimização-1.puml
```

---

## Auditoria de Elementos Externos

### Verificar Exposições

```bash
# Listar todos os serviços NodePort
kubectl get svc -A -o jsonpath='{range .items[?(@.spec.type=="NodePort")]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'

# Listar todos os serviços LoadBalancer
kubectl get svc -A -o jsonpath='{range .items[?(@.spec.type=="LoadBalancer")]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'

# Verificar Ingress expostos
kubectl get ingress -A
```

### Script de Auditoria

```bash
#!/bin/bash
echo "=== Serviços Expostos Externamente ==="
echo ""
echo "NodePort Services:"
kubectl get svc -A | grep NodePort
echo ""
echo "LoadBalancer Services:"
kubectl get svc -A | grep LoadBalancer
echo ""
echo "Dashboard Status:"
kubectl get all -n kubernetes-dashboard 2>/dev/null || echo "Dashboard não instalado"
```

---

## Troubleshooting

### Dashboard Inacessível

```bash
# Verificar pods
kubectl get pods -n kubernetes-dashboard

# Verificar logs
kubectl logs -n kubernetes-dashboard -l k8s-app=kubernetes-dashboard

# Verificar certificados
kubectl get secret -n kubernetes-dashboard kubernetes-dashboard-certs
```

### Erro de Autenticação

```bash
# Verificar ServiceAccount
kubectl get sa -n kubernetes-dashboard

# Verificar tokens
kubectl get secrets -n kubernetes-dashboard

# Testar token manualmente
TOKEN=$(kubectl create token dashboard-admin -n kubernetes-dashboard)
curl -k -H "Authorization: Bearer $TOKEN" https://localhost:8443/api/v1/namespaces
```

---

## Dicas para o Exame CKS

```plantuml,format=png
!include ../assets/diagrams/security/minimizar-acesso-gui-dicas-cks-dashboard-1.puml
```

---

## Referências

- [Hardening](hardening.md)
- [RBAC](rbac.md)
- [ServiceAccount](service-account.md)
- [NetworkPolicy](network-policy.md)
- [Ingress Security](ingress.md)
