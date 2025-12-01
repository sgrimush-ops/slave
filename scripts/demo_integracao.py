"""
Script para demonstrar integração completa do banco de dados com o sistema
"""
from src.database import BancoDadosMix
from src.gerenciador import GerenciadorEstoque
from src.modelos import Loja, CentroDistribuicao, ItemEstoque


def demonstrar_integracao():
    """Demonstra integração do banco SQLite com o sistema de gestão"""
    
    print("="*70)
    print("  INTEGRAÇÃO: BANCO DE DADOS + SISTEMA DE GESTÃO")
    print("="*70)
    
    try:
        # 1. Conecta ao banco
        print("\n1️⃣ Conectando ao banco de dados...")
        db = BancoDadosMix()
        stats = db.obter_estatisticas()
        print(f"✓ Banco carregado: {stats['total_produtos']:,} produtos")
        
        # 2. Inicializa gerenciador
        print("\n2️⃣ Inicializando gerenciador de estoque...")
        gerenciador = GerenciadorEstoque()
        
        # 3. Cria Centro de Distribuição
        print("\n3️⃣ Criando Centro de Distribuição...")
        cd = CentroDistribuicao(
            id="cd_principal",
            nome="CD Principal",
            endereco="Av. Logística, 1000",
            capacidade_m3=1000.0,
            lojas_atendidas=stats['lojas_cadastradas']
        )
        gerenciador.adicionar_centro_distribuicao(cd)
        print(f"✓ CD criado: atende {len(cd.lojas_atendidas)} lojas")
        
        # 4. Cria lojas baseadas nos códigos do banco
        print("\n4️⃣ Criando lojas do banco de dados...")
        lojas_criadas = []
        
        # Mapeia códigos para nomes de lojas (exemplo - ajustar conforme necessário)
        mapa_lojas = {
            "002": ("Loja Centro", "Rua Principal, 100"),
            "003": ("Loja Norte", "Av. Norte, 250"),
            "004": ("Loja Sul", "Av. Sul, 300"),
            "006": ("Loja Leste", "Av. Leste, 400"),
            "011": ("Loja Shopping A", "Shopping Center A"),
            "012": ("Loja Shopping B", "Shopping Center B"),
        }
        
        for codigo in stats['lojas_cadastradas'][:6]:  # Primeiras 6 lojas
            if codigo in mapa_lojas:
                nome, endereco = mapa_lojas[codigo]
            else:
                nome = f"Loja {codigo}"
                endereco = f"Endereço Loja {codigo}"
            
            loja = Loja(
                id=f"loja_{codigo}",
                nome=nome,
                endereco=endereco,
                capacidade_m3=80.0
            )
            gerenciador.adicionar_loja(loja)
            lojas_criadas.append((codigo, loja))
            print(f"  ✓ {loja.nome} (código {codigo})")
        
        # 5. Importa produtos de exemplo do banco
        print("\n5️⃣ Importando produtos de exemplo...")
        
        # Busca produtos Nestlé como exemplo
        produtos_nestle = db.obter_produtos_por_origem("nestle")[:20]
        print(f"  Importando {len(produtos_nestle)} produtos Nestlé...")
        
        produtos_importados = 0
        for prod_data in produtos_nestle:
            # Converte para objeto Produto com preços de exemplo
            produto = db.converter_para_produto(
                prod_data,
                preco_custo=10.0 + (produtos_importados * 0.5),
                preco_venda=15.0 + (produtos_importados * 0.8)
            )
            gerenciador.adicionar_produto_catalogo(produto)
            
            # Adiciona ao CD
            gerenciador.adicionar_estoque_cd(
                "cd_principal",
                produto.id,
                quantidade=200 + (produtos_importados * 10)
            )
            
            produtos_importados += 1
        
        print(f"✓ {produtos_importados} produtos importados e adicionados ao CD")
        
        # 6. Distribui produtos para lojas baseado no mix
        print("\n6️⃣ Distribuindo produtos para as lojas...")
        
        for codigo, loja in lojas_criadas[:3]:  # Primeiras 3 lojas
            # Obtém produtos ativos para esta loja do banco
            produtos_loja_mix = db.obter_produtos_por_loja(codigo)
            
            # Pega alguns produtos importados que estão no mix da loja
            distribuidos = 0
            for prod_data in produtos_loja_mix[:10]:  # Primeiros 10
                cod_interno = str(prod_data['codigo_interno'])
                
                # Verifica se o produto foi importado
                if cod_interno in gerenciador.catalogo_produtos:
                    resultado = gerenciador.transferir_para_loja(
                        cd_id="cd_principal",
                        loja_id=loja.id,
                        produto_id=cod_interno,
                        quantidade=50,
                        observacao=f"Distribuição inicial - produto ativo no mix"
                    )
                    
                    if resultado['sucesso']:
                        distribuidos += 1
            
            print(f"  ✓ {loja.nome}: {distribuidos} produtos distribuídos")
        
        # 7. Relatório final
        print("\n7️⃣ Relatório Final")
        print("-"*70)
        print(f"📦 Banco de dados:")
        print(f"   Total no mix: {stats['total_produtos']:,} produtos")
        print(f"   Origens: {', '.join(stats['origens'][:5])}")
        print(f"   Lojas cadastradas: {len(stats['lojas_cadastradas'])}")
        
        print(f"\n🏢 Sistema de gestão:")
        print(f"   Produtos importados: {len(gerenciador.catalogo_produtos)}")
        print(f"   Centros de distribuição: {len(gerenciador.centros_distribuicao)}")
        print(f"   Lojas criadas: {len(gerenciador.lojas)}")
        
        print(f"\n📊 Estoque CD Principal:")
        cd = gerenciador.centros_distribuicao["cd_principal"]
        relatorio_cd = cd.relatorio_geral()
        print(f"   Total de produtos: {relatorio_cd['total_produtos']}")
        print(f"   Ocupação: {relatorio_cd['ocupacao_percentual']}%")
        
        print(f"\n🏪 Status das lojas:")
        for loja in gerenciador.lojas.values():
            print(f"   {loja.nome}:")
            print(f"     - Produtos: {len(loja.estoque)}")
            print(f"     - Ocupação: {loja.calcular_ocupacao_volume():.1f}%")
            print(f"     - Produtos críticos: {len(loja.listar_produtos_criticos())}")
        
        # 8. Exemplo de consulta integrada
        print("\n8️⃣ Exemplo: Consultando produto específico")
        print("-"*70)
        
        # Busca no banco
        produto_mix = db.buscar_produtos("MUCILON ARROZ", limite=1)[0]
        print(f"📋 Produto no mix:")
        print(f"   {produto_mix['descricao']}")
        print(f"   Código: {produto_mix['codigo_interno']}")
        print(f"   Origem: {produto_mix['origem']}")
        print(f"   Lojas ativas: {produto_mix['loja_ativa_mix']}")
        
        # Verifica no sistema
        cod = str(produto_mix['codigo_interno'])
        if cod in gerenciador.catalogo_produtos:
            produto_sistema = gerenciador.catalogo_produtos[cod]
            print(f"\n✓ Produto importado no sistema:")
            print(f"   Nome: {produto_sistema.nome}")
            print(f"   Preço: R$ {produto_sistema.preco_venda:.2f}")
            
            # Verifica estoque no CD
            item_cd = cd.obter_produto(cod)
            if item_cd:
                print(f"   Estoque CD: {item_cd.quantidade_atual} unidades")
        
        db.fechar()
        
        print("\n" + "="*70)
        print("  ✅ INTEGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*70)
        
        print("\n💡 Próximos passos:")
        print("  1. Execute: python -m src.cli")
        print("  2. Ou: python exemplo.py agente (para consultar o agente IA)")
        print("  3. Ou: python -m src.api (para iniciar a API REST)")
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        print("\n💡 Execute primeiro: python criar_banco.py")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demonstrar_integracao()
