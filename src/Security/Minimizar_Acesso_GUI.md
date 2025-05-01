
- Criar service account
- k create sa admin-dashboard
- criar clusterolebinding clusterrole
-  k create clusterrolebinding aaaaab --clusterrole cluster-admin --serviceaccount default:admin-dashboard
 k create token admin-dashboard -n default
- **Não habilitar --insecure-port --enable-insecure-login
- habilitar --auto-generate-certificates
- A service deve ser ClusterIP, não nodeport**