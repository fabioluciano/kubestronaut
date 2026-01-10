.PHONY: setup build serve clean help lint lint-md lint-plantuml lint-yaml lint-links validate test

# Cores para output
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m # No Color

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# =============================================================================
# SETUP
# =============================================================================

setup: ## Instala todas as dependências
	@echo "$(GREEN)==> Verificando dependências...$(NC)"
	@command -v mise >/dev/null 2>&1 || { echo "$(RED)Erro: mise não está instalado. Instale em https://mise.jdx.dev$(NC)"; exit 1; }
	@command -v cargo >/dev/null 2>&1 || { echo "$(RED)Erro: cargo/rust não está instalado. Instale em https://rustup.rs$(NC)"; exit 1; }
	@command -v node >/dev/null 2>&1 || { echo "$(YELLOW)Aviso: node não está instalado. Alguns linters não funcionarão.$(NC)"; }
	@command -v plantuml >/dev/null 2>&1 || { echo "$(YELLOW)Aviso: plantuml não está instalado. Diagramas não serão gerados.$(NC)"; }
	@echo "$(GREEN)==> Instalando ferramentas via mise...$(NC)"
	@mise trust 2>/dev/null || true
	@mise install
	@echo "$(GREEN)==> Instalando mdbook-plantuml...$(NC)"
	@cargo install mdbook-plantuml --git https://github.com/sytsereitsma/mdbook-plantuml --tag v1.0.0-rc.1 2>/dev/null || true
	@echo "$(GREEN)==> Instalando ferramentas de lint...$(NC)"
	@npm install --silent 2>/dev/null || true
	@echo "$(GREEN)==> Setup completo!$(NC)"

install: setup ## Alias para setup

# =============================================================================
# BUILD
# =============================================================================

build: ## Compila o livro
	@echo "$(GREEN)==> Compilando o livro...$(NC)"
	@mise exec -- mdbook build
	@echo "$(GREEN)==> Livro gerado em ./book/$(NC)"

serve: ## Inicia servidor local com live-reload
	@echo "$(GREEN)==> Iniciando servidor em http://localhost:3000$(NC)"
	@mise exec -- mdbook serve --open

clean: ## Remove arquivos gerados
	@echo "$(GREEN)==> Limpando...$(NC)"
	@rm -rf book/
	@rm -rf .mdbook-plantuml-cache/
	@rm -rf node_modules/
	@echo "$(GREEN)==> Limpo!$(NC)"

# =============================================================================
# LINTING
# =============================================================================

lint: lint-md lint-plantuml lint-yaml lint-links ## Executa todos os linters

lint-md: ## Valida arquivos Markdown
	@echo "$(GREEN)==> Validando Markdown...$(NC)"
	@if command -v npx >/dev/null 2>&1; then \
		npx markdownlint-cli2 "src/**/*.md" --config .markdownlint.json 2>/dev/null || \
		echo "$(YELLOW)Aviso: markdownlint não instalado. Execute 'npm install'.$(NC)"; \
	else \
		echo "$(YELLOW)Aviso: npx não encontrado. Instale Node.js para lint de markdown.$(NC)"; \
	fi

lint-plantuml: ## Valida diagramas PlantUML
	@echo "$(GREEN)==> Validando PlantUML...$(NC)"
	@if command -v plantuml >/dev/null 2>&1; then \
		mkdir -p .plantuml-check; \
		error_count=0; \
		for file in $$(grep -rl '@startuml' src/ 2>/dev/null); do \
			echo "  Verificando $$file..."; \
			grep -Pzo '```plantuml[^\n]*\n\K[\s\S]*?(?=```)' "$$file" 2>/dev/null | \
			while IFS= read -r -d '' block; do \
				echo "$$block" > .plantuml-check/temp.puml; \
				if ! plantuml -syntax .plantuml-check/temp.puml > /dev/null 2>&1; then \
					echo "$(RED)    Erro de sintaxe PlantUML em $$file$(NC)"; \
					error_count=$$((error_count + 1)); \
				fi; \
			done; \
		done; \
		rm -rf .plantuml-check; \
		if [ $$error_count -gt 0 ]; then exit 1; fi; \
	else \
		echo "$(YELLOW)Aviso: plantuml não instalado. Pulando validação.$(NC)"; \
	fi

lint-yaml: ## Valida arquivos YAML
	@echo "$(GREEN)==> Validando YAML...$(NC)"
	@error_count=0; \
	for file in $$(find src/assets -name "*.yaml" -o -name "*.yml" 2>/dev/null); do \
		if ! python3 -c "import yaml; yaml.safe_load(open('$$file'))" 2>/dev/null; then \
			echo "$(RED)  Erro de sintaxe YAML: $$file$(NC)"; \
			error_count=$$((error_count + 1)); \
		fi; \
	done; \
	if [ $$error_count -gt 0 ]; then \
		echo "$(RED)Encontrados $$error_count erros de YAML$(NC)"; \
		exit 1; \
	else \
		echo "$(GREEN)  Todos os arquivos YAML são válidos$(NC)"; \
	fi

lint-links: ## Verifica links quebrados entre documentos
	@echo "$(GREEN)==> Verificando links...$(NC)"
	@error_count=0; \
	for file in $$(find src -name "*.md" 2>/dev/null); do \
		dir=$$(dirname "$$file"); \
		grep -oE '\[([^\]]+)\]\(([^)]+\.md[^)]*)\)' "$$file" 2>/dev/null | \
		sed 's/.*](\([^)]*\)).*/\1/' | \
		sed 's/#.*//' | \
		while read -r link; do \
			if [ -n "$$link" ]; then \
				if echo "$$link" | grep -q "^/"; then \
					target="src$$link"; \
				elif echo "$$link" | grep -q "^http"; then \
					continue; \
				else \
					target="$$dir/$$link"; \
				fi; \
				target=$$(echo "$$target" | sed 's|/\./|/|g'); \
				if [ ! -f "$$target" ]; then \
					echo "$(RED)  Link quebrado em $$file: $$link$(NC)"; \
					error_count=$$((error_count + 1)); \
				fi; \
			fi; \
		done; \
	done; \
	if [ $$error_count -gt 0 ]; then \
		echo "$(RED)Encontrados links quebrados$(NC)"; \
	else \
		echo "$(GREEN)  Todos os links são válidos$(NC)"; \
	fi

# =============================================================================
# VALIDAÇÃO E TESTE
# =============================================================================

validate: lint build ## Executa validação completa (lint + build)
	@echo "$(GREEN)==> Validação completa!$(NC)"

test: ## Testa o livro (mdbook test)
	@echo "$(GREEN)==> Testando...$(NC)"
	@mise exec -- mdbook test

# =============================================================================
# CI/CD HELPERS
# =============================================================================

ci-setup: ## Setup para CI (GitHub Actions)
	@echo "$(GREEN)==> Setup CI...$(NC)"
	@mise install
	@cargo install mdbook-plantuml --git https://github.com/sytsereitsma/mdbook-plantuml --tag v1.0.0-rc.1
	@npm ci --silent 2>/dev/null || npm install --silent

ci-lint: lint-md lint-yaml lint-links ## Lint para CI (sem plantuml pois é lento)
	@echo "$(GREEN)==> CI Lint completo$(NC)"

ci-build: ## Build para CI
	@mise exec -- mdbook build
