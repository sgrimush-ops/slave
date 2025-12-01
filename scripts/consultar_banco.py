"""
Script de exemplo para consultar o banco de dados SQLite
"""
from src.database import BancoDadosMix


def main():
    """Demonstra uso do banco de dados"""
    
    print("="*70)
    print("  CONSULTA AO BANCO DE DADOS - MIX DE PRODUTOS")
    print("="*70)
    
    try:
        # Conecta ao banco
        db = BancoDadosMix()
        
        # 1. Estatísticas gerais
        print("\n📊 ESTATÍSTICAS GERAIS")
        print("-"*70)
        stats = db.obter_estatisticas()
        print(f"Total de produtos: {stats['total_produtos']:,}")
        print(f"Total de origens: {stats['total_origens']}")
        print(f"Lojas cadastradas: {len(stats['lojas_cadastradas'])}")
        
        print(f"\n🏪 Códigos de lojas ativas:")
        lojas = stats['lojas_cadastradas']
        for i in range(0, len(lojas), 10):
            print(f"  {', '.join(lojas[i:i+10])}")
        
        print(f"\n📦 Top 10 Origens/Fornecedores:")
        for item in stats['produtos_por_origem']:
            print(f"  {item['origem']:20} - {item['total']:>5} produtos")
        
        # 2. Busca por termo
        print("\n\n🔍 BUSCA DE PRODUTOS")
        print("-"*70)
        termo = "MUCILON"
        print(f"Buscando por: '{termo}'")
        produtos = db.buscar_produtos(termo, limite=5)
        print(f"Encontrados: {len(produtos)} produtos\n")
        
        for prod in produtos[:5]:
            print(f"Código: {prod['codigo_interno']}")
            print(f"EAN: {prod['codigo_ean']}")
            print(f"Descrição: {prod['descricao']}")
            print(f"Origem: {prod['origem']}")
            print(f"Embalagem: {prod['embalagem']}")
            print(f"Lojas: {prod['loja_ativa_mix']}")
            print("-"*70)
        
        # 3. Produtos por origem
        print("\n\n📦 PRODUTOS POR ORIGEM")
        print("-"*70)
        origem = "nestle"
        print(f"Origem: {origem}")
        produtos_origem = db.obter_produtos_por_origem(origem)
        print(f"Total: {len(produtos_origem)} produtos\n")
        
        for prod in produtos_origem[:10]:
            print(f"  - {prod['descricao']}")
        
        if len(produtos_origem) > 10:
            print(f"  ... e mais {len(produtos_origem) - 10} produtos")
        
        # 4. Produtos por loja
        print("\n\n🏪 PRODUTOS POR LOJA")
        print("-"*70)
        codigo_loja = "002"
        print(f"Loja: {codigo_loja}")
        produtos_loja = db.obter_produtos_por_loja(codigo_loja)
        print(f"Total: {len(produtos_loja)} produtos ativos\n")
        
        for prod in produtos_loja[:10]:
            print(f"  - {prod['descricao']} ({prod['origem']})")
        
        if len(produtos_loja) > 10:
            print(f"  ... e mais {len(produtos_loja) - 10} produtos")
        
        # 5. Busca por código
        print("\n\n🔢 BUSCA POR CÓDIGO")
        print("-"*70)
        codigo = 1012475
        print(f"Código interno: {codigo}")
        produto = db.obter_produto_por_codigo_interno(codigo)
        
        if produto:
            print(f"\n✓ Produto encontrado:")
            print(f"  Código interno: {produto['codigo_interno']}")
            print(f"  Código EAN: {produto['codigo_ean']}")
            print(f"  Descrição: {produto['descricao']}")
            print(f"  Embalagem: {produto['embalagem']}")
            print(f"  Origem: {produto['origem']}")
            print(f"  Lojas ativas: {produto['loja_ativa_mix']}")
        else:
            print("✗ Produto não encontrado")
        
        # 6. Paginação
        print("\n\n📄 LISTAGEM PAGINADA")
        print("-"*70)
        pagina = 1
        por_pagina = 10
        produtos_pag, total_pags = db.listar_produtos_paginado(pagina, por_pagina)
        
        print(f"Página {pagina} de {total_pags} ({por_pagina} itens por página)\n")
        for i, prod in enumerate(produtos_pag, 1):
            print(f"{i:2}. {prod['descricao'][:50]:<50} | {prod['origem']}")
        
        # 7. Conversão para Produto
        print("\n\n🔄 CONVERSÃO PARA OBJETO PRODUTO")
        print("-"*70)
        produto_obj = db.converter_para_produto(
            produto, 
            preco_custo=12.50, 
            preco_venda=19.90
        )
        print(f"Produto convertido:")
        print(f"  ID: {produto_obj.id}")
        print(f"  Nome: {produto_obj.nome}")
        print(f"  Categoria: {produto_obj.categoria}")
        print(f"  Preço: R$ {produto_obj.preco_venda:.2f}")
        print(f"  Estoque mínimo: {produto_obj.estoque_minimo}")
        
        db.fechar()
        
        print("\n" + "="*70)
        print("  ✅ CONSULTAS CONCLUÍDAS COM SUCESSO!")
        print("="*70)
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        print("\n💡 Execute primeiro: python criar_banco.py")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
