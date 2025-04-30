- Roda uma aplicação em todos os nós
	- Não vai rodar se tiver um taint impedindo-o
- É útil quando quando se instala um agent que precisa estar rodando em TODOS os nós do cluster
- DaemonSet não possui replicas. Ele segue o número de nós em seu cluster

```reference
filePath: "@/Attachments/Kubernetes/daemonset/daemonset-test.yaml"
```


## Passos para criação de um daemonset

1) Criar um deployment
2) Transformar o kind para daemonset
3) Remover spec.replicas e spec.strategy