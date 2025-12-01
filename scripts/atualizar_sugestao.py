"""
Script para atualizar APENAS a coluna 'sugestao' no arquivo original gerado.xlsx
"""
import pandas as pd
from src.calculador_pedido import CalculadorPedido


def atualizar_coluna_sugestao():
    """Atualiza apenas a coluna sugestao no arquivo original"""
    
    print("="*70)
    print("  ATUALIZANDO COLUNA 'SUGESTAO' NO ARQUIVO ORIGINAL")
    print("="*70)
    print()
    
    # Ler arquivo original
    print("📂 Lendo arquivo: data/gerado.xlsx")
    df = pd.read_excel("data/gerado.xlsx")
    
    print(f"✓ {len(df)} linhas encontradas\n")
    
    # Inicializar calculador
    calculador = CalculadorPedido(dias_cobertura=4, margem_seguranca=1.2)
    
    # Calcular sugestões
    print("🧮 Calculando sugestões...\n")
    sugestoes = []
    
    for idx, row in df.iterrows():
        resultado = calculador.calcular_sugestao_pedido(
            estoque_atual=int(row['estoque_atual']),
            venda_media_dia=float(row['venda_media_dia']),
            embalagem=int(row['embalagem']),
            venda_7dias=int(row['venda_acumulada_7dias']),
            venda_14dias=int(row['venda_acumulada_14dias']),
            venda_30dias=int(row['venda_acumulada_30dias']),
            venda_60dias=int(row['venda_acumulada_60dias'])
        )
        
        sugestoes.append(resultado['sugestao_unidades'])
        
        # Print simplificado
        if resultado['sugestao_unidades'] > 0:
            print(f"  [{idx+1}] Produto {row['codigo_interno']}: {resultado['sugestao_caixas']} caixas")
    
    # Atualizar coluna sugestao
    df['sugestao'] = sugestoes
    
    # Salvar arquivo (sobrescrevendo o original)
    print(f"\n💾 Salvando arquivo atualizado: data/gerado.xlsx")
    df.to_excel("data/gerado.xlsx", index=False)
    
    print("\n✅ Coluna 'sugestao' atualizada com sucesso!")
    print(f"\n📊 Resumo:")
    print(f"   Total de linhas: {len(df)}")
    print(f"   Linhas com sugestão > 0: {len(df[df['sugestao'] > 0])}")
    print(f"   Total de unidades sugeridas: {df['sugestao'].sum():.0f}")
    

if __name__ == "__main__":
    atualizar_coluna_sugestao()
