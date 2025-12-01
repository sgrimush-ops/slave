"""
Script para calcular sugestões de pedido
"""
from src.calculador_pedido import CalculadorPedido


if __name__ == "__main__":
    # Inicializa calculador
    # dias_cobertura=4: estoque para 4 dias (considerando prazo de entrega de 2-4 dias)
    # margem_seguranca=1.2: 20% a mais para garantir exposição mínima
    calculador = CalculadorPedido(dias_cobertura=4, margem_seguranca=1.2)
    
    # Processa arquivo
    df = calculador.processar_arquivo(
        arquivo_entrada="data/gerado.xlsx",
        arquivo_saida="data/gerado_com_sugestao.xlsx"
    )
    
    # Gera relatório detalhado
    relatorio = calculador.gerar_relatorio_detalhado(df)
    
    # Salva relatório em texto
    with open("data/relatorio_sugestoes.txt", "w", encoding="utf-8") as f:
        f.write(relatorio)
    
    print(f"\n✅ Processamento concluído!")
    print(f"📄 Arquivo gerado: data/gerado_com_sugestao.xlsx")
    print(f"📄 Relatório: data/relatorio_sugestoes.txt")
