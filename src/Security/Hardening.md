## Reduzir a superficie de ataque

- Use o principio do least prigilégio
- Remove pacotes obsoletos 
- Limite o acesso
- Remove serviços obsoletos
- Restrinja  módulos do kernel obsoletos
- identifique e corrija portas abertas

## Limitar o acesso a nós
- os nós não devem estar expostos à internet
- autorizar conexões a partir de fontes conhecidas

## SSH Hardening

- habilitar a conexão aos nós usando keypair
- desabilitar o usuário root a fazer ssh e setar `PermitRootLogin no`
- desabilitar password `PasswordAuthentication no`

## open ports

Qual processo tá sendo usado na porta tal...

```shell title:"Lista todas as portas abertas, bem como o processo associado"
sudo netstat -tunpl | grep -w LISTEN
```


```shell
sudo ss -tupl
```