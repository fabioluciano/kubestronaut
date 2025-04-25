- Módulo de segurança do Kernel
- FAz restrição de systemcalls da user space para o kernel namespace



```shell
mkdir -p /var/lib/kubelet/seccomp/profile
```


```reference
filePath: "@/Attachments/Kubernetes/security/seccomp/seccomp-teste.yaml"
```


tail -f  /var/log/syslog