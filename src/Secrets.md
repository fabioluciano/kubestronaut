---
sticker: emoji//1f512
---

- Secrets não são exatamente seguras. Se usa `base64 -n`  para codificar, o que pode ser facilmente "descodificado" usando o comando `base64 -d`
- Secrets não são criptografadas no ETCd
- Qualquer pessoa que puder criar Deployments/Pods neste no namespace da secret vai ser capaz de visualizar os dados.
- Para criar uma secret a partir de um manifesto, é necessário codificar o valor com `echo -n 'string' | base64` . O mesmo não se aplica a forma imperativa
- Uma secret pode ser marcado como imutável utilizando `secret.immutable = true`
- mudar o default mode`pod.spec.volumes.secret.defaultMode: 0400`
- Secrets **montadas** são automaticamente atualizadas no POD caso sejam modificadas
	- As variáveis de ambiente não são atualizadas por que estão anexadas ao processo de PID 1... logo não tem como atualizar


> [!NOTE]- Criação de uma `Secret`
```reference
filePath: "@/Attachments/Kubernetes/secrets/secret-teste.yaml"
```


> [!NOTE]- Criação de um pod com secrets carregadas com `env.valueFrom`
```reference
filePath: "@/Attachments/Kubernetes/secrets/pod-with-secrets-env-value.yaml"
```


> [!NOTE]- Criação de um pod com secrets carregadas com `envFrom`
```reference
filePath: "@/Attachments/Kubernetes/secrets/pod-with-secrets-envfrom.yaml"
```


> [!NOTE]- Criação de um pod com secrets carregadas com `volume`
```reference
filePath: "@/Attachments/Kubernetes/secrets/pod-with-secrets-volume.yaml"
```


> [!NOTE]- Criação de um pod com secrets carregadas com `env.volume-items`
```reference
filePath: "@/Attachments/Kubernetes/secrets/pod-with-secrets-volume-items.yaml"
```
## Comandos úteis

```shell title:"Cria uma secret de forma imperativa"
kubectl create secret generic secretname --from-literal password=12345
```

```shell
kubectl create secret tls myCert --cert my.crt --key my.key
```

```shell
kubectl create secret generic mySecret --fromfile ssh-private-key=./id_rsa
```

```shell
k get secret teste -o jsonpath="{.data.password}" | base64 -d
```

```shell
kubectl set env deploy DEPLOYMENT --from secret/mysecret 
```



```shell title:"Cria uma secret com credencias para se autenticar no dockerhub usando pod.spec.imagePullSecrets "
kubectl create secret docker-registry docker-credentials \
	--docker-server https://index.docker.io/v1/ \
	--docker-email fabio@naoimporta.com \
	--docker-username fabioluciano \
	--docker-password xxxxxxx
```



> [!NOTE]- Criação de um pod com secrets carregadas com `env.volume-items`
```reference
filePath: "@/Attachments/Kubernetes/secrets/deploy-with-imagepullsecrets.yaml"
```