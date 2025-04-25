# Docker

- Existem duas formas de definir um entrypoint, a forma `exec` e a forma `shell`
- Por padrão, o docker rodará o comando usando o usuário root.
- Todas as capabilities do linux estão descritas no arquivo `/usr/include/linux/capability.h` ou `man 7 capabilities`

## Exec
```Dockerfile
ENTRYPOINT ["command", "ARG", "ARG"]
CMD ["-c"]
```

- Fará com que o comando seja executado com o PID 1
- O `CMD` é o args do `Kubernetes`

## Shell

```Dockerfile
ENTRYPOINT command argument argument
```

- Fará com que qualquer `CMD`seja ignorado
- Não será o PID 1, visto que o comando do entrypoint será executado como subcomando do `sh -c`

