# kube-proxy

- Todo pod pode se comunicar com qualquer outro pod
- A rede de pods é a mesma utilizada por todos os nós do cluster
- É um daemonset que garante que quando um serviço é criado, as regras de firewall(iptables) apropriadas sejam criadas