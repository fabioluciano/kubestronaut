- Feito para executar uma tarefa em um dado período do dia baseado no `cronjob.spec.schedule`
- Basicamente é um wrapper para o Job. Você coloca o `job.spec` dentro de `cronjob.spec.jobTemplate`
- É importante notar que é possível setar o `cronjob.spec.timeZone` que afetará o funcionamento do `cronjob.spec.schedule`
- O Cronjob vai criar um job, assim como um deployment cria uma replicaset

```reference
filePath: "@/Attachments/Kubernetes/cronjob/cronjob-date.yaml"
```

## Comandos úteis

```shell
k create cronjob date --image busybox --schedule="*/1 * * * *" -- date
```



```shell title:"Executa um job a partir de um cronjob, não precisando esperar"
kubectl create job JOBNAME --from cronjob/CRONJOBNAME
```