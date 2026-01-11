#!/usr/bin/env python3
from pathlib import Path

src = Path('src')
assets = src / 'assets'

# Coletar todo o conteúdo dos arquivos .md
all_content = ''
for md in src.rglob('*.md'):
    all_content += md.read_text()

# Contar assets
yaml_files = list(assets.rglob('*.yaml')) + list(assets.rglob('*.yml'))
puml_files = list(assets.rglob('*.puml'))

print(f"Total YAML: {len(yaml_files)}")
print(f"Total PUML: {len(puml_files)}")

# Verificar arquivos órfãos
orphans_yaml = []
orphans_puml = []

for f in yaml_files:
    if f.name not in all_content:
        orphans_yaml.append(str(f.relative_to(src)))

for f in puml_files:
    if f.name not in all_content:
        orphans_puml.append(str(f.relative_to(src)))

print(f"\n=== YAML órfãos: {len(orphans_yaml)} ===")
for o in sorted(orphans_yaml):
    print(f"  {o}")

print(f"\n=== PUML órfãos: {len(orphans_puml)} ===")
for o in sorted(orphans_puml):
    print(f"  {o}")

print(f"\n=== TOTAL: {len(orphans_yaml) + len(orphans_puml)} arquivos órfãos ===")
