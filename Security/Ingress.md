```plantuml
Cliente -> HTTP
HTTP -> Ingress
Ingress -> Rules
Rules -> Service
Service -> Pods
```


- São basicamente proxys reversos implantados;
- Está em feature Freeze e será substituído pelo [[Gateway API]]
- São separados em dois componentes `IngressController`, sendo a solução escolhida para lidar com as regras definidas, denominadas `IngressResources`;
- O Kubernetes não vem com um `IngressController` por padrão;
- Há dois tipos de regras a serem aplicadas. 
	- As baseadas em host
	- As baseadas em path
		- Existem dois tipos principais de `ingress.spec.rules.http.paths.pathTypes.
			- Prefix: Vai encaminhar para o host quando começar com o path informado
			- Exact: Vai encaminhar apenas se casar exatamente como configurado. Inclusive a barra no final


> [!NOTE]- Criação de uma `Secret`
```reference
filePath: "@/Attachments/Kubernetes/ingress/ingress-test.yaml"
```


```shell
k create ingress ingress-test --class nginx --rule="/app=ingress-test:80" --rule="/other=ingress-test-2:80"
```

```shell title:"Recuperar apiVersion do ingress"
kubectl api-resources | grep -i ingress
```


## TLS


```shell title:"criar certificado e chave para ssl"
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

---

```shell title:"Cria uma secret a partir de dos certificado e chave criados"
kubectl create secret tls unsafe --cert cert.pem --key key.pem
```

```reference
filePath: "@/Attachments/Kubernetes/ingress/tls-secret.yaml"
```

---

```shell
kubectl create ingress simple --rule="teste.local/=teste:80,tls=unsafe
```

```reference
filePath: "@/Attachments/Kubernetes/ingress/tls-ingress.yaml"
```

---
```shell
curl -vk https://teste.local --resolve teste.local:443:192.168.49.2
```