# ConfigMap

- Forma de guardar dados não sensíveis
- Guarda arquivos ou itens usando chave=valor
- Pode ser utilizado como um volume dentro do pod, ou como variável de ambiente
- Ao alterar um configmap, é necessário um restart no pod, visto que a alteração não é automaticamente atualizada
- Um configmap pode ser marcado como imutável utilizando `configmap.immutable = true`

> [!NOTE]- Criação de um `ConfigMap` simples
```reference
filePath: "@/Attachments/Kubernetes/configmap/configmap-teste.yaml"
```

---

> [!NOTE]- Utilização de um `ConfigMap` . Sendo que todas as variáveis definidas serão carregas como variáveis de ambiente
```reference
filePath: "@/Attachments/Kubernetes/configmap/pod-with-configmap-env-valuesfrom.yaml"
```
---
> [!NOTE]- Utilização de um `ConfigMap` . Sendo que apenas a `key` especficada será carregada como variável de ambiente
```reference
filePath: "@/Attachments/Kubernetes/configmap/pod-with-configmap-env-key.yaml"
```
---
> [!NOTE]- Utilização de um `ConfigMap` . Sendo que todas as variáveis serão carregadas como um arquivo dentro do pod.
```reference
filePath: "@/Attachments/Kubernetes/configmap/pod-with-configmap-volume.yaml"
```
---
> [!NOTE]- Utilização de um `ConfigMap` . Sendo que será montada um arquivo com uma `key`definida.
```reference
filePath: "@/Attachments/Kubernetes/configmap/pod-with-configmap-volume-items.yaml"
```

## Comandos úteis

```shell title:"Cria um template de configmap"
kubectl create configmap teste --from-literal chave=valor --from-literal chave1=valor1 $kdry
```


```shell
kubectl set env deploy MYDEPLOY CHAVE=VALOR
```

```shell 
kubectl create cm cif --from-literal teste=teste
kubectl set env deploy teste --from configmap/cif
```


```shell title:"cria um configmap a partir de um arquivo com o nome especificado" 
kubectl create configmap teste --from-file=index.html
```