# AppArmor

> **Certificações**: CKS (System Hardening - 15%)

## Conceitos Fundamentais

### O que é AppArmor?

AppArmor (Application Armor) é um módulo de segurança do kernel Linux que restringe as capacidades de programas através de perfis de segurança. No contexto Kubernetes, é usado para restringir o que containers podem fazer.

```admonish info title="Por que usar AppArmor?"
- Suplementa permissões de usuários/grupos do Linux
- Limita acesso a arquivos/diretórios
- Restringe capabilities de rede
- Defesa em profundidade para containers
- Exigido para certificação CKS
```

### Modos de Operação

| Modo | Descrição | Uso |
|------|-----------|-----|
| **enforce** | Monitora e bloqueia violações | Produção |
| **complain** | Permite execução, mas loga violações | Debug/Desenvolvimento |
| **unconfined** | Sem restrições | Desabilitado |

### AppArmor vs Seccomp

| Característica | AppArmor | Seccomp |
|----------------|----------|---------|
| **Escopo** | Filesystem, rede, capabilities | Syscalls |
| **Granularidade** | Paths, operações | Syscalls específicas |
| **Complexidade** | Média | Alta |

---

## Comandos Essenciais

### Verificar Status

```bash
# Verificar se AppArmor está habilitado
cat /sys/module/apparmor/parameters/enabled

# Status do serviço
systemctl status apparmor

# Status detalhado dos profiles
sudo aa-status

# Listar profiles carregados
cat /sys/kernel/security/apparmor/profiles
```

### Gerenciar Profiles

```bash
# Instalar ferramentas do AppArmor
apt install apparmor-utils

# Carregar um profile
sudo apparmor_parser -r /path/to/profile

# Remover um profile
sudo apparmor_parser -R /path/to/profile

# Colocar profile em modo complain
sudo aa-complain /path/to/profile

# Colocar profile em modo enforce
sudo aa-enforce /path/to/profile
```

### Criar Profiles

```bash
# Gerar profile para uma aplicação
sudo aa-genprof /usr/bin/curl

# Analisar logs e atualizar profile
sudo aa-logprof

# Ver qual profile um processo está usando
cat /proc/1/attr/current
```

---

## Usar AppArmor no Kubernetes

### Pré-requisitos

1. AppArmor deve estar habilitado nos nodes
2. Profile deve estar carregado em **todos** os nodes onde o Pod pode rodar
3. Container runtime deve suportar AppArmor (containerd, CRI-O)

### Via SecurityContext (K8s 1.30+)

```yaml
{{#include ../assets/security/apparmor/pod-nginx-apparmor.yaml}}
```


---

### Pod AppArmor via Annotation

```yaml
{{#include ../assets/security/apparmor/pod-apparmor-annotation.yaml}}
```


---

### Pod AppArmor via SecurityContext

```yaml
{{#include ../assets/security/apparmor/pod-apparmor-securitycontext.yaml}}
```

---

## Troubleshooting

### Pod não inicia com AppArmor

```bash
# Verificar se profile existe no node
sudo aa-status | grep <profile-name>

# Verificar eventos do Pod
kubectl describe pod <pod-name>

# Erros comuns:
# "AppArmor profile not found" - Profile não carregado
# "AppArmor not enabled" - AppArmor desabilitado no node
```

### Verificar Profile Ativo no Container

```bash
# Dentro do container
cat /proc/1/attr/current

# Via crictl no node
sudo crictl inspect <container-id> | grep apparmor
```

### Debugar Violações

```bash
# Ver logs de violação do AppArmor
sudo dmesg | grep apparmor
sudo journalctl -k | grep apparmor

# Colocar em modo complain para debug
sudo aa-complain /etc/apparmor.d/<profile>
```

---

## Dicas para o Exame CKS

```admonish tip title="Dicas CKS - AppArmor"
1. **Profile deve estar no node**: Carregue com `apparmor_parser -r`
2. **Verificar status**: `aa-status` mostra profiles carregados
3. **SecurityContext vs Annotation**: Prefira SecurityContext (mais novo)
4. **runtime/default**: Profile padrão do container runtime
5. **localhost/**: Prefixo para profiles customizados
```

### Comandos para Memorizar

```bash
# Verificar se habilitado
cat /sys/module/apparmor/parameters/enabled

# Ver profiles
sudo aa-status

# Carregar profile
sudo apparmor_parser -r /path/to/profile

# Profile no container
cat /proc/1/attr/current
```

---

## Referências

- [Kubernetes AppArmor](https://kubernetes.io/docs/tutorials/security/apparmor/)
- [Seccomp](seccomp.md) - Outra camada de proteção
- [Pod Security](pod-security-admission.md) - Políticas de segurança
