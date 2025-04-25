- Garantir que ao menos um mecanismo de política de controle seja implementado. Pod Security Admission
- No namespace, utilizando a label `pod-security.kubernetes.io/<MODE>: <LEVEL>`. Sendo:
- Level:
	- `privileged`:  Propositalmente aberta, e irrestrita;
	- `baseline`: Prevê o prevenimento de escalação de privilégios
	- `restricted`: Complemetamente restrita. Segue as melhores práticas de hardening de pods
- Modes:
	- `enforce`: Violações a política farão com que a requisição seja rejeitada;
	- `audit`: Violações a política farão com que auditadas e o evento guardado, porém permitida;
	- `warn`:  Dispararão um Warning para o usuário, mas serão permitidas
- É um admission control, `PodSecurity` habilitado por padrão


```kubectl
kubectl exec -n kube-system kube-apiserver-controlplane \
-- kube-apiserver -h | grep enable-admission
```


'E UMA LABEL E NAO UMA ANOTATION'
```shell
kubectl label ns NAMESPACE pod-security.kubernetes.io/MODE=LEVEL
```

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: AdmissionConfiguration
plugins:
  - name: PodSecurity
    configuration:
      apiVersion: pod-security.admission.config.k8s.io/v1
      kind: PodSecurityConfiguration
      defaults:
        enforce: baseline
        enforce-version: latest
        audit: restricted
        audit-version: latest
        warn: restricted
        warn-version: latest
      exemptions:
        usernames: []
        runtimeClassNames: []
        namespaces: [my-namespace]

```