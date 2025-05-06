# Endpoints

- Coleção de Ips e portas expostas pelos pods selecionados pelo pod
- Todas vez que um pod é removido ou adicionado ao seletor, o endpoint é atualizado
- Só podem ter 1000 ips dentro de um endpoint. ou seja, não pode ter mais de 1000 replicas rodando...
- Foi criado o EndpointSlice para resolver os problemas dos endpoints. Ele também guarda informação do nó

## EndpoitsSlices

- Faz o mapeamento dos Ips dos pods para a service criada
