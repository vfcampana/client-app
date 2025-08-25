"""
Exemplo de uso da integração blockchain no sistema de chat
"""

# Como usar a integração blockchain no seu sistema:

# 1. VERIFICAR STATUS DA BLOCKCHAIN
# GET /api/blockchain/status
"""
Retorna:
{
    "connected": true,
    "account_balance": 0.5,
    "total_users": 10,
    "total_blocks": 25,
    "last_update": "2025-01-15T10:30:00Z",
    "message": "Blockchain conectado e funcionando"
}
"""

# 2. REGISTRAR USUÁRIO NA BLOCKCHAIN (automático durante primeira venda)
# POST /api/blockchain/user/register
"""
Headers: { "Authorization": "Bearer <jwt_token>" }
Retorna:
{
    "success": true,
    "message": "Usuário registrado na blockchain com sucesso",
    "transaction_hash": "0x123...",
    "user_uid": "0xabc...",
    "already_registered": false
}
"""

# 3. VERIFICAR SE USUÁRIO ESTÁ REGISTRADO
# GET /api/blockchain/user/check
"""
Headers: { "Authorization": "Bearer <jwt_token>" }
Retorna:
{
    "success": true,
    "user_id": 123,
    "registered_on_blockchain": true,
    "blockchain_connected": true
}
"""

# 4. CRIAR PROPOSTA DE VENDA COM BLOCKCHAIN
# POST /api/blockchain/sale/proposal
"""
Headers: { "Authorization": "Bearer <jwt_token>" }
Body:
{
    "conversa_id": 5,
    "bloco_id": 12,
    "preco": 1500.00
}

Retorna:
{
    "success": true,
    "message": "Proposta de venda criada",
    "mensagem_id": 45
}

Isso criará uma mensagem no chat como:
"💰 PROPOSTA DE VENDA
Bloco: Bloco Ornamental ABC
Material: Granito
Dimensões: 50x30x20
Preço: R$ 1500.00

🔗 Vendedor registrado na blockchain

Para aceitar, responda 'ACEITO'"
"""

# 5. ACEITAR PROPOSTA (AUTOMATICAMENTE PROCESSA BLOCKCHAIN)
# POST /api/blockchain/sale/accept
"""
Headers: { "Authorization": "Bearer <jwt_token>" }
Body:
{
    "conversa_id": 5,
    "mensagem_proposta_id": 45
}

Retorna:
{
    "success": true,
    "message": "Venda processada e registrada na blockchain",
    "blockchain_enabled": true,
    "transaction_hash": "0x456...",
    "block_uid": "0xdef..."
}

Isso automaticamente:
- Registra vendedor na blockchain (se necessário)
- Registra comprador na blockchain (se necessário)
- Registra o bloco na blockchain (se necessário)
- Transfere propriedade do bloco
- Cria mensagem de confirmação no chat
"""

# 6. INTEGRAÇÃO NO FRONTEND

# JavaScript/TypeScript exemplo:

"""
// Verificar status da blockchain
async function checkBlockchainStatus() {
    const response = await fetch('/api/blockchain/status');
    const status = await response.json();
    
    if (status.connected) {
        console.log('Blockchain ativo:', status.message);
        updateBlockchainUI(true, status);
    } else {
        console.log('Blockchain offline:', status.message);
        updateBlockchainUI(false, status);
    }
}

// Criar proposta de venda
async function createSaleProposal(conversaId, blocoId, preco) {
    const token = localStorage.getItem('jwt_token');
    
    const response = await fetch('/api/blockchain/sale/proposal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            conversa_id: conversaId,
            bloco_id: blocoId,
            preco: preco
        })
    });
    
    const result = await response.json();
    
    if (result.success) {
        // Atualizar chat com nova mensagem
        refreshChatMessages();
        showSuccessMessage('Proposta enviada!');
    } else {
        showErrorMessage('Erro ao enviar proposta: ' + result.message);
    }
}

// Aceitar proposta
async function acceptProposal(conversaId, mensagemId) {
    const token = localStorage.getItem('jwt_token');
    
    // Mostrar loading
    showLoadingMessage('Processando transação blockchain...');
    
    const response = await fetch('/api/blockchain/sale/accept', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            conversa_id: conversaId,
            mensagem_proposta_id: mensagemId
        })
    });
    
    const result = await response.json();
    hideLoadingMessage();
    
    if (result.success) {
        if (result.blockchain_enabled) {
            showSuccessMessage('Venda confirmada na blockchain! Hash: ' + result.transaction_hash);
        } else {
            showWarningMessage('Venda processada localmente (blockchain offline)');
        }
        refreshChatMessages();
    } else {
        showErrorMessage('Erro ao processar venda: ' + result.message);
    }
}

// Verificar usuário na blockchain
async function checkUserBlockchain() {
    const token = localStorage.getItem('jwt_token');
    
    const response = await fetch('/api/blockchain/user/check', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const result = await response.json();
    
    if (result.registered_on_blockchain) {
        showBlockchainBadge('Usuário verificado na blockchain');
    } else {
        showBlockchainBadge('Será registrado durante primeira venda');
    }
}
"""

# 7. FLUXO COMPLETO DE UMA VENDA

"""
CENÁRIO: João quer vender um bloco para Maria

1. João acessa a conversa com Maria
2. João clica em "Fazer Proposta" no bloco desejado
3. João define o preço (ex: R$ 1.500,00)
4. Sistema automaticamente:
   - Verifica se blockchain está disponível
   - Verifica se João está registrado na blockchain
   - Cria mensagem de proposta no chat
   
5. Maria vê a proposta no chat:
   "💰 PROPOSTA DE VENDA
    Bloco: Bloco Ornamental XYZ
    Material: Granito
    Dimensões: 50x30x20
    Preço: R$ 1500.00
    🔗 Vendedor registrado na blockchain
    Para aceitar, responda 'ACEITO'"

6. Maria clica em "ACEITO" ou escreve "ACEITO"
7. Sistema automaticamente:
   - Registra Maria na blockchain (se necessário)
   - Registra o bloco na blockchain (se necessário)
   - Transfere propriedade do bloco para Maria
   - Cria mensagem de confirmação:
   
   "🔗 TRANSAÇÃO BLOCKCHAIN CONFIRMADA
    Bloco: Bloco Ornamental XYZ
    Vendedor: João Silva
    Comprador: Maria Santos
    Preço: R$ 1500.00
    Hash: 0x123456789abcdef..."

8. Ambos os usuários veem a confirmação
9. Maria agora é proprietária oficial do bloco na blockchain
"""

# 8. TRATAMENTO DE ERROS

"""
O sistema foi projetado para funcionar mesmo se a blockchain estiver offline:

- Se blockchain offline: vendas são processadas localmente
- Se erro na blockchain: venda continua, mas aviso é exibido
- Se usuário não tem ETH suficiente: erro é reportado
- Se rede está congestionada: sistema tenta novamente

Mensagens de erro típicas:
- "Blockchain não disponível - venda processada localmente"
- "Saldo insuficiente para taxa de transação"
- "Erro de rede - tente novamente em alguns minutos"
"""

print("Documentação de integração blockchain criada!")
print("Consulte este arquivo para entender como usar o sistema.")
