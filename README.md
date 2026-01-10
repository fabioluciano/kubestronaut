# Como me tornar um Kubestronaut

![Logo](src/assets/logo.png)

Este é um guia abrangente em português sobre Kubernetes, focado em ajudar profissionais a se tornarem Kubestronauts (Kubernetes Blue Belt) através da preparação para as certificações oficiais da Cloud Native Computing Foundation (CNCF).

## 🎯 Objetivo

Fornecer material de estudo estruturado em português para as seguintes certificações:

- Certified Kubernetes Administrator (CKA)
- Certified Kubernetes Application Developer (CKAD)
- Certified Kubernetes Security Specialist (CKS)
- Kubernetes and Cloud Native Associate (KCNA)
- Kubernetes and Cloud Native Security Associate (KCSA)

## 📚 Conteúdo

O material está organizado nas seguintes seções principais:

- Fundamentos do Kubernetes
- Componentes do Cluster
- Objetos da API
- Workloads
- Configuração
- Redes
- Segurança
- Operações
- Observabilidade
- Ferramentas

## 🚀 Como Usar

Este material está estruturado como um livro digital usando [mdBook](https://github.com/rust-lang/mdBook). Para visualizar localmente:

### Instalação

```bash
# Instale o Rust (se ainda não tiver)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Instale o mdBook e plugins
cargo install mdbook
cargo install mdbook-admonish
cargo install mdbook-plantuml

# Configure o mdbook-admonish
mdbook-admonish install .
```

### Visualização

```bash
# Clone este repositório
git clone https://github.com/fabioluciano/kubestronaut.git
cd kubestronaut

# Execute o servidor local
mdbook serve

# Acesse http://localhost:3000
```

### Build

```bash
# Gera os arquivos HTML estáticos
mdbook build

# Os arquivos estarão em ./book/
```

## 🤝 Contribuições

Contribuições são bem-vindas! Se você encontrar erros, quiser melhorar o conteúdo ou adicionar novos tópicos:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/NovaSecao`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona nova seção sobre X'`)
4. Push para a branch (`git push origin feature/NovaSecao`)
5. Abra um Pull Request

## ✨ Agradecimentos

Este projeto é mantido pela comunidade para a comunidade. Agradecemos a todos os contribuidores que ajudam a manter este recurso atualizado e relevante.
