## Falco

- Usado para monitorar atividades suspeitas nos containers.
- Observa quais são as system calls que estão sendo invocadas no user usepace
- Usa um módulo do falco para ficar em frente ao kernel e capturar a syscalls
`
```shell
journalctl -fu falco
```

- um arquivo rule do falco pode possuir tres tipos de elementos: rules, lists e macros
- o arquivo de configuração padrão do falco está localizado em `/etc/falco/falco.yaml`
- regras são carregadas usando a opção `rules_file` no arquivo de configuração
- 
### rules
- rule: nome da rule
- desc: descrição da rule
- condition: quando o evento será disparado.
- output: Saida a ser gerada pelo evento
- priority: severidade do evento

- as variáveis definidas no conditions e output, são fornecidas pelo sysdig
- macros são reduções de variaveis... por exemplo `container.id`pode ser referenciado apenas como `container


