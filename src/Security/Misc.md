- É possível acessar o endereço de uma service usando o `kubectl proxy`e depois pegando o endereço de uma service e adicionando proxy na frente

```shell
 curl -X GET http://127.0.0.1:8001/api/v1/namespaces/default/services/seccomp-test/proxy
```

- Pegar o pid de um container rodando
```shell
 sudo crictl inspect 79b11c0376a81 | jq '.info.pid'
```


Extrair o certificado de um dado usuario usando jsonpath

```shell
k config view --raw \
	-ojsonpath="{.users[?(.name == 'restricted@infra-prod')].user.client-certificate-data}"
```



```shell
curl -k -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)" https://kubernetes.default/api/v1/namespaces/restricted/secrets  
```