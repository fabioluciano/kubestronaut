# StatefulSet

- Assim como [[Deployments]], também possuem um template do pod que subirá , pode escalar o número de pods, rollbacks.
- Mantêm a identidade dos pods que são criados
- No StatefulSet,  os pods presentes são criados em uma order sequencial. O primeiro pod têm que estar no status running e ready para que o próximo suba.
- Atribui um indice a cada pod, começando com 0, que refletirá na criação de um DNS único
- Mesmo que o pod morra, ele voltará com o mesmo nome. Ele mantêm sua identidade.
- É necessária um service
- `statefulset.sepc.volumeClaimTemplates`: Cria um PVC que criará um PV
- Pare remover um statefulset, primeiro se scala ara 0, depois deleta

> [!NOTE]- Replication Controller
```reference
filePath: "@/Attachments/Kubernetes/statefulset/statefulset-test.yaml"
```
### Propriedades importantes

- `spec.podManagementPolicy = Parallel`: Não seguir a order de esperar um ser criado/destruído para iniciar/apagar o próximo. 
- `spec.serviceName`: Service a ser utilizada para compor os dns dos pods criados.
- `spec.volumeClaimTemplate`: Cria uma PVC para cada replica do Statefulset


