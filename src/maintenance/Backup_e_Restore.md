## Etcd

- `--data-dir`é a flag que mostra qual é o diretório que guarda os dados do etcd


```shell
ETCDCTL_API=3 etcdctl snapshot save snapshot.db
```

- pra restaurar primeiro para-se o [[kube-apiserver]]

```shell
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db --data-dir /var/lib/etcd-from-backup
```

- configurar o etcd data-dir para apontar para o novo caminho
- reload daemon
- restart etcd
- restart [[kube-apiserver]]
- é necessário informar o
	- `--endpoints=https://127.0.0.1:2379`
	- `--cacert=/etc/etcd/ca.crt`
	- `--cert=/etc/etcd/etcd-server.crt`
	- `--key=/etc/etcd/etcd-server.key`


```plantuml
@startuml
skinparam defaultTextAlignment center


start
:Identificar se o ""etcd"" está rodando\n como um pod estático ou como\n um serviço do ""systemd"";
floating note left: Verificar se o manifesto do ""etcd""\n está presente no diretório de pod estáticos
:Deve-se parar o ""kube-apiserver"" para que\nnovos recursos não sejam criados;
:Defini-se a versão da API do etcd que deseja-se usar\n\n""export ETCDCTL_API=3"";

if(""kube-apiserver"") then(systemd)
	:Parar o serviço do ""kube-apiserver""\n\n""systemctl stop kube-apiserver"";
else (static pod);
	:Parar o pod do ""kube-apiserver"" \nremovendo-o(movendo-o) do diretório\nde pods estáticos;
endif


if(operação) then(backup)
	:Efetua o backup do ""etcd"" em um dado arquivo\n\n""etcdctl ~--endpoints $ENDPOINT  \"" \n"" ~--cacert $CACERT \ ""\n  ""~--cert $CERT \ ""\n  ""~--key $KEY \ ""\n  ""**snapshot save snapshot.db**"";
	note left
	  Os certificados e chave utilizados, podem
	  ser identificados usando as configurações
	  usadas pelo ""kube-apiserver"".
	  ----
	  ""~--etcd-servers"" <&arrow-right> ""~--endpoints""
	  ""~--etcd-cafile"" <&arrow-right> ""~--cacert""
	  ""~--etcd-certfile"" <&arrow-right> ""~--cert""
	  ""~--etcd-keyfile"" <&arrow-right> ""~--key""
	end note
	:Verificar status do backup\n\n""etcdctl **snapshot status snapshot.db**"";
	
else (restore)
	:""etcdctl snapshot restore snapshot.db""\n ""--data-dir /var/lib/etcd-from-backup"";
	note right
		Como a operação não utiliza o servidor do
		""etcd"", não é necessário informar nenhum
		certificado
	end note

	if(""kube-apiserver"") then(systemd)
		:Parar o serviço do ""etcd""\n\n""systemctl stop etcd"";
		:Identificar na saída do status do ""systemd""\n qual o caminho do unit do ""etcd"";
		:Modificar a flag ""--data-dir"" no arquivo de unit\npara apontar para o novo caminho\n""/var/lib/etcd-from-backup"";
		:Efetuar o reload das configurações do ""systemd""\n\n""systemctl daemon-reload"";
		:Reiniciar o serviço do "etcd" no ""systemd""\n\n""systemctl restart etcd"";
	else (static pod);
		:Modificar o manifesto do ""etcd"" colocando\na flag ""--data-dir"" apontando para o novo caminho;
		:Remover o pod do ""etcd"" do namespace ""kube-system"";
	endif
	
endif

if(""kube-apiserver"") then(systemd)
	:Reiniciar o serviço do ""kube-apiserver""\n\n""systemctl start kube-apiserver"";
else (static pod);
	:Retornar o pod do ""kube-apiserver"" \nrecriando-o(movendo-o) no diretório\nde pods estáticos;
endif


end
@enduml
```