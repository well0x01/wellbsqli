# Time-based Blind SQL Injection Script - WELLBSQLI

## Descrição

  Este script Python é projetado para realizar injeções SQL baseadas em tempo (time-based blind SQL injection) em URLs. Ele envia uma lista de payloads para diferentes         parâmetros de URL, paths, e cabeçalhos HTTP para verificar possíveis vulnerabilidades de injeção SQL. 

## Funcionalidades

- **Injeção em Parâmetros de URL**: Injeta payloads nos parâmetros de consulta da URL.
- **Injeção em Paths**: Adiciona payloads ao caminho da URL.
- **Injeção em Cabeçalhos HTTP**: Adiciona payloads aos cabeçalhos `User-Agent`, `Referer`, e `Cookie`.
- **Suporte a Proxies**: Permite o uso de um proxy HTTP para direcionar as solicitações.
- **Relatório de Resultados**: Salva resultados de sucesso em um arquivo de saída.
- **Verificação de Certificado SSL Desativada**: Ignora a verificação de certificado SSL para evitar erros de conexão.

## Instalação

1. **Clone o repositório** (ou faça o download do script):
   
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <DIRETORIO_DO_REPOSITORIO>

2. **Instale as dependências** :

  É recomendado criar um ambiente virtual para instalar as dependências.

  ```bash
  python -m venv venv
  source venv/bin/activate  # Para Linux/Mac
  venv\Scripts\activate     # Para Windows
  pip install <PACOTES>
  ```

## Uso

  ```bash
  python wellbsqli.py -u <URL> -p <CAMINHO_PARA_PAYLOADS> [-o <CAMINHO_PARA_SAIDA>] [-s <PROXY_HTTP>]
  ```

### Opções:

  * -u, --url: URL da API que será testada.
  * -l, --list: Arquivo contendo uma lista de URLs para testar.
  * -p, --payload-file: Arquivo contendo a lista de payloads para testar (obrigatório).
  * -o, --output: Arquivo para salvar os resultados de sucesso.
  * -s, --server-http: Proxy HTTP para direcionar as solicitações (ex: http://127.0.0.1:8080).
  * -h, --help: Mostrar o banner e as opções disponíveis.

## Contribuições:
  Sinta-se à vontade para contribuir com melhorias ou correções. Envie um pull request ou abra um issue para discussões.

## Autor:
  Desenvolvido por @well0x01







