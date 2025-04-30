- Se você tiver no mesmo namespace, voce vai conseguir acessar uma service apenas por seu nome, sem mencionar o namespace http://SERVICENAME
- Se voce tiver em outro namespace você precisa mencionar o namespace https://SERVICENAME.NAMESPACE
- Service name : `SVCNAME.NAMESPACE.svc.cluster.local`
- Pods por padrão não recebem um DNS, mas podem ser configurados
	- Quando configurado, o DNS do pode será o número do IP substituindo o dot pelo dash 192.168.56.10 `192-168-56-10' 
	- O endereço é `IPWITHDASHES.NAMESPACE.pod.cluster.local`
	- A forma contraída não funciona da para pods, já que não é colocada no resolv,conf

## Core DNS

- Para habilitar que pods também recebam DNS, ative a opção `pods insecure` no Corefile do coredns