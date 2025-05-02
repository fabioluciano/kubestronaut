# Atualização do Sistema Operacional

- Se os nó ficar mais de cinco minutos sem reponder. Os pods daquele nós serão terminados. 
	- Caso sejam partes de um replicaset, serão recriados em outro nó;
	- Caso seja um pod que não seja parte de um replication controller, ele vai ser perdido
- Caso você faça uma tarefa que fará com que um nó entre no estado de notready
	- executar o drain no nó
		- O drain matará os pods neste node e criará em outro
		- ao mesmo tempo, o nó será marcado como cordoned(marcado no unschedule)
		- após estar tudo certo, o nó deve ser uncordon
		- o comando cordon vai marcar o nó como unshedulable, sem mover nada... nenhum novo pod será alocado