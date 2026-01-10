# Primitivos de Segurança

## Conceitos Fundamentais

### Visão Geral da Segurança Kubernetes

```plantuml,format=png
!include ../assets/diagrams/security/primitivos-seguranca-camadas-de-segurança-kubernetes-1.puml
```

### Primeira Linha de Defesa: kube-apiserver

```plantuml,format=png
!include ../assets/diagrams/security/primitivos-seguranca-fluxo-de-requisição-no-api-server-1.puml
```

---

## Autenticação (Authentication)

### Tipos de Usuários

| Tipo | Descrição | Gerenciado por |
|------|-----------|----------------|
| **Users** | Humanos (admins, developers) | Externo (LDAP, OIDC) |
| **Service Accounts** | Processos/Aplicações | Kubernetes |

### Métodos de Autenticação

```plantuml,format=png
!include ../assets/diagrams/security/primitivos-seguranca-diagram-3-1.puml
```

### Autenticação por Certificados

```bash
# Criar chave privada
openssl genrsa -out user.key 2048

# Criar CSR (Common Name = username, Organization = group)
openssl req -new -key user.key -out user.csr \
  -subj "/CN=myuser/O=developers"

# Assinar com CA do cluster
openssl x509 -req -in user.csr \
  -CA /etc/kubernetes/pki/ca.crt \
  -CAkey /etc/kubernetes/pki/ca.key \
  -CAcreateserial \
  -out user.crt -days 365
```

### Configurar kubeconfig

```bash
# Adicionar credenciais
kubectl config set-credentials myuser \
  --client-certificate=user.crt \
  --client-key=user.key

# Adicionar contexto
kubectl config set-context myuser-context \
  --cluster=kubernetes \
  --user=myuser

# Usar contexto
kubectl config use-context myuser-context
```

### Kubeconfig Estrutura

```yaml
{{#include ../assets/security/kubeconfig-example.yaml}}
```

---

## Autorização (Authorization)

### Modos de Autorização

| Modo | Descrição |
|------|-----------|
| **Node** | Autoriza kubelets (usuários system:node:*) |
| **RBAC** | Role-Based Access Control (recomendado) |
| **Webhook** | Autorização externa via HTTP |
| **ABAC** | Attribute-Based (arquivo JSON, não recomendado) |
| **AlwaysAllow** | Permite tudo (NÃO usar em produção) |
| **AlwaysDeny** | Nega tudo |

### Configuração no API Server

```yaml
{{#include ../assets/security/kube-apiserver-authorization.yaml}}
```

### Node Authorizer

```plantuml,format=png
!include ../assets/diagrams/security/primitivos-seguranca-diagram-4-1.puml
```

### Ordem de Avaliação

```plantuml,format=png
!include ../assets/diagrams/security/primitivos-seguranca-ordem-de-avaliação-1.puml
```

---

## Verificar Permissões

### kubectl auth can-i

```bash
# Verificar próprias permissões
kubectl auth can-i create pods
kubectl auth can-i delete deployments

# Verificar permissões de outro usuário
kubectl auth can-i create pods --as=myuser
kubectl auth can-i delete pods --as=system:serviceaccount:default:mysa

# Verificar em namespace específico
kubectl auth can-i get secrets -n production

# Listar todas as ações permitidas
kubectl auth can-i --list

# Como outro usuário
kubectl auth can-i --list --as=myuser
```

### Verificar Autenticação

```bash
# Ver usuário atual
kubectl config current-context
kubectl config view --minify

# Testar autenticação
kubectl cluster-info

# Ver token de ServiceAccount
kubectl get secret <sa-token> -o jsonpath='{.data.token}' | base64 -d
```

---

## Comunicação TLS

### Certificados do Cluster

```plantuml,format=png
!include ../assets/diagrams/security/primitivos-seguranca-certificados-do-cluster-1.puml
```

### Verificar Certificados

```bash
# Ver detalhes do certificado
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout

# Verificar expiração
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -dates

# Verificar CA
openssl verify -CAfile /etc/kubernetes/pki/ca.crt \
  /etc/kubernetes/pki/apiserver.crt
```

---

## Dicas para o Exame CKS

```plantuml,format=png
!include ../assets/diagrams/security/primitivos-seguranca-diagram-7-1.puml
```

---

## Referências

- [RBAC](rbac.md)
- [ServiceAccount](service-account.md)
- [TLS](tls.md)
- [Certificate API](certificate-api.md)
- [Admission Controllers](admission-controllers.md)

