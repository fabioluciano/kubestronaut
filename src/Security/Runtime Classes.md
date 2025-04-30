- Permite que seja utilizado mais que um container runtime instalado

## Gvisor
 - Adiciona mais uma camada entre o userspace e o kernel space
 - Como é feito para funcionar com containers, vai fornecer um número limitado de syscalls para que as aplicações funcionem
 - É composto de dois componentes:
	 - Sentry - Intercepta e responde a requisições
 - Ele vai funcionar ocmo um proxy entre o kernel e a aplicação
 - Sem utilizar um sandbox, o mesmo kernel da máquina, será o kernel do container
 - Como tem mais instruções, pode ser mais lento
 - Não funciona para qualquer aplicações



```reference
filePath: "@/Attachments/Kubernetes/security/runtimeclass/runtimeclass-runsc.yaml"
```


```reference
filePath: "@/Attachments/Kubernetes/security/runtimeclass/runtimeclass-teste.yaml"
```


```shell
kubectl exec -ti runtimeclass-teste -- uname -a
```

```shell
kubectl exec -ti runtimeclass-teste -- dmesg
```