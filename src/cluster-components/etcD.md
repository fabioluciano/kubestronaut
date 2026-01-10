# Etcd

- Banco de dados que guarda os dados  em formato `chave/valor`
- Roda na porta `2379`
- `etcdctl` controla o etcd
- guarda todas as configurações de todos os recursos implantados no cluster 

```shell
kubectl exec etcd-controlplane -n kube-system -- sh -c "ETCDCTL_API=3 etcdctl get / --prefix --keys-only --limit=10 --cacert /etc/kubernetes/pki/etcd/ca.crt --cert /etc/kubernetes/pki/etcd/server.crt --key /etc/kubernetes/pki/etcd/server.key"
```