sha512sum

para pegar o sha de um pod do kubesystem rodando..

rodar ps aux pra pegar o PID...
entrar no diretório /proc/PID/root
find . | grep apiserver
sha512...