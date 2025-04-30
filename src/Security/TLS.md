## Certificado
 
-  Utilizado para garantir a confiabilidade entre a comunicação entre duas entidades
 - **Criptografia assimétrica** é quando uma chave se usa uma chave pública para criptografar, a a chave privada para descriptografar
 - **Criptografia simétrica** é quando a mesma chave é utilizada para criptografar e descriptografar uma informação
 - Autoridade certificadora é uma organização conhecida que assina seu certificado
 - Todo o processo de geração de chaves, incluindo as pessoas, as CAs, é chamado DE PKI - Public Key Infraestruture
 - Geralmente as chaves públicas são `.crt` e `.pem`
 - Chaves privadas geralmente são `.key`ou `*-key.pem`

```shell title:"gera uma chave privada"
openssl genrsa -out mykey.key 1024
```

```shell title:"Gera uma chave publica"
openssl rsa -in mykey.key -pubout > pub.pem
```

---
## Kubernetes

- Todos os componentes do cluster têm um par de certificados

```shell title:"imprime informações sobre um sertificado"
openssl x509 -in cert.crt -text -noout
```


![[CleanShot 2024-11-02 at 02.37.04.png]]