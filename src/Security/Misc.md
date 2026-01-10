# Dicas e Comandos Úteis

<span class="badge badge-cks">CKS</span> <span class="badge badge-cka">CKA</span> <span class="badge badge-ckad">CKAD</span>

---

## Acessar Services via kubectl proxy

```admonish info title="kubectl proxy"
O `kubectl proxy` cria um túnel seguro para o API Server, permitindo acessar services internas sem expor portas.
```

```bash
# Iniciar proxy (porta 8001 por padrão)
kubectl proxy

# Acessar service via proxy
curl http://127.0.0.1:8001/api/v1/namespaces/<namespace>/services/<service>/proxy/

# Exemplo prático
curl -X GET http://127.0.0.1:8001/api/v1/namespaces/default/services/my-app/proxy/
```

---

## Trabalhar com Containers (crictl)

### Obter PID de um Container

```bash
# Listar containers
sudo crictl ps

# Obter PID do processo principal
sudo crictl inspect <container-id> | jq '.info.pid'

# Entrar no namespace do container
sudo nsenter -t <pid> -n ip addr
```

---

## Extrair Certificados e Credenciais

### Extrair certificado de usuário do kubeconfig

```bash
# Extrair certificado de um usuário específico
kubectl config view --raw \
  -o jsonpath="{.users[?(@.name == 'admin')].user.client-certificate-data}" | base64 -d

# Extrair chave privada
kubectl config view --raw \
  -o jsonpath="{.users[?(@.name == 'admin')].user.client-key-data}" | base64 -d

# Ver todos os usuários
kubectl config view -o jsonpath='{.users[*].name}'
```

---

## Acessar API de dentro de um Pod

```admonish warning title="Service Account Token"
Todo Pod tem um token de ServiceAccount montado automaticamente em `/run/secrets/kubernetes.io/serviceaccount/`.
```

```bash
# Variáveis disponíveis no Pod
# - KUBERNETES_SERVICE_HOST
# - KUBERNETES_SERVICE_PORT

# Acessar API usando o token do ServiceAccount
curl -k \
  -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)" \
  https://kubernetes.default/api/v1/namespaces/default/pods

# Listar secrets (requer permissão RBAC)
curl -k \
  -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)" \
  https://kubernetes.default/api/v1/namespaces/<namespace>/secrets
```

### Arquivos do ServiceAccount no Pod

```bash
/run/secrets/kubernetes.io/serviceaccount/
├── token      # JWT token para autenticação
├── ca.crt     # CA do cluster
└── namespace  # Namespace do Pod
```

---

## Debug de Rede

```bash
# Testar DNS de dentro de um Pod
kubectl run -ti --rm debug --image=busybox -- nslookup kubernetes.default

# Ver resolv.conf
kubectl run -ti --rm debug --image=nginx -- cat /etc/resolv.conf

# Testar conectividade
kubectl run -ti --rm debug --image=nicolaka/netshoot -- curl http://service:port
```

---

## Verificar Configurações do Cluster

```bash
# Range de IPs dos Services
kubectl cluster-info dump | grep service-cluster-ip-range

# CIDR dos Pods
kubectl cluster-info dump | grep cluster-cidr

# Ver todas as configurações
kubectl cluster-info dump | grep -E "(cidr|range)"
```

---

## JSONPath Úteis

```bash
# IPs de todos os Pods
kubectl get pods -o jsonpath='{.items[*].status.podIP}'

# Nodes e seus IPs
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.addresses[0].address}{"\n"}{end}'

# Containers em um Pod
kubectl get pod <pod> -o jsonpath='{.spec.containers[*].name}'

# Images usadas
kubectl get pods -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u
```

---

## Dicas para os Exames

```admonish tip title="Dicas"
1. **kubectl proxy**: Útil para acessar services sem NodePort
2. **crictl**: Use para debug de containers no node
3. **ServiceAccount token**: Sempre em `/run/secrets/kubernetes.io/serviceaccount/`
4. **JSONPath**: Domine para extrair informações rapidamente
```

---

## Referências

- [crictl](../tools/crictl.md) - Ferramenta de debug de containers
- [RBAC](rbac.md) - Permissões para ServiceAccounts
- [Certificados](certificates.md) - PKI do Kubernetes
