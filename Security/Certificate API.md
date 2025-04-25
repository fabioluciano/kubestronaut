
- Primeiro se cria um certificado
- Depois se cria uma Request de assinatura
- Base64 nessa request que será enviada para o [[kube-apiserver]]
- O controller manager que controlará o que será assinado

```shell title:"Gera o certificado"
openssl genrsa -out fabioluciano.key 2048
```

```shell title:"Gerar requisicão de certificado"
openssl req -new -key fabioluciano.key -subj "/CN=fabioluciano" -out fabioluciano.csr
```


```shell
cat fabioluciano.csr | base64 -w 0
```


```reference
filePath: "@/Attachments/Kubernetes/certificates/certificatesignrequest.yaml"
```

```shell
kubectl certificate approve fabioluciano
```

```shell
kubectl get certificatesigningrequests fabioluciano \
	-o jsonpath='{.status.certificate}' | base64 -d > certificate.crt
```


OU

```shell
sudo openssl x509 -req -in benicio.csr \
	-CA /etc/kubernetes/pki/ca.crt \
	-CAkey /etc/kubernetes/pki/ca.key  \
	-CAcreateserial -out benicio.crt -days 10000
```


```shell
kubectl config set-credentials fabioluciano \
  --client-key=$(pwd)/fabioluciano.key\
  --client-certificate=$(pwd)/fabioluciano.crt \
  --embed-certs=true
```

```shell
kubectl config set-context fabioluciano \
  --cluster=kubernetes 
  --user=fabioluciano
```