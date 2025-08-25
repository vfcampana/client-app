# Integração Blockchain - Guia Completo

Este documento explica como a integração blockchain foi implementada na aplicação usando o SCManager.

## 📋 Visão Geral

A integração blockchain permite:
- Registro automático de usuários na blockchain Ethereum
- Registro de blocos ornamentais como NFTs
- Transferência segura de propriedade durante vendas
- Rastreamento transparente de transações
- Funcionamento offline (fallback para sistema local)

## 🚀 Configuração Inicial

### 1. Pré-requisitos

Certifique-se de ter as seguintes variáveis no arquivo `.env`:

```properties
# Configurações blockchain
ETHEREUM_PRIVATE_KEY='0xsua_chave_privada_aqui'
ETHEREUM_ENDPOINT='https://mainnet.infura.io/v3/seu_projeto_id'

# Configurações do banco
DATABASE_URL="postgresql://user:pass@host:port/db"
```

### 2. Instalação das Dependências

```bash
# Ativar ambiente virtual
cd c:\Users\Enzo\Documents\GitHub\client-app
.\blockchaind\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Instalar SCManager
pip install -e "c:\Users\Enzo\Downloads\SCManager-master\SCManager-master"
```

### 3. Configuração Inicial da Blockchain

```bash
# Executar script de configuração
python blockapi\blockchain\setup.py
```

## 🏗️ Arquitetura

### Estrutura de Arquivos

```
blockapi/
├── blockchain/
│   ├── __init__.py
│   ├── blockchain_manager.py    # Gerenciador principal da blockchain
│   ├── chat_service.py         # Integração com sistema de chat
│   ├── setup.py               # Script de configuração inicial
│   └── exemplo_uso.py         # Documentação e exemplos
├── api/
│   └── resources/
│       └── blockchain.py      # Endpoints da API blockchain
└── models/
    ├── usuario.py            # Modelo atualizado com blockchain_uid
    └── mensagem.py          # Modelo atualizado com metadata
```

### Componentes Principais

1. **BlockchainManager**: Gerencia todas as operações blockchain
2. **BlockchainChatService**: Integra blockchain com sistema de chat
3. **API Resources**: Endpoints REST para operações blockchain
4. **Models**: Modelos de dados atualizados para suportar blockchain

## 🔧 Como Usar

### 1. Verificar Status da Blockchain

```http
GET /api/blockchain/status
```

```json
{
    "connected": true,
    "account_balance": 0.5,
    "total_users": 10,
    "total_blocks": 25,
    "message": "Blockchain conectado e funcionando"
}
```

### 2. Registrar Usuário (Automático)

Os usuários são registrados automaticamente durante a primeira venda.

```http
POST /api/blockchain/user/register
Authorization: Bearer <jwt_token>
```

### 3. Criar Proposta de Venda

```http
POST /api/blockchain/sale/proposal
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "conversa_id": 5,
    "bloco_id": 12,
    "preco": 1500.00
}
```

### 4. Aceitar Proposta (Automático)

Quando um usuário escreve "ACEITO" no chat, o sistema:
- Registra usuários na blockchain (se necessário)
- Registra o bloco na blockchain (se necessário)  
- Transfere propriedade
- Cria confirmação no chat

## 💬 Integração com Chat

### Mensagens Automáticas

O sistema cria mensagens automáticas no chat:

#### Proposta de Venda
```
💰 PROPOSTA DE VENDA
Bloco: Bloco Ornamental ABC
Material: Granito
Dimensões: 50x30x20
Preço: R$ 1500.00

🔗 Vendedor registrado na blockchain

Para aceitar, responda 'ACEITO'
```

#### Confirmação Blockchain
```
🔗 TRANSAÇÃO BLOCKCHAIN CONFIRMADA
Bloco: Bloco Ornamental ABC
Vendedor: João Silva
Comprador: Maria Santos
Preço: R$ 1500.00
Hash: 0x123456789abcdef...
```

#### Modo Offline
```
⚠️ AVISO: Venda processada localmente
Erro blockchain: Rede indisponível
A venda foi registrada no sistema local.
```

### Palavras-chave de Aceitação

O sistema reconhece as seguintes palavras para aceitar propostas:
- ACEITO
- ACEITAR
- OK
- SIM
- CONFIRMADO

## 🛡️ Tratamento de Erros

### Cenários Suportados

1. **Blockchain Offline**: Vendas continuam funcionando localmente
2. **Saldo Insuficiente**: Erro é reportado, venda cancelada
3. **Rede Congestionada**: Sistema aguarda e tenta novamente
4. **Usuário Não Registrado**: Registro automático durante transação

### Logs

Todos os eventos blockchain são logados:

```python
import logging
logger = logging.getLogger(__name__)

# Configurar logs para ver atividade blockchain
logging.basicConfig(level=logging.INFO)
```

## 📊 Monitoramento

### Verificar Status dos Usuários

```http
GET /api/blockchain/user/check
Authorization: Bearer <jwt_token>
```

### Verificar Preparação para Transação

```http
POST /api/blockchain/transfer/check
Content-Type: application/json

{
    "vendedor_id": 123,
    "comprador_id": 456
}
```

## 🔄 Fluxo Completo de Venda

1. **Usuário A** quer vender bloco para **Usuário B**
2. **A** cria proposta no chat (via API ou interface)
3. Sistema verifica blockchain e cria mensagem de proposta
4. **B** vê proposta e responde "ACEITO"
5. Sistema automaticamente:
   - Registra A na blockchain (se necessário)
   - Registra B na blockchain (se necessário)
   - Registra bloco na blockchain (se necessário)
   - Transfere propriedade do bloco
   - Cria mensagem de confirmação
6. Ambos usuários veem confirmação da transação

## 🧪 Testes

### Executar Configuração de Teste

```bash
python blockapi\blockchain\setup.py
```

### Testar via API

```bash
# Verificar status
curl http://localhost:5000/api/blockchain/status

# Registrar usuário (com token JWT)
curl -X POST http://localhost:5000/api/blockchain/user/register \
  -H "Authorization: Bearer <token>"

# Criar proposta
curl -X POST http://localhost:5000/api/blockchain/sale/proposal \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"conversa_id":1,"bloco_id":1,"preco":1000.00}'
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **"scmanager not found"**
   ```bash
   pip install -e "c:\Users\Enzo\Downloads\SCManager-master\SCManager-master"
   ```

2. **"Blockchain não conectado"**
   - Verificar variáveis de ambiente (.env)
   - Verificar saldo da carteira
   - Verificar endpoint Infura

3. **"Microsoft Visual C++ required"**
   - Instalar Visual Studio Build Tools
   - Ou usar versão pré-compilada do lru-dict

4. **"Transaction failed"**
   - Verificar saldo ETH para gas
   - Verificar congestionamento da rede
   - Verificar se endpoint está funcionando

### Debug

```python
# Ativar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)

# Verificar status da blockchain
from blockchain.blockchain_manager import blockchain_manager
status = blockchain_manager.get_blockchain_status()
print(status)
```

## 📈 Próximos Passos

1. **Interface Frontend**: Implementar UI para status blockchain
2. **Notificações**: Alertas em tempo real para transações
3. **Histórico**: Página para visualizar transações blockchain
4. **Analytics**: Dashboard com métricas blockchain
5. **Multi-chain**: Suporte para outras redes (Polygon, BSC)

## 🤝 Contribuição

Para contribuir com melhorias na integração blockchain:

1. Fork o projeto
2. Crie branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Abra Pull Request

## 📞 Suporte

Para questões técnicas sobre blockchain:
- Consulte a documentação do SCManager
- Verifique logs da aplicação
- Teste em rede de desenvolvimento primeiro

---

**Nota**: Esta integração foi projetada para ser robusta e funcionar mesmo quando a blockchain está indisponível, garantindo que o sistema principal continue operacional.
