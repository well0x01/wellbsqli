# Time-based Blind SQL Injection Script

## Descrição

Este script foi criado para testar vulnerabilidades de injeção SQL baseada em tempo (Time-based Blind SQL Injection) em aplicações web. Ele realiza solicitações HTTP com payloads que causam atrasos na resposta quando uma vulnerabilidade está presente.

## Funcionalidades

- Testa URLs individuais ou a partir de uma lista de URLs.
- Injeção de payloads em diferentes partes da solicitação: cabeçalhos, parâmetros de consulta, caminho da URL e corpo de dados (para solicitações POST).
- Suporte para proxies HTTP.
- Testes multi-thread para melhorar a eficiência.
- Suporte para diferentes métodos de codificação de payloads.
- Gera relatórios de vulnerabilidades encontradas.
- Suporte para testes POST por meio de um arquivo 'request.txt'
- Exibe a versão atual do script.

## Uso
### Opções

  * -u, --url: URL que será testada.
  * -l, --list: Arquivo contendo uma lista de URLs para testar.
  * -p, --payload-file: Arquivo contendo a lista de payloads para testar.
  * -o, --output: Arquivo para salvar os resultados de sucesso.
  * -s, --server-http: Proxy HTTP para direcionar as solicitações (ex: http://127.0.0.1:8080).
  * -t, --threads: Número de threads para realizar as requisições (padrão: 2).
  * -r, --requests: Arquivo contendo uma requisição HTTP para testar.
  * -v, --version: Exibe a versão atual do script.
  * -h, --help: Mostra o banner e as opções disponíveis.

## Exemplos

  1. Testar uma url : ```python wellbsqli.py -u http://example.com/vulnerable_endpoint -p payloads.txt -o resultados.txt```
  2. Testar uma lista de urls: ```python wellbsqli.py -l urls.txt -p payloads.txt -o resultados.txt```
  3. Testar uma requisição HTTP específica a partir de um arquivo: ```python wellbsqli.py -r request.txt -p payloads.txt -o resultados.txt```

## Changelog
### Versão 1.0.1

  * Lançamento inicial do script.
  * Suporte para injeção de payloads em cabeçalhos, parâmetros de consulta, caminho da URL e corpo de dados.
  * Adição de diferentes métodos de codificação de payloads.
  * Suporte para proxy HTTP.
  * Testes multi-thread.
  * Geração de relatórios de vulnerabilidades.
  * Adição da opção para exibir a versão do script.



