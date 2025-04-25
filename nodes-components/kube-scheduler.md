- Decide onde um pod deve ser colocado. Ele não coloca. Quem coloca é o kubelet;
- Observa cada pod e tentar encontrar qual o melhor nó para ele;
- Ranqueia os nós pra identificar qual o melhor nó para se colocar o pod
- Você pode customizar o scheduler, criando o seu próprio. Karpenter.,
---
Pode ser usar para definir um nó de um pod:
- Requests e Limits
- Taints e tolerations
- node selector/affinity
- nodename
---
Para visualizar suas configurações
- Instalado pelo kubeadm `/etc/kubernetes/manifest/kube-scheduler.yaml`
- nstalado na mão: `/etc/systemd/system/kube-scheduler.service`