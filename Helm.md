- É um gerenciador de pacotes do Kubernetes
- Consiste nas ferramenta helm e os charts, que são as aplicações que serão instaladas
- Um helm chart contém o seguinte:
	- Descriçao do pacote
	- Templates dos manifestos

```shell title:"Adiciona um repositório helm"
helm repo add REPONAME REPOURL
```

```shell title:"Atualiza os repositórios"
helm repo update
```

```shell title:"Lista os repositórios helm"
helm repo list
```

```shell title:"Faz a busca em um repositório helm"
helm search repo REPONAME
```


```shell title:"Instala um helm chart"
helm install RELEASENAME CHART
```

```shell title:"Lista os helmcharts instalados"
helm list
```

## Helm Chart

- São templates de manifestos a serem aplicados em um cluster
- Os valores customizados são guardados num arquivo chamado values.yaml
- Os valores disponíveis em values.yaml são os valores padrão do chart

```shell title:"Lista todos os valores disponíveis"
helm show values
```

```shell title:"Instala com um values customizado"
helm install NAME CHART --values values.yaml
```

```shell title:"Instala com um values customizado"
helm install NAME CHART --set KEY=VALUE
```

```shell title:"Mostra os valores usados"
helm show values RELEASENAME
```