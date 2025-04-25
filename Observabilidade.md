## Probes:

- Fornece uma solução padrão para monitorar aplicações
- É um simples teste fornecido como uma propriedade do container
- Existem três tipos de probes:
	- `livenessProbe` - Checa se o container está vivo;
	- `readinessProbe`: Checa se a aplicação está pronta para receber tráfego
		- O container vai ser removido da lista de serviços disponíveis se falhar( o endepoint some?)
	- `startupProbe`: Usado para  verificar se a aplicação inicializou corretamente. Usado para aplicações que demora muito, por que ele não vai usar os outros probes
		- Nenhum outro probe será validado
-  pode ser `exec` `httpGet`, `tcpSocket` ou `grpc`
- configurações do `pod.spec.containers[*].(liveness|readiness|startup)Probe`
	- `initialDelaySeconds`:  Quanto tempo ele vai demorar até mandar o primeiro comando
	- `periodSeconds`: Com qual frequencia ele vai executar esse probe
	- `successThreshout`: Quantas vezes eu preciso que dê sucesso pra considerar o container up. No liveness e no readiness tem que ser 1
	- `failureThreshoud`: Quantas vezes eu preciso que dê erro pra considerar o container up. No liveness e no readiness tem que ser 1



- - **/healthz** - Informa se aplicação está saudável
- - **/livez** - Indica que a api está "alive"
- - **/readyz** - Indica que a aplicação está pronta pra receber trafego 


```shell
curl -k https://$(minikube ip):8443/healthz
curl -k https://$(minikube ip):8443/healthz?verbose
```
