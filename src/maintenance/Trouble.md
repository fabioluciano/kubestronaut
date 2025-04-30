- Se o kubectl não estiver respondendo é o kubeapi server que não está funcionando...
	- Olhar com critrl o que está acontecendo
- Se um pod está em pending state e nàoi alocado nenhum nó, é o scheduler
- Se ao scalar a aplicação, não  é escalado, é o controller manager


```plantuml

start

:O Cliente envia o comando ""kubectl""\npara criação de um ""deployment"";
:O Api server manda envia o objeto\na ser criado para o ""etcd"";
:O ""kube-scheduller"" faz a análise de qual\nserá o melhor nó para alocar o pod, baseado\nem requisitos como recursos e affinities;
end
```