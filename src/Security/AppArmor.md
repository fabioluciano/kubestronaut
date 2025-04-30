- Módulo de segurança do kernel do linux
- Sumplementa os permissionamentos de usuários e grupos do linux
- Pode-se limitar que programas leia/escrevam em diretórios
- Desabilitar a rede
- Todos estes permissionamentos são atrelados a perfis
- Os perfis precisam ser adicionados aos workernodes
- Existem três tipos de modos de appamor
	- enforce - o app armor vai monitorar e forçar as regras
	- complain - vai permitir executar o processo, mas um log será gerado
	- unconfined - permite qualquer coisa sem fazer nada

```shell title:"Instala o apparmor"
apt install apparmor-utils
```

```shell title:"checar se o apparmor está rodando"
###Serviço
systemctl status apparmor


sudo aa-status

 cat /sys/module/apparmor/parameters/enabled
```


```shell title:"Listar todos os profiles disponíveis"
cat /sys/kernel/security/apparmor/profiles
```

```shell title:"Gera um profile para o curl"
aa-genprof curl
```

```shell title:"Lsita a aprova todos os recursos utilizado pela aplicação"
aa-logprof
```

```shell title:"carrega um arquivo de profile do apparmor"
apparmor_parser -r ARQUIVOPROFILE
```

```shell title:"Recupera qual é o perfil que está sendo utilizado"
# Dentro do pod

cat /proc/1/attr/current
```

```reference
filePath: "@/Attachments/Kubernetes/security/apparmor/denyall-profile"
```



```reference
filePath: "@/Attachments/Kubernetes/security/apparmor/apparmor-test-annotations.yaml"
```

```reference
filePath: "@/Attachments/Kubernetes/security/apparmor/apparmor-test-securitycontext.yaml"
```
