- Permitem responder perguntas como:
	 - Quem fez?
	 - Quando fez?
	 - O que foi feito?
	 - Como a modificação foi feita?
- Garante aderência as regulações de compliance
- Provê uma trilha que pode ser utilizada para investigar e entender o impacto de um incidente
- Histórico de mudança
- Garantir que os recursos são gerenciados de maneira eficiente
- Identifica a causa raiz de uma problema


Estágios
 - `RequestReceived` - Assim que recebe a requisição
 - `RequestStarted` - Os cabeçalhos foram enviados mas não o corpo da mensagem... watch
 - `RequestComplete` - A resposta foi enviada e não serão enviadas outras informações
 - `Panic`- Ocorreu um panico

- Tipos de políticas
	- None - Não logará eventos - Util quando se quer excluir certos eventos
	- Metadata - Logará os metadados relacionados a uma requisição. Mas não a requisição
	- Request - Metadados e o corpo da requisição
	- RequestResponse - Metadata/Request e Response


- `--audit-log-path` - Informa a localização onde os logs de auditoria serão salvos
- `--audit-policy-file` - Arquivo que contém as políticas configuradas do audit
- `--audit-log-maxage` - Informa por quantos dias os logs serão guardados. O recomendado são 30 dias
- `--audit-log-maxbackup` - Informa quantos arquivos de rotação serão retidos. O recomendado são 10.
- `--audit-log-maxsize`- Informa o tamanho máximo que o arquivo poderá ter. O recomendado são 100

```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
  namespaces: ["prod"]
  verbs: ["delete"]
  resources:
  - group: ""
    resources: ["secrets"]
```


ADICIONAR `- level: None` PARA DESABILITAR TODOS OS OUTROS E DEIXAR SOMENTE O QUE FOR CONFIGURADO



```yaml
    volumeMounts:
    - mountPath: /etc/kubernetes/prod-audit.yaml
      name: audit
      readOnly: true
    - mountPath: /var/log/prod-secrets.log
      name: audit-log
      readOnly: false
  volumes:
  - name: audit
    hostPath:
      path: /etc/kubernetes/prod-audit.yaml
      type: File
  - name: audit-log
    hostPath:
      path: /var/log/prod-secrets.log
      type: FileOrCreate
```