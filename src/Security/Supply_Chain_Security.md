- Basicamente se trata da implementação de pipelines para fazer verificações e validações dos componentes

- Permite a identificação prematura de vulnerabilidades
- Melhor gereciamento de recursos
- Melhoria de compliance
- Respostas efetivas a incidentes
- Melhhora a postura de segurança da organização


## SBOM

- Software Bill of Materials
- Funciona como uma receita do que o software é composto
	- Componentes de software
	- Dependencias
	- Composições de software
	- Vulnerabilidades de segurança
	- Licenças
	- Versões

- Dá dois formatos: `SPDX`e `CycloneDX`

- GERAR SBOM -> SCAN -> Analyzar -> Remediar -> Monitorar

Ferramenta: syft 

```shell
syft dockerimage:tag -o spdx-json
```

```shell
syft docker.io/kodekloud/webapp-color:latest -o spdx-json  > /root/webapp-spdx.sbom
```

grype do sbom.json

```shell
grype sbom:/root/webapp-sbom.json -o json > /root/grype-report.json
```

```shell
bom generate -i registry.k8s.io/kube-apiserver:v1.21.0 --format json > spdx.json
```

```shell
bom document outline spdx.json
```

## Minimize base image footprint

- Não buildar multiplas aplicações em uma imagem
- usar imagens de fontes confiáveis
- deixar as imagen o menor possivelk
- usar distroless images

## Kube-linter

```shell
kube-linter lint teste-deployment.yaml
```




## Kubesec


```shell
kubesec scan bluegreen-service-based.yam
```



## trivy


```shell
trivy config Dockerfile
```


```shell
trivy k8s --report summary all
```

```shell
trivy k8s pod/nginx
```

```shell
trivy image --severity HIGH --output /root/python.txt public.ecr.aws/docker/library/python:3.9-bullseye
```

```shell
trivy image --input alpine.tar --format json --output /root/alpine.json
```


```shell
trivy image nginx --format json
```