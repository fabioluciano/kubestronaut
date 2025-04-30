> **Configuraões para o vim** 
```shell
set ai
set et
set cursorcolumn
set cursorline
set sw=2
set sts=2
set si
set ts=2
syntax on
```


> Configurações para o .bashrc
```shell
alias k=kubectl`
complete -o default -F __start_kubectl k
alias kg='kubectl get'
alias kd='kubectl describe'
alias ke='kubectl explain'
alias kl='kubectl logs'
alias kp='kubectl port-forward'
alias kr='kubectl run'
alias ked='kubectl edit'
alias kex='kubectl exec -it'
source .bashrc
export kdry="--dry-run=client -o yaml"
```
