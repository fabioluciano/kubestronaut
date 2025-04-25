- Provê a possibilidade de isolar aplicações usando os namespaces do Kernel do linux 
- Contém a aplicação e todas suas dependências
- As imagens dos containers são capturadas de um registrador
- As imagens são altamente parametrizas para serem rodadas em qualquer computador

## Container Runtime

 - Aplicação que roda um container
 - Dá pra comparar com o systemD do linux, = subindo aplicações
 - Um examplo é o `runc`
- O Docker e o Podman e o Kubenetes, como Container Engine, manipularão o runc

## Container Registry

- É uma loja de imagens de container
- É possível ter registradores publicos ou pirvados
- Para rodar uma imagem de um container é necessário um FQCN(Fully Qualified Container name)
- Se for utilizar o podman, você deve passar o endereço inteiro (eg. docker.io/library/nginx)

```shell title:"Run a container"
docker run -d nginx
podman run -d docker.io/library/nginx
kubectl run -d nginx --image docker.io/library/nginx
```


```shell title:"Retorna informações sobre um container"
docker [image] inspect image
```

```shell title:"Cria um imagem a partir de um container rodando"
docker commit CONTAINER IMAGE:TAG
```