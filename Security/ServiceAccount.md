- Existem dois tipos de ServiceAccounts, uma de usuário e outra de serviço;
- Usada para autenticar um serviço para se comunicar com a API do kubernetes;
- A partir da versão 1.24, tokens não são criados automaticamente na criação de uma SA
	- Você pode criar uma secret do tipo service account e associar a serviceaccount. Esse token não terá expiração
	- ou usar a api para recuperar o token `kubectl create token pod-with-serviceaccount`. Terá a expiração dada pelo servidor... default 1hora
- Todo namespace possui uma service account criada. 
	- Essa service account é automaticamente montada dentro do pod.
- Não é possível editar a serviceaccount de um pod. É necessário deletar e recriar o pod;
- As credenciais fornecidas pela service account, serão automaticamente montadas no diretório `/var/run/secrets/kubernetes.io/serviceaccount` . A propriedade `pod.automountServiceAccountToken: false` desabilita esse comportamento.
	- Essa opção funciona tanto para sa.spec quanto pod.spec


> [!NOTE]- Service Account
```reference
filePath: "@/Attachments/Kubernetes/serviceaccount/serviceaccount-test.yaml"
```


> [!NOTE]- Pod with service account
```reference
filePath: "@/Attachments/Kubernetes/serviceaccount/pod-with-serviceaccount.yaml"
```

> [!NOTE]- Pod with service account
```reference
filePath: "@/Attachments/Kubernetes/serviceaccount/pod-with-serviceaccount-automount-false.yaml"
```


> [!NOTE]- Service Account with token attached
```reference
filePath: "@/Attachments/Kubernetes/serviceaccount/serviceaccount-with-token.yaml"
```


```shell title:"Cria uma serviceaccount"
kubectl create serviceaccount teste
```

```shell title:"Cria um token com uma determinada duração a partir de uma serviceaccount"
kubectl create token SERVICEACCOUNT --duration=3600s
```