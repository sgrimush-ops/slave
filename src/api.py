"""
API REST para o sistema de gestão de estoque
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from .modelos import Produto, Loja, CentroDistribuicao, ItemEstoque, TipoMovimentacao, Movimentacao
from .agente_estoque import AgenteEstoque
from .analisador import AnalisadorEstoque
from .gerenciador import GerenciadorEstoque


# Modelos Pydantic para API
class ProdutoCreate(BaseModel):
    id: str
    nome: str
    categoria: str
    unidade: str
    preco_custo: float
    preco_venda: float
    peso: float = 0.0
    volume: float = 0.0
    estoque_minimo: int = 10
    estoque_seguranca: int = 20
    tempo_reposicao_dias: int = 7


class LojaCreate(BaseModel):
    id: str
    nome: str
    endereco: str
    capacidade_m3: float


class TransferenciaRequest(BaseModel):
    produto_id: str
    loja_destino_id: str
    quantidade: int
    observacao: Optional[str] = ""


class ConsultaAgenteRequest(BaseModel):
    pergunta: str
    contexto: Optional[str] = ""


# Inicializa FastAPI
app = FastAPI(
    title="Sistema de Gestão de Estoque com IA",
    description="API para gestão inteligente de estoque usando LLaMA 3",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instâncias globais (em produção, usar banco de dados)
gerenciador = GerenciadorEstoque()
agente = AgenteEstoque()
analisador = AnalisadorEstoque()


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "mensagem": "Sistema de Gestão de Estoque com IA",
        "versao": "1.0.0",
        "modelo_ia": "LLaMA 3"
    }


@app.get("/status")
async def status():
    """Status do sistema"""
    return {
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "lojas": len(gerenciador.lojas),
        "centros_distribuicao": len(gerenciador.centros_distribuicao),
        "produtos_catalogo": len(gerenciador.catalogo_produtos)
    }


# === ENDPOINTS DE PRODUTOS ===

@app.post("/produtos", status_code=201)
async def criar_produto(produto: ProdutoCreate):
    """Criar novo produto no catálogo"""
    try:
        novo_produto = Produto(**produto.dict())
        gerenciador.adicionar_produto_catalogo(novo_produto)
        return {"mensagem": "Produto criado com sucesso", "produto_id": novo_produto.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/produtos")
async def listar_produtos():
    """Listar todos os produtos do catálogo"""
    produtos = [
        {
            "id": p.id,
            "nome": p.nome,
            "categoria": p.categoria,
            "preco_venda": p.preco_venda,
            "estoque_minimo": p.estoque_minimo
        }
        for p in gerenciador.catalogo_produtos.values()
    ]
    return {"total": len(produtos), "produtos": produtos}


@app.get("/produtos/{produto_id}")
async def obter_produto(produto_id: str):
    """Obter detalhes de um produto"""
    produto = gerenciador.catalogo_produtos.get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto.__dict__


# === ENDPOINTS DE LOJAS ===

@app.post("/lojas", status_code=201)
async def criar_loja(loja: LojaCreate):
    """Criar nova loja"""
    try:
        nova_loja = Loja(**loja.dict())
        gerenciador.adicionar_loja(nova_loja)
        return {"mensagem": "Loja criada com sucesso", "loja_id": nova_loja.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/lojas")
async def listar_lojas():
    """Listar todas as lojas"""
    lojas = [
        {
            "id": l.id,
            "nome": l.nome,
            "endereco": l.endereco,
            "produtos_cadastrados": len(l.estoque),
            "produtos_criticos": len(l.listar_produtos_criticos()),
            "ocupacao": round(l.calcular_ocupacao_volume(), 2)
        }
        for l in gerenciador.lojas.values()
    ]
    return {"total": len(lojas), "lojas": lojas}


@app.get("/lojas/{loja_id}")
async def obter_loja(loja_id: str):
    """Obter detalhes de uma loja"""
    loja = gerenciador.lojas.get(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    return {
        "id": loja.id,
        "nome": loja.nome,
        "endereco": loja.endereco,
        "capacidade_m3": loja.capacidade_m3,
        "ocupacao": round(loja.calcular_ocupacao_volume(), 2),
        "total_produtos": len(loja.estoque),
        "produtos_criticos": len(loja.listar_produtos_criticos())
    }


@app.get("/lojas/{loja_id}/estoque")
async def estoque_loja(loja_id: str):
    """Obter estoque completo de uma loja"""
    loja = gerenciador.lojas.get(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    estoque = [
        {
            "produto_id": item.produto.id,
            "produto_nome": item.produto.nome,
            "quantidade_atual": item.quantidade_atual,
            "quantidade_disponivel": item.quantidade_disponivel,
            "status": item.status,
            "estoque_minimo": item.produto.estoque_minimo
        }
        for item in loja.estoque.values()
    ]
    
    return {"loja": loja.nome, "total_itens": len(estoque), "estoque": estoque}


@app.get("/lojas/{loja_id}/alertas")
async def alertas_loja(loja_id: str):
    """Obter alertas de uma loja"""
    loja = gerenciador.lojas.get(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    # Busca CD principal
    cd = list(gerenciador.centros_distribuicao.values())[0] if gerenciador.centros_distribuicao else None
    if not cd:
        raise HTTPException(status_code=404, detail="Centro de distribuição não encontrado")
    
    alertas = analisador.gerar_alertas_loja(loja, cd)
    return {"loja": loja.nome, "total_alertas": len(alertas), "alertas": alertas}


# === ENDPOINTS DO CENTRO DE DISTRIBUIÇÃO ===

@app.get("/cd")
async def listar_centros():
    """Listar centros de distribuição"""
    centros = [
        {
            "id": cd.id,
            "nome": cd.nome,
            "relatorio": cd.relatorio_geral()
        }
        for cd in gerenciador.centros_distribuicao.values()
    ]
    return {"total": len(centros), "centros": centros}


@app.get("/cd/{cd_id}/estoque")
async def estoque_cd(cd_id: str):
    """Obter estoque do CD"""
    cd = gerenciador.centros_distribuicao.get(cd_id)
    if not cd:
        raise HTTPException(status_code=404, detail="CD não encontrado")
    
    estoque = [
        {
            "produto_id": item.produto.id,
            "produto_nome": item.produto.nome,
            "quantidade_atual": item.quantidade_atual,
            "quantidade_disponivel": item.quantidade_disponivel,
            "status": item.status
        }
        for item in cd.estoque.values()
    ]
    
    return {"cd": cd.nome, "total_itens": len(estoque), "estoque": estoque}


@app.post("/cd/{cd_id}/transferir")
async def transferir_produto(cd_id: str, transferencia: TransferenciaRequest):
    """Transferir produto do CD para loja"""
    resultado = gerenciador.transferir_para_loja(
        cd_id=cd_id,
        loja_id=transferencia.loja_destino_id,
        produto_id=transferencia.produto_id,
        quantidade=transferencia.quantidade,
        observacao=transferencia.observacao
    )
    
    if resultado["sucesso"]:
        return resultado
    else:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])


# === ENDPOINTS DO AGENTE IA ===

@app.post("/agente/analise-abastecimento/{loja_id}")
async def analisar_abastecimento(loja_id: str):
    """Solicitar análise de abastecimento ao agente IA"""
    loja = gerenciador.lojas.get(loja_id)
    if not loja:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    
    cd = list(gerenciador.centros_distribuicao.values())[0] if gerenciador.centros_distribuicao else None
    if not cd:
        raise HTTPException(status_code=404, detail="CD não encontrado")
    
    try:
        resposta = agente.analisar_necessidade_abastecimento(loja, cd)
        return {
            "loja": loja.nome,
            "timestamp": datetime.now().isoformat(),
            "analise": resposta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar agente: {str(e)}")


@app.post("/agente/otimizar-distribuicao")
async def otimizar_distribuicao():
    """Otimizar distribuição entre todas as lojas"""
    if not gerenciador.lojas:
        raise HTTPException(status_code=404, detail="Nenhuma loja cadastrada")
    
    cd = list(gerenciador.centros_distribuicao.values())[0] if gerenciador.centros_distribuicao else None
    if not cd:
        raise HTTPException(status_code=404, detail="CD não encontrado")
    
    try:
        lojas = list(gerenciador.lojas.values())
        resposta = agente.otimizar_distribuicao(cd, lojas)
        return {
            "timestamp": datetime.now().isoformat(),
            "total_lojas": len(lojas),
            "plano_distribuicao": resposta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar agente: {str(e)}")


@app.post("/agente/consulta")
async def consulta_livre(request: ConsultaAgenteRequest):
    """Fazer uma pergunta livre ao agente"""
    try:
        resposta = agente.consulta_livre(request.pergunta, request.contexto)
        return {
            "timestamp": datetime.now().isoformat(),
            "pergunta": request.pergunta,
            "resposta": resposta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar agente: {str(e)}")


@app.get("/agente/historico")
async def historico_agente():
    """Obter histórico de consultas ao agente"""
    historico = agente.obter_historico()
    return {
        "total_consultas": len(historico),
        "historico": historico[-10:]  # Últimas 10 consultas
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
