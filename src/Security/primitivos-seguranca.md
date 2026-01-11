# Primitivos de Segurança

## Conceitos Fundamentais

### Visão Geral da Segurança Kubernetes

```plantuml,format=png
@startuml
skinparam monochrome true

title CAMADAS DE SEGURANÇA KUBERNETES

rectangle "INFRAESTRUTURA (Host Security)" as infra {
  note as n1
    • SSH keys (não password)
    • Desabilitar root login
    • Firewall/Security groups
    • Atualizações de segurança
  end note
}

rectangle "KUBERNETES (Cluster Security)" as k8s {
  note as n2
    • Authentication (quem você é)
    • Authorization (o que você pode fazer)
    • Admission Control (validação/mutação)
    • TLS entre componentes
  end note
}

rectangle "WORKLOAD (Pod Security)" as workload {
  note as n3
    • Pod Security Admission
    • NetworkPolicy
    • Seccomp/AppArmor
    • RuntimeClass
  end note
}

infra --> k8s
k8s --> workload
@enduml
```

### Primeira Linha de Defesa: kube-apiserver

```plantuml,format=png
@startuml
skinparam monochrome true

title FLUXO DE REQUISIÇÃO NO API SERVER

actor "Requisição\n(kubectl, API)" as req

rectangle "1. AUTHENTICATION (AuthN)" as authn {
  note right
    **Quem é você?**
    • Certificados X.509
    • Bearer Tokens
    • OIDC
  end note
}

rectangle "2. AUTHORIZATION (AuthZ)" as authz {
  note right
    **O que você pode fazer?**
    • RBAC
    • Node
    • Webhook
  end note
}

rectangle "3. ADMISSION CONTROL" as admission {
  note right
    **Validar/Mutar requisição**
    • Validating webhooks
    • Mutating webhooks
  end note
}

entity "4. PERSIST (etcd)" as persist
req --> authn
authn --> authz
authz --> admission
admission --> persist
@enduml
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
@startuml
skinparam monochrome true

map "MÉTODOS DE AUTENTICAÇÃO" as auth {
}

note bottom of auth
  **CERTIFICADOS X.509 (Recomendado)**
  • CN (Common Name) = username
  • O (Organization) = group
  • Usado por kubeadm para componentes

  **BEARER TOKENS**
  • Service Account tokens
  • Bootstrap tokens

  **OIDC (OpenID Connect)**
  • Integração com IdP externo
  • Recomendado para produção

  **STATIC FILES (NÃO RECOMENDADO)**
  • --basic-auth-file (deprecated)
  • --token-auth-file (deprecated)
end note
@enduml
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
@startuml
skinparam monochrome true

map "NODE AUTHORIZER" as node {
}

note bottom of node
  **Autoriza requisições de kubelets:**
  • Usuário: system:node:<nodename>
  • Grupo: system:nodes

  **Permissões:**
  • READ: Services, Endpoints, Nodes, Pods
  • WRITE: Node status, Pod status, Events
end note
@enduml
```

### Ordem de Avaliação

```plantuml,format=png
@startuml
skinparam monochrome true

title ORDEM DE AVALIAÇÃO

note as config
  --authorization-mode=Node,RBAC,Webhook
end note

actor "Requisição" as req
entity "Node" as node
entity "RBAC" as rbac
entity "Webhook" as webhook
entity "AUTORIZADO" as auth
req --> node : avaliar
node --> rbac : DENY
node --> auth : ALLOW
rbac --> webhook : DENY
rbac --> auth : ALLOW
webhook --> auth : ALLOW

note bottom of auth
  **Regras:**
  • Primeiro ALLOW ganha
  • Se todos DENY = não autorizado
end note
@enduml
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
@startuml
skinparam monochrome true

title CERTIFICADOS DO CLUSTER

folder "/etc/kubernetes/pki/" as pki {
  file "ca.crt, ca.key" as ca
  note right of ca : CA do cluster
  
  file "apiserver.crt, apiserver.key" as api
  note right of api : API Server
  
  file "apiserver-kubelet-client.*" as akc
  note right of akc : API → Kubelet
  
  file "front-proxy-ca.*" as fpc
  note right of fpc : Aggregation layer
  
  file "front-proxy-client.*" as fpclient
  note right of fpclient : API → extension servers
  
  file "sa.key, sa.pub" as sa
  note right of sa : Service Account signing
  
  folder "etcd/" as etcddir {
    file "ca.crt, ca.key" as etcdca
    note bottom : etcd CA
    file "server.crt, server.key" as etcdsrv
    note bottom : etcd server
    file "peer.crt, peer.key" as etcdpeer
    note bottom : etcd peer
    file "healthcheck-client.*" as etcdhc
    note bottom : etcd health checks
  }
}
@enduml
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
@startuml
skinparam monochrome true

map "DICAS CKS - PRIMITIVOS DE SEGURANÇA" as dicas {
}

note bottom of dicas
  **FLUXO DE REQUISIÇÃO:**
  1. Authentication (quem é você)
  2. Authorization (o que pode fazer)
  3. Admission Control (validar/mutar)

  **AUTENTICAÇÃO:**
  • Certificados: CN=username, O=group
  • Service Accounts: tokens montados em pods
  • NÃO usar: basic-auth-file, token-auth-file

  **AUTORIZAÇÃO:**
  • --authorization-mode=Node,RBAC (padrão kubeadm)
  • Ordem importa! Primeiro ALLOW ganha

  **VERIFICAR PERMISSÕES:**
  kubectl auth can-i <verb> <resource>
  kubectl auth can-i --list
  kubectl auth can-i create pods --as=myuser

  **KUBECONFIG:**
  • clusters, users, contexts
  • current-context = contexto ativo
  • kubectl config use-context <name>
end note
@enduml
```

---

## Referências

- [RBAC](rbac.md)
- [ServiceAccount](service-account.md)
- [TLS](tls.md)
- [Certificate API](certificate-api.md)
- [Admission Controllers](admission-controllers.md)

