# sitema_gestao_leo

Antonio Vinicius Oni Sousa Silva (RM: 560235) 
Guilherme Terzi Gonzalez (RM: 560175) 
Gustavo Gimenez Gozzi (RM: 560053) 
Matheus Barbosa da Silva (RM: 561085) 
Moacyr Cabral da Silva (RM: 559263)

Vai no meu github leo: https://github.com/ViniciusOnii/

# Sistema de Gestão de Estoque

Um sistema completo de gestão de estoque desenvolvido em Python com interface gráfica Tkinter e banco de dados MongoDB.

## 🚀 Funcionalidades

### 1. Gestão de Funcionários
- Cadastro e gerenciamento de funcionários
- Controle de acesso e permissões
- Histórico de atividades

### 2. Gestão de Fornecedores
- Cadastro de fornecedores
- Histórico de compras
- Controle de contatos

### 3. Gestão de Categorias
- Organização de produtos por categorias
- Filtros e busca por categorias

### 4. Gestão de Produtos
- Cadastro completo de produtos
- Controle de estoque
- Alertas de estoque baixo
- Histórico de movimentações

### 5. Sistema de Vendas
- PDV (Ponto de Venda)
- Geração de notas fiscais
- Histórico de vendas
- Relatórios de vendas

### 6. Gestão Financeira
- Controle de receitas e despesas
- Relatórios financeiros
- Fluxo de caixa
- Análise de lucratividade

### 7. Programa de Fidelidade
- Cadastro de clientes
- Sistema de pontos
- Níveis de fidelidade (Bronze, Prata, Ouro)
- Histórico de pontos

### 8. Dashboard Avançado
- KPIs em tempo real
- Gráficos de vendas
- Previsão de demanda
- Alertas em tempo real

### 9. Análise Avançada
- Análise de tendências
- Relatórios personalizados
- Métricas de desempenho

### 10. Sistema de Suporte
- Abertura de tickets
- Acompanhamento de chamados
- Histórico de atendimentos

## 📋 Pré-requisitos

- Python 3.8 ou superior
- MongoDB 4.4 ou superior
- Bibliotecas Python (listadas em requirements.txt)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/ViniciusOnii/sistema_gestao.git
cd gerenciamento_estoque_2
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Certifique-se que o MongoDB está instalado e rodando:
```bash
mongod
```

4. Execute o sistema:
```bash
python dashboard.py
```

## 🔑 Credenciais de Acesso

- Usuário: Leo
- Senha: 123

## 📁 Estrutura do Projeto

```
gerenciamento_estoque_2/
├── dashboard.py              # Interface principal
├── employee.py              # Gestão de funcionários
├── supplier.py              # Gestão de fornecedores
├── category.py              # Gestão de categorias
├── products.py              # Gestão de produtos
├── sales.py                 # Sistema de vendas
├── billing.py               # PDV e notas fiscais
├── financeiro.py            # Gestão financeira
├── fidelidade.py            # Programa de fidelidade
├── dashboard_avancado.py    # Dashboard com KPIs
├── analise_avancada.py      # Análise avançada
├── suporte.py               # Sistema de suporte
├── images/                  # Imagens do sistema
├── bill/                    # Notas fiscais geradas
└── requirements.txt         # Dependências do projeto
```

## 💾 Banco de Dados

O sistema utiliza MongoDB com as seguintes coleções:
- usuarios
- funcionarios
- fornecedores
- categorias
- produtos
- vendas
- clientes
- tickets
- financeiro

## 🔒 Segurança

- Sistema de login com autenticação
- Controle de acesso por nível de usuário
- Backup automático do banco de dados
- Registro de atividades dos usuários

## 📊 Relatórios

O sistema gera diversos tipos de relatórios:
- Relatório de vendas
- Relatório de estoque
- Relatório financeiro
- Relatório de clientes
- Relatório de funcionários


Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

# Sistema de Gestão de Vendas - Documentação

## Visão Geral
Este projeto implementa um sistema de gestão de vendas utilizando Python e MongoDB, focando no gerenciamento eficiente de produtos, categorias, fornecedores, funcionários, vendas e faturamento. A interface gráfica é construída com `tkinter`, utilizando também as bibliotecas `pymongo` para comunicação com o banco de dados e `PIL` (Pillow) para manipulação de imagens.

## Estrutura do Projeto
O projeto é organizado da seguinte forma:

- **bill/**: Armazena faturas geradas durante as vendas.
- **images/**: Contém imagens usadas na interface gráfica.
- **billing.py**: Gerencia o faturamento e cria relatórios financeiros.
- **category.py**: Criação e edição de categorias de produtos.
- **create_db.py**: Inicializa o banco de dados MongoDB.
- **dashboard.py**: Interface para análise de dados de vendas.
- **employee.py**: Cadastro e gerenciamento de funcionários.
- **products.py**: Cadastro e controle de produtos.
- **sales.py**: Registro de vendas com integração ao faturamento.
- **supplier.py**: Gerenciamento de fornecedores e atualização de estoque.

## Funcionalidades Principais
- Cadastro e gerenciamento de produtos, categorias, fornecedores e funcionários.
- Registro de vendas e emissão de faturas.
- Visualização de dashboards analíticos.
- Criação automatizada e configuração do banco de dados MongoDB.
- Interface gráfica amigável construída com `tkinter`.

## Requisitos para Execução
1. **Instalação do Python:** Certifique-se de ter o Python 3.x instalado no seu sistema. Caso não tenha, baixe em [python.org](https://www.python.org/downloads/).

2. **Instalação do MongoDB:** Baixe e instale o MongoDB Community Server em [mongodb.com](https://www.mongodb.com/try/download/community). Certifique-se de iniciar o serviço MongoDB.

## Configuração de Login e Senha
- Para acessar a área do dashboard, é necessário realizar login.
- As credenciais padrão configuradas são:
  - **Usuário:** Leo
  - **Senha:** 123
- Caso deseje alterar o login e senha, abra o código no módulo de autenticação e ajuste as variáveis correspondentes.




##Partes do Projeto:
##Dashboard.py
![image](https://github.com/user-attachments/assets/d17f8727-facc-470a-84e3-13ab7c8fa63e)
![image](https://github.com/user-attachments/assets/8fb418e4-c544-4d89-bc38-c300502da849)

Parte Principal do Sistema onde você vai conseguir acessar as outras abas

##Employee.py
![image](https://github.com/user-attachments/assets/a32f3165-a99b-491e-a1d4-4fb821696cba)
Onde você irá cadastrar os dados do cliente ou funcionario cadastrando suas informações


##Suplier.py
![image](https://github.com/user-attachments/assets/a4a1bbb3-81e8-433c-b578-ed14d04fd4eb)
Onde você ira cadastrar os fornecedores 


#Cateogry.py
![image](https://github.com/user-attachments/assets/4dbfa2b6-7c1c-4f8f-a993-267b0386f256)
Onde irá colocar as categorias do seu produto ou qualquer coisa do tipo.

##Products.py
![image](https://github.com/user-attachments/assets/ca768dc7-235b-4f91-a45d-a08a58e07253)
#Onde irá adicionar seus produtos ao banco de dados para vender

##Billing.py
![image](https://github.com/user-attachments/assets/f0c2d548-b824-4745-85ce-aeff419731f0)
Onde você ira adicionar os produtos que você quer comprar, que está no banco de dados.

##Sales.py
![image](https://github.com/user-attachments/assets/c9fd4428-da1a-43c3-af2a-f1d29b52b3c5)
#Onde você irá ver as vendas




