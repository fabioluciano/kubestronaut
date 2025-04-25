- Intercepta uma requisição para o `kube-apiserver` antes de ser persistido
- A requisição precisa ser autenticada e autorizada
- Permite implementar medidas para reforçar como o cluster é utilizado, e como os recursos criados.
- O [[LimitRange]] [[ResourceQuota]]? é um admission controller 
- Para habilitar um admission controller é necessário modificar o pod do `kube-apiserver`
	- `--enable-admission-plugins`
	- `--disable-admission-plugins` no `/etc/kubernetes/manifests/apiserver.yaml`

```plantuml
"Autenticação" -> "Autorização"
"Autorização" -> "Admission Controller"
```

## Tipos de Admission Controllers
 - Os `Mutating` são chamados primeiro que o `Validating`, visto que qualquer modificação feita, seja validada.
 - `ValidatingAdmissionWebhook`  e `MutatingAdmissionWebhook` apontam para um servidor interno ou externo ao cluster, permitindo a customização
	 - O webhook precisa responder com um objeto permitindo ou negando a requisição `AdmissionReview`
### Validating
 - Faz validações no objeto a ser criado. Permitindo-a ou rejeitando-a

### Mutating
 - Faz modificações no objeto sendo criado

## ImagePolicyWebhook

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: image-bouncer-webhook
  name: image-bouncer-webhook
spec:
  type: NodePort
  ports:
    - name: https
      port: 443
      targetPort: 1323
      protocol: "TCP"
      nodePort: 30080
  selector:
    app: image-bouncer-webhook
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: image-bouncer-webhook
spec:
  selector:
    matchLabels:
      app: image-bouncer-webhook
  template:
    metadata:
      labels:
        app: image-bouncer-webhook
    spec:
      containers:
        - name: image-bouncer-webhook
          imagePullPolicy: Always
          image: "kainlite/kube-image-bouncer:latest"
          args:
            - "--cert=/etc/admission-controller/tls/tls.crt"
            - "--key=/etc/admission-controller/tls/tls.key"
            - "--debug"
            - "--registry-whitelist=docker.io,registry.k8s.io"
          volumeMounts:
            - name: tls
              mountPath: /etc/admission-controller/tls
      volumes:
        - name: tls
          secret:
            secretName: tls-image-bouncer-webhook
```


```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: ImagePolicyWebhook
  configuration:
    imagePolicy:
      kubeConfigFile: /etc/kubernetes/pki/admission_kube_config.yaml
      allowTTL: 50
      denyTTL: 50
      retryBackoff: 500
      defaultAllow: false
```

```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority: /etc/kubernetes/pki/server.crt
    server: https://image-bouncer-webhook:30080/image_policy
  name: bouncer_webhook
contexts:
- context:
    cluster: bouncer_webhook
    user: api-server
  name: bouncer_validator
current-context: bouncer_validator
preferences: {}
users:
- name: api-server
  user:
    client-certificate: /etc/kubernetes/pki/apiserver.crt
    client-key:  /etc/kubernetes/pki/apiserver.key
```


```yaml
    - --enable-admission-plugins=NodeRestriction,ImagePolicyWebhook
    - --admission-control-config-file=/etc/kubernetes/pki/admission_configuration.yaml
```
