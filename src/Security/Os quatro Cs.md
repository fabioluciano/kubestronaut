
# Cloud
- É necessário implementar regras de segurança que previna o acesso de usuários não autorizados aos recursos
- É necessário se atentar a diminuir a superfície de ataque a nível de
	- Servidores
	- Datacenter
	- Rede

## Cluster
- é necessário que os mecanismos que permitem a administração dos componentes do cluster tenham implementados requisitos como autenticação e autorização
- É necessário se atentar a diminuir a superfície de ataque ao nível de
	- [[Primitivos de Segurança#Autenticação|Autenticação]]
	- [[Primitivos de Segurança#Autenticação|Autorização]]
	- [[Admission Controllers]]Admissão
	- [[NetworkPolicy]]Políticas de Rede

## Containers
- Restringir quais imagens podem rodar em seu cluster
- É necessário se atentar a diminuir a superfície de ataque a nível de
	- Restringir imagens que podem rodar no cluster
	- Supply Chain
	- SandBoxing
	- Privileged

## Code