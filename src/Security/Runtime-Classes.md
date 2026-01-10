# Runtime Classes

> **Certificacoes**: CKS (Minimize Microservice Vulnerabilities - 20%)

## Conceitos Fundamentais

**RuntimeClass** e um recurso do Kubernetes que permite selecionar diferentes container runtimes para executar Pods. Isso possibilita usar runtimes de seguranca aprimorada como gVisor ou Kata Containers para workloads que requerem isolamento adicional.

```admonish info title="Por que usar diferentes runtimes?"
O runtime padrao (runc) compartilha o kernel do host com os containers. Runtimes alternativos como gVisor e Kata Containers fornecem camadas adicionais de isolamento, reduzindo a superficie de ataque.
```

## O que sao Container Runtimes?

Container runtimes sao os componentes responsaveis por executar containers. No Kubernetes, o kubelet se comunica com o runtime atraves do CRI (Container Runtime Interface).

```plantuml,format=png
!include ../assets/diagrams/security/runtime-classes-arquitetura-do-container-runtime-interface-cri-1.puml
```

## Comparacao de Isolamento

```plantuml,format=png
!include ../assets/diagrams/security/runtime-classes-container-runtimes-niveis-de-isolamento-1.puml
```

## Hierarquia de Seguranca dos Runtimes

| Runtime | Isolamento | Superficie de Ataque | Performance | Compatibilidade |
|---------|------------|---------------------|-------------|-----------------|
| **runc** | Namespaces/cgroups | ~330 syscalls | Otima | Total |
| **gVisor** | Kernel userspace | ~60 syscalls | Boa | ~95% |
| **Kata** | VM com hardware | Virtualizacao | Moderada | Total |
| **Firecracker** | MicroVM | Virtualizacao | Boa | Total |

## Arquitetura RuntimeClass

```plantuml,format=png
!include ../assets/diagrams/security/runtime-classes-fluxo-completo-runtimeclass-1.puml
```

## Criando RuntimeClass

### Estrutura do Recurso

```yaml
{{#include ../assets/security/runtimeclass.yaml}}
```

### RuntimeClass para gVisor e Kata

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-gvisor-kata.yaml}}
```

### RuntimeClass Completo

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-complete.yaml}}
```

## gVisor (runsc)

gVisor e um runtime que fornece um kernel em userspace, interceptando syscalls e fornecendo um sandbox de seguranca. Desenvolvido pelo Google e usado no GKE Sandbox.

### Arquitetura do gVisor

```plantuml,format=png
!include ../assets/diagrams/security/runtime-classes-arquitetura-interna-do-gvisor-1.puml
```

### Componentes do gVisor

| Componente | Funcao | Detalhes |
|------------|--------|----------|
| **Sentry** | Implementa syscalls em userspace | Escrito em Go, ~200 syscalls |
| **Gofer** | Fornece acesso ao filesystem | Comunicacao via 9P protocol |
| **runsc** | OCI runtime que integra com containerd | CLI compativel com runc |
| **netstack** | Stack de rede em userspace | Implementacao propria TCP/IP |

### Caracteristicas do gVisor

**Vantagens:**
- Intercepta ~200 syscalls mais comuns
- Kernel escrito em Go (memory-safe, sem buffer overflow)
- Menor overhead que VMs (~20Mi memoria)
- Startup rapido (similar a containers)
- Compativel com a maioria das aplicacoes (~95%)

**Limitacoes:**
- Nao suporta todas as syscalls (algumas apps podem falhar)
- Aplicacoes que usam `ptrace` podem falhar
- Algumas funcionalidades de rede podem ter problemas
- Performance menor para I/O intensivo
- Nao suporta /dev/nvidia (GPU)

### Instalacao do gVisor

```bash
# === Ubuntu/Debian ===

# Adicionar repositorio
curl -fsSL https://gvisor.dev/archive.key | sudo gpg --dearmor -o /usr/share/keyrings/gvisor-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/gvisor-archive-keyring.gpg] https://storage.googleapis.com/gvisor/releases release main" | sudo tee /etc/apt/sources.list.d/gvisor.list > /dev/null

# Instalar runsc
sudo apt-get update && sudo apt-get install -y runsc

# Verificar instalacao
runsc --version
```

### Configurar containerd para gVisor

```toml
# /etc/containerd/config.toml

version = 2

[plugins."io.containerd.grpc.v1.cri".containerd]
  default_runtime_name = "runc"

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes]

  # Runtime padrao (runc)
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
    runtime_type = "io.containerd.runc.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
      SystemdCgroup = true

  # gVisor runtime
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]
    runtime_type = "io.containerd.runsc.v1"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc.options]
      TypeUrl = "io.containerd.runsc.v1.options"
      # Opcional: arquivo de configuracao do runsc
      ConfigPath = "/etc/containerd/runsc.toml"
```

```bash
# Reiniciar containerd
sudo systemctl restart containerd

# Verificar runtimes disponiveis
sudo ctr plugins ls | grep runtime
```

### Pod com gVisor

```yaml
{{#include ../assets/security/runtime-classes/pod-gvisor.yaml}}
```

### Pod gVisor Completo

```yaml
{{#include ../assets/security/runtime-classes/pod-gvisor-complete.yaml}}
```

### Verificar gVisor

```bash
# Verificar kernel (deve mostrar gVisor)
kubectl exec -ti sandboxed-pod -- uname -a
# Output: Linux sandboxed-pod 4.4.0 #1 SMP ... x86_64 Linux
# Note: versao 4.4.0 indica gVisor

# Verificar dmesg (mostra mensagens do Sentry)
kubectl exec -ti sandboxed-pod -- dmesg | head
# Starting gVisor...

# Verificar /proc/version
kubectl exec -ti sandboxed-pod -- cat /proc/version
# Linux version 4.4.0 (go1.20.5)

# Verificar syscalls (gVisor limita algumas)
kubectl exec -ti sandboxed-pod -- cat /proc/sys/kernel/hostname
```

## Kata Containers

Kata Containers executa containers dentro de VMs leves (microVMs), fornecendo isolamento de hardware completo. Combina a velocidade de containers com a seguranca de VMs.

### Arquitetura do Kata Containers

```plantuml,format=png
!include ../assets/diagrams/security/runtime-classes-arquitetura-interna-do-kata-containers-1.puml
```

### Componentes do Kata

| Componente | Funcao |
|------------|--------|
| **kata-runtime** | OCI runtime, gerencia ciclo de vida da VM |
| **kata-agent** | Agente dentro da VM, executa containers |
| **QEMU/Cloud Hypervisor** | Hypervisor para criar VMs |
| **Guest Kernel** | Kernel Linux otimizado para boot rapido |
| **virtio-fs** | Compartilhamento de filesystem eficiente |

### Caracteristicas do Kata

**Vantagens:**
- Isolamento total via virtualizacao de hardware
- Kernel dedicado por Pod (vulnerabilidades de kernel nao afetam host)
- Compatibilidade total com aplicacoes (kernel Linux completo)
- Suporte a virtio para performance
- Pode usar diferentes hypervisors (QEMU, Cloud Hypervisor, Firecracker)

**Limitacoes:**
- Requer suporte a virtualizacao (VT-x/AMD-V)
- Maior overhead de memoria (~120Mi por VM)
- Startup mais lento que containers tradicionais (2-5 segundos)
- Nao funciona em nested virtualization sem suporte especial
- Nao suporta alguns recursos de host (ex: GPU sem passthrough)

### Instalacao do Kata Containers

```bash
# === Ubuntu 20.04+ ===

# Instalar dependencias
sudo apt-get update
sudo apt-get install -y wget curl

# Baixar e instalar Kata
ARCH=$(uname -m)
KATA_VERSION=3.2.0

wget https://github.com/kata-containers/kata-containers/releases/download/${KATA_VERSION}/kata-static-${KATA_VERSION}-${ARCH}.tar.xz
sudo tar -xvf kata-static-${KATA_VERSION}-${ARCH}.tar.xz -C /
sudo ln -sf /opt/kata/bin/kata-runtime /usr/local/bin/kata-runtime
sudo ln -sf /opt/kata/bin/containerd-shim-kata-v2 /usr/local/bin/containerd-shim-kata-v2

# Verificar instalacao
kata-runtime --version
kata-runtime check

# Verificar suporte a virtualizacao
kata-runtime env
```

### Configurar containerd para Kata

```toml
# /etc/containerd/config.toml

version = 2

[plugins."io.containerd.grpc.v1.cri".containerd]
  default_runtime_name = "runc"

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes]

  # Runtime padrao (runc)
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
    runtime_type = "io.containerd.runc.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
      SystemdCgroup = true

  # Kata Containers com QEMU
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.kata]
    runtime_type = "io.containerd.kata.v2"
    pod_annotations = ["io.katacontainers.*"]
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.kata.options]
      ConfigPath = "/opt/kata/share/defaults/kata-containers/configuration.toml"

  # Kata Containers com Cloud Hypervisor (mais leve)
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.kata-clh]
    runtime_type = "io.containerd.kata-clh.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.kata-clh.options]
      ConfigPath = "/opt/kata/share/defaults/kata-containers/configuration-clh.toml"
```

```bash
# Reiniciar containerd
sudo systemctl restart containerd
```

### Pod com Kata Containers

```yaml
{{#include ../assets/security/runtime-classes/pod-kata.yaml}}
```

### Pod Kata Completo

```yaml
{{#include ../assets/security/runtime-classes/pod-kata-complete.yaml}}
```

### Verificar Kata

```bash
# Verificar kernel (kernel dedicado da VM)
kubectl exec -ti kata-pod -- uname -r
# Output: 5.15.x-kata (versao do guest kernel)

# Verificar que NAO e gVisor
kubectl exec -ti kata-pod -- uname -a | grep -i gvisor
# Nao deve retornar nada

# Ver processos (apenas do container)
kubectl exec -ti kata-pod -- ps aux

# Verificar virtualizacao no host
ps aux | grep qemu
# Deve mostrar processo QEMU para o Pod
```

## RuntimeClass com Overhead

O campo `overhead` define recursos adicionais consumidos pelo runtime. O scheduler considera esse overhead ao agendar Pods.

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-overhead.yaml}}
```

```admonish warning title="Overhead e Scheduling"
O overhead e adicionado aos requests do Pod para fins de scheduling.
Um Pod com requests de 100Mi usando RuntimeClass com overhead de 120Mi
sera schedulado considerando **220Mi**.

**Importante**: O overhead nao afeta os limits do container,
apenas o scheduling.
```

### Calculo de Recursos com Overhead

```plantuml,format=png
!include ../assets/diagrams/security/runtime-classes-calculo-de-recursos-com-runtimeclass-overhead-1.puml
```

## RuntimeClass com Scheduling

O campo `scheduling` permite restringir em quais nodes o runtime pode executar.

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-scheduling.yaml}}
```

### RuntimeClass com NodeSelector e Tolerations

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-node-selector.yaml}}
```

### Preparar Nodes para Runtimes Seguros

```bash
# Adicionar label para nodes com gVisor
kubectl label nodes worker-1 worker-2 runtime.class/gvisor=true

# Adicionar label para nodes com Kata (necessita VT-x)
kubectl label nodes worker-3 worker-4 runtime.class/kata=true

# Adicionar taint para isolamento (opcional)
kubectl taint nodes worker-3 worker-4 runtime=kata:NoSchedule

# Verificar labels
kubectl get nodes -l runtime.class/kata=true
```

## Deployment com RuntimeClass

```yaml
{{#include ../assets/security/runtime-classes/deployment-runtimeclass.yaml}}
```

### Deployment Completo com gVisor

```yaml
{{#include ../assets/security/runtime-classes/deployment-gvisor-complete.yaml}}
```

## Casos de Uso

### Multi-tenancy

```plantuml,format=png
!include ../assets/diagrams/security/runtime-classes-runtimeclass-para-multi-tenancy-1.puml
```

### RuntimeClass por Nivel de Confianca

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-trust-levels.yaml}}
```

### Compliance (PCI-DSS, HIPAA)

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-pci-compliant.yaml}}
```

### FaaS/Serverless

Runtimes como Kata sao ideais para FaaS onde codigo nao confiavel e executado:

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-faas.yaml}}
```

## Comparacao Detalhada de Runtimes

| Caracteristica | runc | gVisor | Kata | Firecracker |
|----------------|------|--------|------|-------------|
| **Tipo** | Container nativo | Kernel userspace | MicroVM | MicroVM |
| **Isolamento** | Namespaces/cgroups | Interceptacao syscalls | Hardware VM | Hardware VM |
| **Superficie de ataque** | ~330 syscalls | ~60 syscalls | Hypervisor | Hypervisor |
| **Overhead CPU** | 0% | 5-10% | 10-20% | 5-15% |
| **Overhead Memoria** | 0 | ~20Mi | ~120Mi | ~50Mi |
| **Startup time** | <100ms | <200ms | 1-3s | <125ms |
| **Compatibilidade** | 100% | ~95% | 100% | 100% |
| **Requisitos** | Linux | Linux | VT-x/AMD-V | VT-x/AMD-V |
| **GPU Support** | Sim | Nao | Passthrough | Nao |
| **Nested Virt** | N/A | N/A | Com suporte | Com suporte |

## Fluxo de Decisao

```plantuml,format=png
!include ../assets/diagrams/security/runtime-classes-escolhendo-o-runtime-correto-1.puml
```

## Comandos Uteis

```bash
# === RuntimeClass ===
# Listar RuntimeClasses
kubectl get runtimeclass

# Ver detalhes de um RuntimeClass
kubectl describe runtimeclass gvisor

# Criar RuntimeClass
kubectl apply -f runtimeclass.yaml

# === Pods ===
# Ver qual RuntimeClass um Pod usa
kubectl get pod <pod> -o jsonpath='{.spec.runtimeClassName}'

# Listar pods por RuntimeClass
kubectl get pods -A -o jsonpath='{range .items[?(@.spec.runtimeClassName)]}{.metadata.namespace}/{.metadata.name}: {.spec.runtimeClassName}{"\n"}{end}'

# === Nodes ===
# Verificar nodes com label para RuntimeClass
kubectl get nodes -l runtime.class/gvisor=true
kubectl get nodes -l runtime.class/kata=true

# === containerd ===
# Verificar runtimes configurados no containerd
sudo ctr plugins ls | grep runtime

# Verificar configuracao do containerd
sudo cat /etc/containerd/config.toml | grep -A10 runtimes

# Listar containers por runtime
sudo ctr -n k8s.io containers ls

# === Verificacao do runtime ===
# Verificar se Pod usa gVisor
kubectl exec <pod> -- uname -a | grep -i gvisor

# Verificar kernel (gVisor mostra 4.4.0)
kubectl exec <pod> -- uname -r

# Verificar /proc/version
kubectl exec <pod> -- cat /proc/version

# === Eventos ===
# Ver eventos de Pod (erros de runtime)
kubectl describe pod <pod> | grep -A10 Events

# Ver logs do kubelet
journalctl -u kubelet | grep -i runtime

# === Debug ===
# Testar runtime diretamente
sudo ctr run --runtime io.containerd.runsc.v1 docker.io/library/alpine:latest test-gvisor uname -a
```

## Troubleshooting

### Pod Fica Pending

```admonish failure title="Erro: Pod em Pending com RuntimeClass"
**Causas comuns**:
1. RuntimeClass nao existe
2. Nenhum node com handler configurado
3. NodeSelector nao corresponde a nenhum node
4. Resources insuficientes (considerando overhead)

**Solucao**:
1. Verificar se RuntimeClass existe: `kubectl get runtimeclass`
2. Verificar labels dos nodes: `kubectl get nodes --show-labels`
3. Verificar events do Pod: `kubectl describe pod <pod>`
4. Verificar scheduling com overhead
```

### Runtime Handler Not Found

```admonish failure title="Erro: handler not found"
**Causa**: O handler especificado no RuntimeClass nao esta configurado no containerd/CRI-O.

**Verificacao**:
```bash
# Ver handlers configurados
sudo cat /etc/containerd/config.toml | grep -A5 runtimes

# Verificar se runtime esta instalado
which runsc  # gVisor
which kata-runtime  # Kata
```

**Solucao**:
1. Instalar runtime no node
2. Configurar handler no containerd
3. Reiniciar containerd: `systemctl restart containerd`
```

### gVisor: Syscall Nao Suportada

```admonish failure title="Erro: syscall not implemented"
Algumas syscalls nao sao suportadas pelo gVisor.

**Verificacao**:
```bash
# Ver logs do container
kubectl logs <pod>

# Ver logs do sistema
dmesg | grep -i gvisor
journalctl -u containerd | grep -i runsc
```

**Syscalls NAO suportadas**:
- `ptrace` (debuggers)
- `io_uring`
- Algumas `ioctl`

**Solucao**:
1. Verificar se aplicacao realmente precisa da syscall
2. Usar runtime diferente (runc ou Kata)
3. Atualizar gVisor (novas versoes suportam mais syscalls)
```

### Kata: Virtualization Not Supported

```admonish failure title="Erro: hardware virtualization not supported"
Kata requer VT-x (Intel) ou AMD-V (AMD).

**Verificacao**:
```bash
# Verificar suporte a virtualizacao
kata-runtime check

# Verificar CPU flags
grep -E 'vmx|svm' /proc/cpuinfo

# Em VMs (nested virtualization)
# Verificar se nested virt esta habilitado
cat /sys/module/kvm_intel/parameters/nested  # Intel
cat /sys/module/kvm_amd/parameters/nested    # AMD
```

**Solucao**:
1. Usar hardware com suporte a virtualizacao
2. Habilitar VT-x/AMD-V na BIOS
3. Para VMs, habilitar nested virtualization
4. Usar gVisor como alternativa
```

### Performance Degradada

```admonish warning title="Performance inferior ao esperado"
Runtimes seguros tem overhead natural.

**Benchmarking**:
```bash
# CPU benchmark
kubectl exec <pod> -- time dd if=/dev/zero of=/dev/null bs=1M count=10000

# I/O benchmark (impactado por gVisor)
kubectl exec <pod> -- time dd if=/dev/zero of=/tmp/test bs=1M count=100 oflag=dsync

# Network benchmark
kubectl exec <pod> -- time curl -o /dev/null http://internal-service
```

**Mitigacoes**:
1. gVisor: usar para workloads CPU-bound, evitar I/O intensivo
2. Kata: usar virtio-fs para melhor performance de filesystem
3. Considerar tradeoff seguranca vs performance
```

## Dicas para o Exame CKS

```admonish tip title="Dicas CKS"
1. **Criar RuntimeClass**: Saiba criar do zero sem olhar documentacao
2. **handler**: Deve corresponder EXATAMENTE ao configurado no containerd
3. **Verificar gVisor**: Use `uname -a` - gVisor mostra versao 4.4.0
4. **overhead**: Entenda que afeta scheduling (requests + overhead)
5. **scheduling**: Saiba usar nodeSelector e tolerations
6. **Quando usar**: gVisor para workloads nao confiaveis, Kata para isolamento maximo
7. **Troubleshooting**: Saiba verificar eventos do Pod e logs do kubelet
```

```admonish warning title="Pontos de Atencao no Exame"
- RuntimeClass e um recurso **cluster-wide** (sem namespace)
- O campo `handler` e **case-sensitive**
- Nodes sem o runtime configurado nao podem executar Pods com RuntimeClass
- gVisor pode nao suportar algumas aplicacoes (teste sempre)
```

## Best Practices

1. **Use RuntimeClass para workloads nao confiaveis** - Codigo de terceiros, FaaS, multi-tenancy
2. **Considere o overhead** - gVisor e Kata consomem mais recursos
3. **Teste compatibilidade** - Nem todas apps funcionam com gVisor
4. **Use nodeSelector** - Garanta que Pods vao para nodes corretos
5. **Documente** - Mantenha registro de quais workloads usam qual runtime
6. **Monitore** - Overhead pode impactar custos
7. **Defense in Depth** - RuntimeClass e uma camada, combine com outras (NetworkPolicy, PSA)
8. **Padronize** - Defina politicas de qual runtime usar para cada tipo de workload
9. **Atualize regularmente** - Novos releases trazem mais syscalls e fixes
10. **Tenha fallback** - Se um runtime falhar, tenha plano B

## Recursos Adicionais

- [Kubernetes RuntimeClass](https://kubernetes.io/docs/concepts/containers/runtime-class/)
- [gVisor Documentation](https://gvisor.dev/docs/)
- [gVisor Compatibility](https://gvisor.dev/docs/user_guide/compatibility/)
- [Kata Containers](https://katacontainers.io/docs/)
- [Kata Architecture](https://github.com/kata-containers/kata-containers/tree/main/docs/design/architecture)
- [Container Runtime Interface (CRI)](https://kubernetes.io/docs/concepts/architecture/cri/)
- [containerd Runtime Handlers](https://github.com/containerd/containerd/blob/main/docs/cri/config.md)


---

### RuntimeClass gVisor

```yaml
{{#include ../assets/security/runtimeclass/runtimeclass-runsc.yaml}}
```


---

### RuntimeClass Untrusted

```yaml
{{#include ../assets/security/runtime-classes/runtimeclass-untrusted.yaml}}
```
