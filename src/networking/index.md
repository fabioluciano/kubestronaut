# Networking no Kubernetes

## Conceitos Fundamentais

### Modelo de Rede do Kubernetes

O Kubernetes implementa um modelo de rede flat onde:

1. **Todo Pod tem um IP único** no cluster
2. **Pods podem comunicar sem NAT** entre si
3. **Nodes podem comunicar com Pods** sem NAT
4. **O IP que o Pod vê é o mesmo** que outros veem

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title REDES DO KUBERNETES

package "CLUSTER NETWORK\n(Nodes, API Server, etcd)\n10.0.0.0/16" as cn {
}

package "POD NETWORK\n(Comunicação entre Pods - CNI)\n10.244.0.0/16" as pn {
}

package "SERVICE NETWORK\n(ClusterIP para Services)\n10.96.0.0/12" as sn {
}

cn -[hidden]down-> pn
pn -[hidden]down-> sn

@enduml
```

---

## Tipos de Comunicação

### 1. Container para Container (mesmo Pod)

Containers no mesmo Pod compartilham o namespace de rede - mesmo IP.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title CONTAINER PARA CONTAINER (mesmo Pod)

package "POD\nIP: 10.244.1.5" as pod {
  rectangle "Container A\n:8080" as ca
  rectangle "Container B\n:9090" as cb
  ca <--> cb : localhost:PORT
}

note bottom of pod: Comunicação via localhost:PORT

@enduml
```

```yaml
{{#include ../assets/service/multi-container-pod.yaml}}
```

```bash
# Verificar namespace de rede
sudo lsns -t net

# Verificar interfaces no namespace
sudo ip netns exec <netns> ip addr
```

### 2. Pod para Pod (mesmo Node)

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title POD PARA POD (mesmo Node)

package "NODE" {
  package "POD A\n10.244.1.5" as poda {
    rectangle "veth" as vetha
  }
  
  package "POD B\n10.244.1.6" as podb {
    rectangle "veth" as vethb
  }
  
  rectangle "Bridge\n(cbr0)" as bridge
  
  vetha --> bridge
  vethb --> bridge
}

@enduml
```

```bash
# Pod A pode acessar Pod B diretamente pelo IP
kubectl exec pod-a -- curl 10.244.1.6:8080
```

### 3. Pod para Pod (Nodes diferentes)

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title POD PARA POD (Nodes diferentes)

package "NODE 1" {
  package "POD A\n10.244.1.5" as poda {
  }
  rectangle "Bridge" as bridge1
  rectangle "eth0" as eth1
  
  poda --> bridge1
  bridge1 --> eth1
}

package "NODE 2" {
  package "POD B\n10.244.2.5" as podb {
  }
  rectangle "Bridge" as bridge2
  rectangle "eth0" as eth2
  
  podb --> bridge2
  bridge2 --> eth2
}

rectangle "CNI Plugin\n(Overlay/Routing)" as cni

eth1 --> cni
eth2 --> cni

@enduml
```

### 4. Pod para Service

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title POD para SERVICE

rectangle "Pod Client" as client

rectangle "Service\nmy-svc\n10.96.0.10" as svc

rectangle "Pod 1" as pod1
rectangle "Pod 2" as pod2
rectangle "Pod 3" as pod3

client --> svc : DNS
svc --> pod1
svc --> pod2
svc --> pod3

note bottom of svc
  DNS: my-svc.default.svc.cluster.local → 10.96.0.10
  kube-proxy mantém regras iptables/ipvs para load balance
end note

@enduml
```

```bash
# Resolução DNS dentro do Pod
kubectl exec my-pod -- nslookup my-service
kubectl exec my-pod -- nslookup my-service.default.svc.cluster.local

# /etc/resolv.conf é gerado pelo kubelet
kubectl exec my-pod -- cat /etc/resolv.conf
# nameserver 10.96.0.10  (CoreDNS)
# search default.svc.cluster.local svc.cluster.local cluster.local
```

### 5. Externo para Service

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title ACESSO EXTERNO

cloud "Internet" as inet
rectangle "LB / Ingress" as lb
note right of lb: LoadBalancer Service ou\nIngress Controller

rectangle "NodePort" as np
note right of np: Porta 30000-32767 em cada Node

rectangle "ClusterIP" as cip
note right of cip: IP interno do Service

rectangle "Pods" as pods

inet --> lb
lb --> np
np --> cip
cip --> pods

@enduml
```

---

## CNI - Container Network Interface

### O que é CNI?

CNI é uma especificação e conjunto de bibliotecas para configurar interfaces de rede em containers Linux.

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title FLUXO DO CNI

start

:1. API Server → Kubelet: "Crie Pod X";
:2. Kubelet → CRI (containerd): "Crie container";
:3. CRI: Cria network namespace;
:4. CRI → CNI Plugin: "Configure rede para namespace Y";

:5. CNI Plugin;
note right
  - Cria veth pair
  - Conecta à bridge
  - Atribui IP
  - Configura rotas
end note

:6. CNI → CRI: Retorna configuração de rede;
:7. Pod está pronto com rede configurada;

stop

@enduml
```

### CNI Plugins Populares

| Plugin | Descrição | Recursos |
|--------|-----------|----------|
| **Calico** | L3 networking, BGP | NetworkPolicy, eBPF |
| **Cilium** | eBPF-based | L7 policy, observability |
| **Flannel** | Simple overlay | Simples, VXLAN |
| **Weave** | Mesh networking | Encryption, multicast |
| **Canal** | Flannel + Calico | Overlay + Policy |

### Configuração CNI

```bash
# Localização das configurações
ls /etc/cni/net.d/

# Exemplo de configuração
cat /etc/cni/net.d/10-calico.conflist

# Binários CNI
ls /opt/cni/bin/
```

### Verificar CNI

```bash
# Ver qual CNI está instalado
kubectl get pods -n kube-system | grep -E "calico|cilium|flannel|weave"

# Ver configuração
kubectl get cm -n kube-system | grep -i cni
```

---

## kube-proxy

### Modos de Operação

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title MODOS DO KUBE-PROXY

rectangle "iptables (default)" {
  note as n1
    Usa regras iptables para NAT
    Random selection de backends
    Não requer kernel modules extras
  end note
}

rectangle "ipvs" {
  note as n2
    Usa IPVS (IP Virtual Server)
    Melhor performance para muitos Services
    Múltiplos algoritmos de balanceamento
    Requer: ip_vs, ip_vs_rr, ip_vs_wrr, ip_vs_sh
  end note
}

rectangle "userspace (legacy)" {
  note as n3
    Proxy em userspace
    Lento, não usar
  end note
}

@enduml
```

### Ver Regras iptables

```bash
# Ver regras de um Service
sudo iptables -t nat -L KUBE-SERVICES -n | grep my-service

# Ver todas as regras do kube-proxy
sudo iptables-save | grep -i kube
```

---

## DNS no Kubernetes

### CoreDNS

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DNS RESOLUTION

rectangle "Formato FQDN" as fqdn
note bottom of fqdn
  <service>.<namespace>.svc.<cluster-domain>
end note

rectangle "Exemplos" {
  card "my-svc.default.svc.cluster.local" as e1
  card "my-svc.default (search domain)" as e2
  card "my-svc (mesmo namespace)" as e3
}

rectangle "Para Pods (quando habilitado)" {
  card "10-244-1-5.default.pod.cluster.local" as p1
}

rectangle "Para Headless Service" {
  card "pod-name.my-svc.default.svc.cluster.local" as h1
}

@enduml
```

### Verificar DNS

```bash
# Testar resolução DNS
kubectl run dnstest --image=busybox:1.28 --rm -it --restart=Never -- nslookup kubernetes

# Ver CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Ver ConfigMap do CoreDNS
kubectl get cm coredns -n kube-system -o yaml
```

---

## Network Policies

### Conceito

NetworkPolicy controla tráfego entre Pods. Por padrão, todo tráfego é permitido.

```yaml
{{#include ../assets/service/network-policy-deny-all.yaml}}
```

### Permitir Tráfego Específico

```yaml
{{#include ../assets/service/network-policy-allow-web.yaml}}
```

---

## Troubleshooting

### Pod Não Conecta

```bash
# Verificar IP do Pod
kubectl get pod -o wide

# Testar conectividade básica
kubectl exec pod-a -- ping <pod-b-ip>

# Verificar DNS
kubectl exec pod-a -- nslookup kubernetes

# Verificar Service
kubectl get endpoints my-service
```

### CNI com Problema

```bash
# Verificar pods do CNI
kubectl get pods -n kube-system

# Logs do CNI
kubectl logs -n kube-system -l k8s-app=calico-node

# Verificar configuração
cat /etc/cni/net.d/*.conf
```

### kube-proxy com Problema

```bash
# Verificar kube-proxy
kubectl get pods -n kube-system -l k8s-app=kube-proxy

# Logs
kubectl logs -n kube-system -l k8s-app=kube-proxy

# Verificar iptables
sudo iptables -t nat -L -n | grep -i kube
```

---

## Dicas para os Exames

```plantuml,format=png
@startuml
skinparam monochrome true
skinparam backgroundColor white

title DICAS - NETWORKING

rectangle "CKA" as cka {
  note as ncka
    • Entender fluxo de tráfego (Pod→Service→Pod)
    • Troubleshooting de DNS (nslookup, dig)
    • Verificar CNI e kube-proxy
    • NetworkPolicy básica
  end note
}

rectangle "CKAD" as ckad {
  note as nckad
    • Como Pods se comunicam (mesmo Pod, diferentes Pods)
    • Resolução DNS de Services
    • NetworkPolicy para restringir acesso
  end note
}

rectangle "CKS" as cks {
  note as ncks
    • NetworkPolicy deny-all como baseline
    • Segmentação de namespaces
    • Egress policies
  end note
}

rectangle "FQDN" as fqdn {
  note as nfqdn
    <service>.<namespace>.svc.cluster.local
  end note
}

cka -[hidden]down-> ckad
ckad -[hidden]down-> cks
cks -[hidden]down-> fqdn

@enduml
```

---

## Referências

- [DNS](./DNS.md)
- [NetworkPolicy](./Security/NetworkPolicy.md)
- [Service](./networking/service.md)
- [Ingress](./Ingress.md)
- [kube-proxy](./cluster-components/kube-proxy.md)
