# CLAUDE.md - Contexto do Projeto Kubestronaut

> Este arquivo contém o contexto necessário para continuar o trabalho de melhoria do guia Kubestronaut.

## 🎯 Objetivo do Projeto

Transformar este material em um **guia completo em português** para passar em **TODAS** as certificações Kubernetes:
- **KCNA** - Kubernetes and Cloud Native Associate
- **KCSA** - Kubernetes and Cloud Native Security Associate  
- **CKAD** - Certified Kubernetes Application Developer
- **CKA** - Certified Kubernetes Administrator
- **CKS** - Certified Kubernetes Security Specialist

## 📊 Status Atual (Janeiro 2026) - ATUALIZADO

### Cobertura por Certificação

| Certificação | Cobertura | Status |
|--------------|-----------|--------|
| KCNA | 90% | cloud-native.md + kcna.md completos |
| KCSA | 90% | kcsa.md + threat-model + compliance |
| CKAD | 90% | ckad.md + workloads completos |
| CKA | 90% | cka.md + troubleshooting + operações |
| CKS | 90% | cks.md + segurança completa |

### Arquivos Verificados
- **Total**: 93 arquivos .md
- **Completos**: 80+ arquivos
- **Build**: Funcionando (95 páginas HTML)
- **Links**: Todos válidos

## ✅ Trabalho Concluído

### Migração Obsidian → mdBook
- [x] Convertidos ~81 wikilinks para markdown padrão
- [x] Convertidos ~50+ callouts para admonish blocks
- [x] Corrigidos ~20+ reference blocks
- [x] Criados scripts de migração (migrate_obsidian_to_mdbook.py, fix_admonish.py, fix_final.py)

- [x] TEMPLATE_ARQUIVO.md - Template padrão para arquivos

### Arquivos Expandidos
- [x] src/crictl.md - Expandido de 1 comando para guia completo

## ✅ Arquivos Críticos - COMPLETOS

| Arquivo | Linhas | Status |
|---------|--------|--------|
| tools/kubeadm.md | 300 | ✅ Completo |
| security/etcdctl.md | 286 | ✅ Completo |
| security/mtls.md | 200 | ✅ Completo |
| security/minimizar-acesso-gui.md | 267 | ✅ Completo |
| tools/kustomize.md | 193 | ✅ Completo |
| maintenance/troubleshooting.md | 417 | ✅ Completo |
| observability/monitoring.md | 276 | ✅ Completo |
| observability/observabilidade.md | 416 | ✅ Completo |
| certifications/kcna.md | 642 | ✅ Completo |
| workloads/horizontal-pod-autoscaler.md | 317 | ✅ Completo |
| tools/helm.md | 300+ | ✅ Completo |
| docker.md | 520 | ✅ Completo |
| high-availability.md | 350+ | ✅ Completo |
| networking/ingress.md | 232 | ✅ Completo |

## ✅ Arquivos Criados para Certificações

| Arquivo | Linhas | Certificação |
|---------|--------|--------------|
| cloud-native.md | 450+ | KCNA (16%) |
| certifications/kcna.md | 640+ | KCNA |
| certifications/kcsa.md | 500+ | KCSA |
| certifications/ckad.md | 550+ | CKAD |
| certifications/cka.md | 600+ | CKA |
| certifications/cks.md | 650+ | CKS |
| security/threat-model.md | 400+ | KCSA (16%) |
| security/compliance.md | 450+ | KCSA (10%) |

## 📋 Plano de Fases

### Fase 1 - Gaps Críticos ✅ CONCLUÍDA
Todos os 15 arquivos críticos estão completos.

### Fase 2 - Consolidação ✅ CONCLUÍDA
- Adicionar seção Troubleshooting em todos arquivos
- Expandir nodes-components/
- Garantir 3+ exemplos práticos por arquivo

### Fase 3 - Reorganização ✅ CONCLUÍDA
- SUMMARY.md atualizado com nova estrutura
- Diretórios reorganizados (workloads/, networking/, cluster-components/, etc.)
- Links internos corrigidos

### Fase 4 - Excelência ✅ CONCLUÍDA
- 335 diagramas PlantUML
- Tema Kubestronaut criado
- Build funcionando

## 📝 Template Padrão para Arquivos

Usar o template em `TEMPLATE_ARQUIVO.md`. Estrutura mínima:

```markdown
---
certifications: [CKA, CKAD]
exam_weight: 15%
difficulty: intermediate
---

# Título

> **Certificações**: CKA (X%), CKAD (Y%)

## 📖 Conceitos
## 🎯 Casos de Uso  
## 💻 Exemplos Práticos
## 🔧 Comandos Úteis
## 🐛 Troubleshooting
## 🎓 Dicas para o Exame
## 📚 Best Practices
## 🔗 Referências
## ✅ Checklist
```

## 🛠️ Como Continuar

### Próximos Passos Imediatos

1. **Expandir kubeadm.md** - Arquivo crítico para CKA
   - Adicionar kubeadm init com todas flags
   - kubeadm join (control plane e worker)
   - kubeadm upgrade workflow completo
   - Troubleshooting

2. **Expandir ETCDCTL.md** - Crítico para backup/restore
   - Comandos de backup e restore
   - Verificação de health
   - Variáveis de ambiente necessárias

3. **Expandir Troubleshooting.md** - 30% da prova CKA!
   - Application troubleshooting
   - Control plane troubleshooting
   - Worker node troubleshooting
   - Network troubleshooting

### Comando para Ver Progresso

```bash
# Ver arquivos por tamanho (identificar vazios)
find src -name "*.md" -exec wc -l {} \; | sort -n

# Ver arquivos modificados recentemente
ls -lt src/*.md | head -20
```

## 📁 Estrutura do Projeto

```
kubestronaut/
├── book.toml              # Config do mdBook
├── CLAUDE.md              # Este arquivo (contexto)
├── PLANO_CORRECOES.md     # Plano detalhado
├── TEMPLATE_ARQUIVO.md    # Template padrão
├── MIGRATION.md           # Doc da migração
├── src/
│   ├── SUMMARY.md         # Índice do livro
│   ├── index.md           # Página inicial
│   ├── *.md               # Arquivos de conteúdo
│   ├── Security/          # 28 arquivos de segurança (CKS/KCSA)
│   ├── maintenance/       # 5 arquivos de operações (CKA)
│   ├── network/           # Arquivos de rede
│   ├── nodes-components/  # Componentes do cluster
│   ├── workload/          # Pod, Deployment, ReplicaSet
│   └── assets/            # Exemplos YAML
```

## 🔗 Arquivos de Referência

- **PLANO_CORRECOES.md** - Plano completo com todas as fases e ações
- **TEMPLATE_ARQUIVO.md** - Template para criar/expandir arquivos
- **src/Apresentação.md** - Links para currículos oficiais das certificações

## ⚠️ Notas Importantes

1. **Não usar rodapé** com "Status: Completo" - O terminal travou com isso
2. **Manter linguagem em português** - Guia é para audiência brasileira
3. **Testar YAMLs** - Todos exemplos devem funcionar
4. **Seguir template** - Consistência é importante
5. **NÃO USAR HEREDOC** - Trava o terminal do usuário
6. **Para criar arquivos**: Usar ferramenta `create_file` do Copilot (deletar arquivo antes se existir com `rm`)
7. **Referenciar outros arquivos** - Sempre que possível linkar arquivos relacionados

## 📞 Contexto da Conversa Anterior

- Usuário: Fabio Luciano
- Projeto nasceu no Obsidian, migrado para mdBook
- Objetivo: Ser Kubestronaut (todas 5 certificações)
- Análise completa de 86 arquivos foi feita
- crictl.md AINDA NÃO foi expandido (heredoc falhou)

