- Controla o trafego entre os pods
- A CNI precisa ser compatível com a network policy
- O trafego é dividido em duas categorias:
	- Ingress: O que entra
	- Egress:  O que sai
- Por padrão todos os pod se comunicam entre sí sem nenhuma  configuração adicional
- Caso não seja mencionado, o PolicyType manterá o padrão. Ou seja, vai poder se comunicar com qualquer um
- Quando é configurado um ingress, o egress daquela porta é configurado automaticamente
- Por padrão, desde de que o podSelector do from case com o podlabel, vai funcionar para qualquer namespace
- A porta que referenciada por ports é a targetPort do service. Ou seja, aporta do container
- Para selecionar o pod que se conectará ao elemento restringido, é possível selecionar por:
	- `networkpolicy.spec.ingress.from.ipBlock`
	- `networkpolicy.spec.ingress.from.namespaceSelector`
	- `networkpolicy.spec.ingress.from.podSelector`

- Para definir uma NetworkPolicy siga os seguintes passos:
	- Defina qual o pod que receberá a regra usando `networkpolicy.spec.podSelector.matchLabels
	- Defina qual tipo de regra que será aplicada `Egress` ou `Ingress` ou ambas
	- Caso seja ingress, defina o `networkpolicy.spec.ingress.from` bem como as  `networkpolicy.spec.ingress.ports`
	- Caso seja egress, defina o `networkpolicy.spec.ingress.to` bem como as  `networkpolicy.spec.ingress.ports`



> [!NOTE]- Criação de uma `Secret`
```reference
filePath: "@/Attachments/Kubernetes/networkpolicy/netpol-ingress-test.yaml"
```


> [!NOTE]- Criação de uma `Secret`
```reference
filePath: "@/Attachments/Kubernetes/networkpolicy/netpol-egress-test.yaml"
```


> [!NOTE]- Criação de uma `Secret`
```reference
filePath: "@/Attachments/Kubernetes/networkpolicy/netpol-allow-all-test.yaml"
```


> [!NOTE]- Criação de uma `Secret`
```reference
filePath: "@/Attachments/Kubernetes/networkpolicy/netpol-deny-all-test.yaml"
```

## Node metadata protection

- Dado que tenho uma aplicação comprometida na cloud e ela consegue fazer requisições para o endpoint de metadados, qualquer informação sensível estará exposta.
- O endereço padrão de metadado é `http://169.254.169.254/latest/meta-data`

```reference title:"Bloqueia todo o trafego de entrada e saída de todos os pods do namespace"
filePath: "@/Attachments/Kubernetes/networkpolicy/cks/default-deny.yaml"
```


```reference title:"Bloqueia todo o trafego de saída para o bloco de IP de retrival de metadata"
filePath: "@/Attachments/Kubernetes/networkpolicy/cks/block-metadata-retrieval.yaml"
```


MUITO IMPORTANTE LEMBRAR QUE 0.0.0.0/0 LIBERA PRA TODOS E CIDR/32 'e um IP SO'
