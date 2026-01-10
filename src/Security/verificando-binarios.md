# Verificando Binários do Kubernetes

## Conceitos Fundamentais

### Por que Verificar Binários?

A verificação de binários é uma prática essencial de **Supply Chain Security** que garante:

1. **Integridade**: O arquivo não foi corrompido durante download
2. **Autenticidade**: O arquivo veio realmente do Kubernetes
3. **Segurança**: Não houve adulteração maliciosa (man-in-the-middle)

```plantuml,format=png
!include ../assets/diagrams/security/verificando-binarios-supply-chain-attack-1.puml
```

---

## Métodos de Verificação

### 1. SHA256/SHA512 Checksum

O método mais comum para verificar integridade:

```bash
# Baixar binário do kubectl
curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl"

# Baixar o checksum SHA256
curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl.sha256"

# Verificar (deve retornar "kubectl: OK")
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
```

### Para SHA512

```bash
# Baixar checksum SHA512
curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl.sha512"

# Verificar
echo "$(cat kubectl.sha512)  kubectl" | sha512sum --check
```

### Verificação Manual

```bash
# Calcular hash do binário baixado
sha256sum kubectl
# Saída: 3d21e9f8a0e1f32d26b2c3c8b4a5e6f7... kubectl

# Comparar com hash oficial
cat kubectl.sha256
# Deve ser IDÊNTICO ao calculado acima

# Ou em uma linha
sha256sum kubectl | awk '{print $1}' && cat kubectl.sha256
```

---

## Verificando Binários Existentes

### Verificar Binários em Execução

```bash
# Encontrar caminho do binário
which kubectl
which kubelet
which kubeadm

# Verificar hash do binário instalado
sha256sum /usr/bin/kubectl
sha256sum /usr/bin/kubelet
sha256sum /usr/bin/kubeadm
```

### Comparar com Versão Oficial

```bash
# Ver versão atual
kubectl version --client --short
# Client Version: v1.29.0

# Baixar checksum da mesma versão
VERSION="v1.29.0"
curl -LO "https://dl.k8s.io/release/${VERSION}/bin/linux/amd64/kubectl.sha256"

# Comparar
INSTALLED_HASH=$(sha256sum /usr/bin/kubectl | awk '{print $1}')
OFFICIAL_HASH=$(cat kubectl.sha256)

if [ "$INSTALLED_HASH" == "$OFFICIAL_HASH" ]; then
    echo "✅ Binário verificado - íntegro"
else
    echo "❌ ALERTA: Hash não corresponde!"
fi
```

---

## Verificando via /proc (Binários em Execução)

### Método para Processos Ativos

```bash
# Encontrar PID do processo
pgrep kubelet
# 1234

# Verificar binário real via /proc
ls -la /proc/1234/exe
# lrwxrwxrwx 1 root root 0 ... /proc/1234/exe -> /usr/bin/kubelet

# Calcular hash do binário em execução
sha256sum /proc/1234/exe
# ou
sha256sum /proc/$(pgrep kubelet)/exe
```

### Script Completo de Verificação

```bash
#!/bin/bash
# verify-k8s-binaries.sh

echo "=== Verificação de Binários Kubernetes ==="

# Lista de binários a verificar
BINARIES=("kubelet" "kubeadm" "kubectl")

for BIN in "${BINARIES[@]}"; do
    echo ""
    echo "--- $BIN ---"
    
    # Verificar se está rodando
    PID=$(pgrep -x "$BIN" 2>/dev/null)
    
    if [ -n "$PID" ]; then
        echo "PID: $PID"
        echo "Binário: $(readlink -f /proc/$PID/exe)"
        echo "Hash: $(sha256sum /proc/$PID/exe | awk '{print $1}')"
    else
        # Se não está rodando, verificar instalado
        BIN_PATH=$(which $BIN 2>/dev/null)
        if [ -n "$BIN_PATH" ]; then
            echo "Instalado em: $BIN_PATH"
            echo "Hash: $(sha256sum $BIN_PATH | awk '{print $1}')"
        else
            echo "Não encontrado"
        fi
    fi
done
```

---

## Verificação com GPG/Cosign

### GPG Signature (Método Tradicional)

```bash
# Importar chave pública do Kubernetes
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --import

# Baixar assinatura
curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl.sig"

# Verificar assinatura
gpg --verify kubectl.sig kubectl
```

### Cosign (Método Moderno - Sigstore)

```bash
# Instalar cosign
curl -LO https://github.com/sigstore/cosign/releases/download/v2.2.0/cosign-linux-amd64
chmod +x cosign-linux-amd64
mv cosign-linux-amd64 /usr/local/bin/cosign

# Verificar imagem de container assinada
cosign verify \
  --certificate-identity krel-staging@k8s-releng-prod.iam.gserviceaccount.com \
  --certificate-oidc-issuer https://accounts.google.com \
  registry.k8s.io/kube-apiserver:v1.29.0
```

---

## URLs Oficiais para Download

### Binários do Kubernetes

```plantuml,format=png
!include ../assets/diagrams/security/verificando-binarios-urls-oficiais-1.puml
```

### Exemplo Completo

```bash
VERSION="v1.29.0"
ARCH="linux/amd64"

# kubectl
curl -LO "https://dl.k8s.io/release/${VERSION}/bin/${ARCH}/kubectl"
curl -LO "https://dl.k8s.io/release/${VERSION}/bin/${ARCH}/kubectl.sha256"

# kubelet
curl -LO "https://dl.k8s.io/release/${VERSION}/bin/${ARCH}/kubelet"
curl -LO "https://dl.k8s.io/release/${VERSION}/bin/${ARCH}/kubelet.sha256"

# kubeadm
curl -LO "https://dl.k8s.io/release/${VERSION}/bin/${ARCH}/kubeadm"
curl -LO "https://dl.k8s.io/release/${VERSION}/bin/${ARCH}/kubeadm.sha256"

# Verificar todos
for bin in kubectl kubelet kubeadm; do
    echo "Verificando $bin..."
    echo "$(cat ${bin}.sha256)  ${bin}" | sha256sum --check
done
```

---

## Troubleshooting

### Hash Não Corresponde

```bash
# Possíveis causas:
# 1. Download incompleto
# 2. Versão errada do checksum
# 3. Binário foi alterado

# Solução: Re-baixar
rm kubectl kubectl.sha256
curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/v1.29.0/bin/linux/amd64/kubectl.sha256"

# Verificar tamanho do arquivo (download completo?)
ls -la kubectl
```

### Erro "sha256sum: WARNING: 1 computed checksum did NOT match"

```bash
# O arquivo está corrompido ou foi modificado!
# NÃO INSTALE este binário

# Verificar se é problema de formatação
cat kubectl.sha256
# Deve conter apenas o hash, sem nome do arquivo

# Formato esperado do comando de verificação:
echo "<HASH>  kubectl" | sha256sum --check
# Note os dois espaços entre hash e nome!
```

---

## Dicas para o Exame CKS

```plantuml,format=png
!include ../assets/diagrams/security/verificando-binarios-dicas-cks-verificação-de-binários-1.puml
```

---

## Referências

- [Supply Chain Security](supply-chain-security.md)
- [Hardening](hardening.md)
- [CIS Benchmark](cis-benchmark.md)
- [kubeadm](../tools/kubeadm.md)
- [Install](../maintenance/install.md)
