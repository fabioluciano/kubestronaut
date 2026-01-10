# Certificate API

## Conceitos Fundamentais

### O que é a Certificate API?

A Certificate API do Kubernetes permite criar, aprovar e gerenciar certificados TLS através do cluster. É usada principalmente para criar certificados de usuário para autenticação no cluster.

```plantuml,format=png
!include ../assets/diagrams/security/certificate-api-fluxo-da-certificate-api-1.puml
```

### Componentes

| Componente | Função |
|------------|--------|
| **CSR** | Certificate Signing Request - pedido de assinatura |
| **Controller Manager** | Processa e assina os CSRs |
| **CA** | Certificate Authority do cluster |
| **signerName** | Define qual CA vai assinar |

---

## Criar Certificado de Usuário

### Passo 1: Gerar Chave Privada

```bash
# Gerar chave RSA de 2048 bits
openssl genrsa -out john.key 2048

# Ou 4096 bits (mais seguro)
openssl genrsa -out john.key 4096
```

### Passo 2: Criar CSR (Certificate Signing Request)

```bash
# Criar CSR com informações do usuário
# CN (Common Name) = nome do usuário
# O (Organization) = grupo do usuário (usado pelo RBAC)
openssl req -new -key john.key -out john.csr \
  -subj "/CN=john/O=developers"

# Para múltiplos grupos
openssl req -new -key john.key -out john.csr \
  -subj "/CN=john/O=developers/O=qa"
```

### Passo 3: Codificar CSR em Base64

```bash
# Codificar CSR (remover quebras de linha)
cat john.csr | base64 | tr -d '\n'

# Ou
base64 -w 0 john.csr
```

### Passo 4: Criar CertificateSigningRequest no Kubernetes

```yaml
{{#include ../assets/certificates/csr-john.yaml}}
```

```bash
# Aplicar o CSR
kubectl apply -f csr.yaml

# Ou criar via comando
kubectl apply -f csr-inline.yaml
```

```yaml
{{#include ../assets/certificates/csr-inline.yaml}}
```

### Passo 5: Aprovar o CSR

```bash
# Ver CSRs pendentes
kubectl get csr
# NAME   AGE   SIGNERNAME                            REQUESTOR   CONDITION
# john   10s   kubernetes.io/kube-apiserver-client   admin       Pending

# Aprovar o CSR
kubectl certificate approve john

# Ou rejeitar
kubectl certificate deny john
```

### Passo 6: Obter o Certificado

```bash
# Extrair certificado assinado
kubectl get csr john -o jsonpath='{.status.certificate}' | base64 -d > john.crt

# Verificar o certificado
openssl x509 -in john.crt -text -noout
```

---

## Signer Names

### Signers Disponíveis

```plantuml,format=png
!include ../assets/diagrams/security/certificate-api-diagram-2-1.puml
```

### Usages Válidos

```yaml
{{#include ../assets/certificates/csr-usages.yaml}}
```

---

## Configurar kubectl

### Adicionar Credenciais ao kubeconfig

```bash
# Método 1: Adicionar certificado inline (embed)
kubectl config set-credentials john \
  --client-key=john.key \
  --client-certificate=john.crt \
  --embed-certs=true

# Método 2: Referenciar arquivos (não embed)
kubectl config set-credentials john \
  --client-key=/path/to/john.key \
  --client-certificate=/path/to/john.crt
```

### Criar Context

```bash
# Criar contexto para o usuário
kubectl config set-context john-context \
  --cluster=kubernetes \
  --user=john \
  --namespace=default

# Usar o contexto
kubectl config use-context john-context

# Testar
kubectl get pods

# Voltar ao contexto admin
kubectl config use-context kubernetes-admin@kubernetes
```

### Arquivo kubeconfig Completo

```yaml
{{#include ../assets/certificates/kubeconfig-example.yaml}}
```

---

## Método Alternativo: Assinar com CA Diretamente

Você pode assinar certificados diretamente com a CA do cluster sem usar a Certificate API:

```bash
# Assinar CSR diretamente com CA do cluster
sudo openssl x509 -req -in john.csr \
  -CA /etc/kubernetes/pki/ca.crt \
  -CAkey /etc/kubernetes/pki/ca.key \
  -CAcreateserial \
  -out john.crt \
  -days 365

# Verificar certificado
openssl x509 -in john.crt -text -noout | grep -A1 Subject
```

---

## Comandos Úteis

```bash
# Listar CSRs
kubectl get csr

# Ver detalhes de um CSR
kubectl describe csr john

# Aprovar CSR
kubectl certificate approve john

# Rejeitar CSR
kubectl certificate deny john

# Deletar CSR
kubectl delete csr john

# Ver certificado do CSR aprovado
kubectl get csr john -o jsonpath='{.status.certificate}' | base64 -d

# Verificar condições do CSR
kubectl get csr john -o jsonpath='{.status.conditions}'
```

---

## Exemplo Completo: Novo Usuário

```bash
#!/bin/bash
# Script para criar novo usuário

USERNAME="developer1"
GROUP="developers"

# 1. Gerar chave
openssl genrsa -out ${USERNAME}.key 2048

# 2. Gerar CSR
openssl req -new -key ${USERNAME}.key -out ${USERNAME}.csr \
  -subj "/CN=${USERNAME}/O=${GROUP}"

# 3. Criar CertificateSigningRequest (usando o template abaixo)
kubectl apply -f csr-template-script.yaml
```

```yaml
{{#include ../assets/certificates/csr-template-script.yaml}}
```

```bash
# 4. Aprovar
kubectl certificate approve ${USERNAME}

# 5. Obter certificado
kubectl get csr ${USERNAME} -o jsonpath='{.status.certificate}' | \
  base64 -d > ${USERNAME}.crt

# 6. Configurar kubectl
kubectl config set-credentials ${USERNAME} \
  --client-key=${USERNAME}.key \
  --client-certificate=${USERNAME}.crt \
  --embed-certs=true

kubectl config set-context ${USERNAME}-context \
  --cluster=kubernetes \
  --user=${USERNAME}

echo "Usuário ${USERNAME} criado com sucesso!"
echo "Use: kubectl config use-context ${USERNAME}-context"
```

---

## Troubleshooting

### CSR Pending por muito tempo

```bash
# Verificar se controller-manager está rodando
kubectl get pods -n kube-system | grep controller-manager

# Verificar logs do controller-manager
kubectl logs -n kube-system kube-controller-manager-<node>

# Verificar se CA está configurada
ls -la /etc/kubernetes/pki/ca.*
```



### CSR para Novo Usuário

```yaml
{{#include ../assets/certificates/csr-new-user.yaml}}
```
### CSR Manifest

```yaml
{{#include ../assets/certificates/certificatesignrequest.yaml}}
```
### Certificado Rejeitado

```bash
# Ver motivo da rejeição
kubectl describe csr john

# Verificar conditions
kubectl get csr john -o yaml | grep -A5 conditions
```

### Erro de Autenticação

```bash
# Verificar se certificado é válido
openssl verify -CAfile /etc/kubernetes/pki/ca.crt john.crt

# Verificar CN e O
openssl x509 -in john.crt -subject -noout

# Verificar expiração
openssl x509 -in john.crt -enddate -noout
```

---

## Dicas para o Exame CKA/CKS

```plantuml,format=png
!include ../assets/diagrams/security/certificate-api-diagram-3-1.puml
```

---

## Referências

- [TLS](tls.md)
- [RBAC](rbac.md)
- [ServiceAccount](service-account.md)
- [kube-controller-manager](../cluster-components/kube-controller-manager.md)


---

### Certificate com cert-manager

```yaml
{{#include ../assets/certificates/cert-manager-certificate.yaml}}
```
