## Volumes

- É possível montar um volume em um Pod que não está anexado a um PV, como por exemplo PVs dos tipos abaixo:
	- hostPath - Vollume criado a partir de um diretório persistente no nó
		- É anexado a um host
	- emptyDir - Volume efemero, o dado vai ficar armazenado em um diretório temporário
		- É anexado ao um host, então não é possível anexá-lo a vários pods instances
	- `persistentVolumeClaims` possibilitam a utilização de um `PersistentVolume`
- Os volumes definidos em `pod.spec.volumes` precisam ser referenciados em `pod.spec.containers.volumeMounts`


> [!NOTE]- `Pod` with volume without `PersistentVolume`
```reference
filePath: "@/Attachments/Kubernetes/persistentvolumes/hostpath-volume-pod.yaml"
```

```reference
filePath: "@/Attachments/Kubernetes/persistentvolumes/pod-with-emptydir-volume.yaml"
```

## Persistent Volumes

### Conceitos

- Possui um ciclo de vida independente do ciclo de vida de um pod.
- Existem diversos tipos de `PVs`, todos implementados como plugins;
- É uma pool de storage disponível por todo o cluster
- É um objeto que pertence ao cluster, enquanto `PVCs`são por namespace;

> [!NOTE]- `PersistentVolume`
```reference
filePath: "@/Attachments/Kubernetes/persistentvolumes/hostpath-persistent-volume.yaml"
```

### Propriedades importantes
- `persistenvolume.spec.accessModes`:
	- `ReadWriteOnce`: O Volume pode ser montado para leitura e escrita em **apenas** um nó;
	- `ReadOnlyMany`: O volume pode ser montado como leitura em vários nós;
	- `ReadWriteMany`: O volume pode ser montado como leitura e escrita em vários nós;
	- `ReadWriteOncePod`: O volume pode ser montado como leitura e escrita em apenas um [[Pods]]
- `persistentVolume.spec.persistentVolumeReclaimPolicy`:
	- `Retain`: Os dados não serão apagados, porém não poderá ser utilizada por outro claim até que os metadados sejam limpos;
	- `Delete`:  Os dados do volume serão apagados. O comportamento varia de acordo com o provisionador
	- `Recycle`: Apesar de depreciado, mantêm os dados.
- `persistentvolume.spec.volumeMode:
	- `FileSystem`: Entrega o disco formatado
	- `Block`: Entre uma stream block para ser formatada.
- `capacity.storage`: Quanto de recurso será reservado 


```reference
filePath: "@/Attachments/Kubernetes/persistentvolumes/pod-with-pvc.yaml"
```

```reference
filePath: "@/Attachments/Kubernetes/persistentvolumes/pv-and-pvc-delete-policy.yaml"
```

```reference
filePath: "@/Attachments/Kubernetes/persistentvolumes/pv-and-pvc-recycle-policy.yaml"
```
## Persistent Volume Claims

- É necessário criar um `PersistentVolumeClaim` para utilizar um `PersistentVolume`.
- Cada [[Storage#Persistent Volume Claims|Persistent Volume Claim]] está ligado a um `PV`. E somente a um [[Storage#Persistent Volumes|Persistent Volume]]
- Quando um [[Storage#Persistent Volume Claims|Persistent Volume Claim]] captura um PV, nenhum outro `PVC`, conseguirá usar o resto do storage disponível no [[Storage#Persistent Volumes|Persistent Volume]]
- O kubernetes tentará encontrar uma [[Storage#Persistent Volumes|Persistent Volume]]com as capacidades indicadas por um [[Storage#Persistent Volume Claims|Persistent Volume Claim]]
- Caso não haja um [[Storage#Persistent Volumes|Persistent Volume]]disponível com as capacidades descritas, o [[Storage#Persistent Volume Claims|Persistent Volume Claim]] ficará no `spec.phase` Pending. Quando o [[Storage#Persistent Volume Claims|Persistent Volume Claim]] encontrar um [[Storage#Persistent Volumes|Persistent Volume]], ele mudará para o estado 
- O pvc ficará em um estado de terminating infinitamente se tiver um pod utilizando-o
- Define uam requisição de storage

### Propriedades importantes
- `persistenvolume.spec.accessModes`:
	- `ReadWriteOnce`: O Volume pode ser montado para leitura e escrita em **apenas** um nó;
	- `ReadOnlyMany`: O volume pode ser montado como leitura em vários nós;
	- `ReadWriteMany`: O volume pode ser montado como leitura e escrita em vários nós;
	- `ReadWriteOncePod`: O volume pode ser montado como leitura e escrita em apenas um [[Pods]]
- `persistentvolume.spec.volumeName`: Força a utilização de um determinado volume
- `persistentvolume.spec.resources`:
	- `persistentvolume.spec.resources.requests`: 
		- `persistentvolume.spec.resources.requests.storage`
	- `persistentvolume.spec.resources.limits`:
		- `persistentvolume.spec.resources.limits.storage`

> [!NOTE]- `PersistentVolume`
```reference
filePath: "@/Attachments/Kubernetes/persistentvolumes/pv-and-pvc.yaml"
```

## Storage Class

- Quando você cria um [[#Persistent Volumes]]e utiliza um [[#Persistent Volume Claims]]para alocar o valor de um PV por uma PVC, é chamado de provisionamento estático de volumes;
- Com StorageClasses, utilizando um provisionador, você pode automaticamente alocar o valor solicitado. Ou seja, um PVC é criado chamando um determinado storage class. Isso é chamado provisionamento dinâmico


> [!NOTE]- `PersistentVolume`
```reference
filePath: "@/Attachments/Kubernetes/persistentvolumes/storageclass-localpath.yaml"
```

### Comandos úteis:

```shell title:"Recupera o estado de um PVC"
k get pvc my-persistent-volume-claim -o jsonpath="{.status.phase}"
```