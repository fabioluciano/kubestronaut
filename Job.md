 - Feitos para executar uma tarefa específica e finalizar
 - Você pode fazer a mesma coisa com um pod normal, mas ele vai ficar reexecutando o processamento diversas vezes, resultando em um `CrashLoopBackOff`. Isso por que [[Pods]]são idealizados para executar Long running workloads. Esse comportamento é dado pela propriedade `pod.spec.restartPolicy`
 - É um pod em que o `pod.spec.restartPolicy` é setado para Never
 - É bom lembrar que cada Job criará um ou mais pods para executar sua tarefa
 - `job.spec.ttlSecondsAfterFinished` limpa automaticamente os jobs
 - Para executar múltiplos pods da task, utilize `job.spec.completions`. Os pods são criados de maneira sequencial. O segundo só será criado se o primeiro finalizar.
	 - O scheduler vai continuar a executar pods, até o numero de completions seja atingido
	 - É possível alterar esse comportamento adicionando a propriedade `job.spec.parallelism`, dizendo quantos serão criados em paralelo.
	 - `job.spec.backoffLimit` é o número de vezes que vai dar erro até ele desistir


```reference
filePath: "@/Attachments/Kubernetes/job/pod-with-expr.yaml"
```

```reference
filePath: "@/Attachments/Kubernetes/job/job-execute-expression.yaml"
```

```reference
filePath: "@/Attachments/Kubernetes/job/job-execute-expression-completions.yaml"
```

## Comandos uteis

```shell
 create job job-execute-expression --image ubuntu $kdry -- expr 3 + 4 > job-execute-expression.yaml
```