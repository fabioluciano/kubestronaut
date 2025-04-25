- Quando a master não está configurada como HA e a máquina morrer, os nodes continuarão a rodar
	- Se algum pod morrer e ele for parte de um replication controller, ele não vai subir, já que o schedular e controll manager não estão funcionando
	- não será possível acessar o api server, logo comandos kubectl não funcionarão
- O kubeapi deve ser colocaco atrás de um proxy reverso para garantir HA
- Os outros componentes rodarão em um esquema de ativo/standy, sendo que um responde, e outro fica aguardando a indisponibilidade do outro
	- Deve-se eleger o líder dos seguintes

## ETCd
- O etc garante que todos os nós do cluster tenham a possibilidade de ler e escrever
- Um lider é eleito e mesmo que uma scrita aconteça em um follower(slave), ele vai pasasar para o lider
- Um registro é considerado completo quando a maioria dos membros dizem ok
	- Maioria = Quorum = Numero de insitancia / 2 + 1