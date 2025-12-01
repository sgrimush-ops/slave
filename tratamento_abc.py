#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tratamento de Dados ABC

Este script processa o arquivo grid_tmp_abcmerc.csv:
1. Lê os nomes das colunas de colunas.txt
2. Remove colunas desnecessárias
3. Adiciona coluna data_venda informada pelo usuário
4. Gera arquivo Excel com resultado
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import pyarrow.parquet as pq
import pyarrow as pa


def ler_nomes_colunas(arquivo_colunas='colunas.txt'):
    """
    Lê os nomes das colunas do arquivo colunas.txt
    
    Returns:
        Lista com nomes das colunas
    """
    print(f"[INFO] Lendo nomes das colunas de: {arquivo_colunas}")
    
    if not os.path.exists(arquivo_colunas):
        print(f"[ERRO] Arquivo {arquivo_colunas} não encontrado!")
        return None
    
    colunas = []
    with open(arquivo_colunas, 'r', encoding='utf-8') as f:
        for linha in f:
            # Remove espaços e quebras de linha
            linha = linha.strip()
            if linha:
                # Formato: "1\tloja" ou "1 coluna==loja"
                if '\t' in linha:
                    # Separado por tab
                    partes = linha.split('\t')
                    if len(partes) >= 2:
                        nome_coluna = partes[1].strip()
                        colunas.append(nome_coluna)
                elif '==' in linha:
                    # Formato "1 coluna==loja"
                    nome_coluna = linha.split('==')[1].strip()
                    colunas.append(nome_coluna)
    
    print(f"[OK] {len(colunas)} colunas encontradas")
    return colunas


def validar_data(data_str):
    """
    Valida e formata a data no formato dd/mm/yy
    
    Args:
        data_str: String com data no formato dd/mm/yy
        
    Returns:
        String formatada ou None se inválida
    """
    try:
        # Tenta converter para verificar se é válida
        data_obj = datetime.strptime(data_str, '%d/%m/%y')
        return data_str
    except ValueError:
        return None


def salvar_no_banco_parquet(df_novo, arquivo_parquet, data_venda):
    """
    Salva dados no banco Parquet de forma incremental
    Se já existir dados para a mesma data, substitui
    Caso contrário, adiciona novos registros
    
    Args:
        df_novo: DataFrame com novos dados
        arquivo_parquet: Caminho do arquivo Parquet
        data_venda: Data dos dados sendo inseridos
    """
    print(f"\n[INFO] Salvando no banco de dados Parquet...")
    
    try:
        # Verifica se arquivo já existe
        if os.path.exists(arquivo_parquet):
            print(f"   [INFO] Banco existente encontrado, carregando...")
            df_existente = pd.read_parquet(arquivo_parquet)
            print(f"   [INFO] Registros existentes: {len(df_existente)}")
            
            # Verificar se já existe dados para esta data
            if 'data_venda' in df_existente.columns:
                registros_mesma_data = len(df_existente[df_existente['data_venda'] == data_venda])
                
                if registros_mesma_data > 0:
                    print(f"   [AVISO] Encontrados {registros_mesma_data} registros para {data_venda}")
                    print(f"   [INFO] Removendo registros antigos dessa data...")
                    # Remove registros da mesma data
                    df_existente = df_existente[df_existente['data_venda'] != data_venda]
                    print(f"   [OK] Registros removidos. Restam {len(df_existente)} registros")
            
            # Combinar dados existentes com novos
            df_final = pd.concat([df_existente, df_novo], ignore_index=True)
            print(f"   [INFO] Adicionando {len(df_novo)} novos registros")
            
        else:
            print(f"   [INFO] Criando novo banco de dados...")
            df_final = df_novo
        
        # Salvar no formato Parquet
        df_final.to_parquet(arquivo_parquet, index=False, engine='pyarrow', compression='snappy')
        
        print(f"   [OK] Banco atualizado com sucesso!")
        print(f"   [INFO] Total de registros no banco: {len(df_final)}")
        
        # Mostrar estatísticas por data
        if 'data_venda' in df_final.columns:
            print(f"\n   [INFO] Registros por data:")
            contagem_datas = df_final['data_venda'].value_counts().sort_index()
            for data, count in contagem_datas.items():
                print(f"      {data}: {count} registros")
        
    except Exception as e:
        print(f"   [ERRO] Erro ao salvar no banco Parquet: {e}")
        print(f"   [AVISO] O arquivo Excel foi salvo, mas o banco não foi atualizado")


def solicitar_data_venda():
    """
    Solicita ao usuário a data de venda
    Sugere o dia anterior como padrão
    
    Returns:
        String com data no formato dd/mm/yy
    """
    print("\n" + "="*60)
    print("INFORMAR DATA DE VENDA")
    print("="*60)
    
    # Sugerir dia anterior
    data_ontem = (datetime.now() - timedelta(days=1)).strftime('%d/%m/%y')
    print(f"\n[INFO] Data sugerida (ontem): {data_ontem}")
    
    while True:
        data = input(f"Digite a data de venda ou ENTER para usar {data_ontem}: ").strip()
        
        # Se usuário pressionou ENTER, usar data sugerida
        if not data:
            data = data_ontem
            print(f"[OK] Usando data sugerida: {data}")
            return data
        
        data_validada = validar_data(data)
        if data_validada:
            print(f"[OK] Data válida: {data_validada}")
            return data_validada
        else:
            print("[ERRO] Data inválida! Use o formato dd/mm/yy (exemplo: 30/11/25)")


def processar_arquivo_abc(
    arquivo_csv='grid_tmp_abcmerc.csv',
    arquivo_colunas='colunas.txt',
    arquivo_saida='resultado_abc.xlsx'
):
    """
    Processa o arquivo CSV com dados ABC
    
    Args:
        arquivo_csv: Arquivo CSV de entrada
        arquivo_colunas: Arquivo com nomes das colunas
        arquivo_saida: Arquivo Excel de saída
    """
    
    print("="*60)
    print("TRATAMENTO DE DADOS ABC")
    print("="*60)
    print()
    
    # 1. Ler nomes das colunas
    nomes_colunas = ler_nomes_colunas(arquivo_colunas)
    if not nomes_colunas:
        return
    
    # 2. Ler arquivo CSV
    print(f"\n[INFO] Lendo arquivo CSV: {arquivo_csv}")
    
    if not os.path.exists(arquivo_csv):
        print(f"[ERRO] Arquivo {arquivo_csv} não encontrado!")
        return
    
    try:
        # Tenta ler com diferentes encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'windows-1252']
        df = None
        
        for encoding in encodings:
            try:
                # Ler CSV sem especificar decimal/thousands primeiro
                # O pandas vai detectar automaticamente o formato
                df = pd.read_csv(
                    arquivo_csv, 
                    header=None, 
                    encoding=encoding, 
                    sep=';',
                    dtype=str  # Ler tudo como string primeiro para converter depois
                )
                print(f"[OK] Arquivo lido com encoding '{encoding}': {len(df)} linhas, {len(df.columns)} colunas")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print(f"[ERRO] Não foi possível ler o arquivo com nenhum encoding testado")
            return
            
    except Exception as e:
        print(f"[ERRO] Erro ao ler CSV: {e}")
        return
    
    # 3. Verificar se número de colunas bate
    if len(df.columns) != len(nomes_colunas):
        print(f"[AVISO] CSV tem {len(df.columns)} colunas, mas colunas.txt tem {len(nomes_colunas)} nomes")
        print(f"   Usando {min(len(df.columns), len(nomes_colunas))} colunas")
        nomes_colunas = nomes_colunas[:len(df.columns)]
    
    # Atribuir nomes às colunas
    df.columns = nomes_colunas
    print(f"\n[OK] Colunas nomeadas: {list(df.columns)}")
    
    # 3.5. Converter colunas numéricas do formato brasileiro
    print("\n[INFO] Convertendo números do formato brasileiro...")
    colunas_numericas = [
        'valor_venda', 'quantidade_vendida', 'ponto_pedido', 
        'estoque_ideal', 'embalagem', 'capacidade', 'estoque', 'estoque_cd'
    ]
    
    def converter_numero_brasileiro(valor):
        """Converte número no formato brasileiro (1.234,56) para float"""
        if pd.isna(valor) or valor == '':
            return 0.0
        
        # Se já for número, retorna
        if isinstance(valor, (int, float)):
            return float(valor)
        
        # Converter string
        valor_str = str(valor).strip()
        
        # Remover pontos (separador de milhares) e substituir vírgula por ponto (decimal)
        # Exemplo: "1.234,56" -> "1234.56"
        valor_str = valor_str.replace('.', '')  # Remove pontos (milhares)
        valor_str = valor_str.replace(',', '.')  # Vírgula vira ponto (decimal)
        
        try:
            return float(valor_str)
        except ValueError:
            return 0.0
    
    for col in colunas_numericas:
        if col in df.columns:
            print(f"  Convertendo coluna: {col}")
            df[col] = df[col].apply(converter_numero_brasileiro)
    
    print("[OK] Conversão de números concluída!")
    
    # 3.6. Normalizar códigos com padding de zeros
    print("\n[INFO] Normalizando códigos e lojas com zeros à esquerda...")
    
    # Padronizar loja com 3 dígitos (001, 002, etc)
    if 'loja' in df.columns:
        df['loja'] = df['loja'].astype(str).str.zfill(3)
        print("  [OK] Coluna 'loja' padronizada com 3 dígitos")
    
    # Padronizar codigo_interno com 7 dígitos (0021771, etc)
    if 'codigo_interno' in df.columns:
        df['codigo_interno'] = df['codigo_interno'].astype(str).str.zfill(7)
        print("  [OK] Coluna 'codigo_interno' padronizada com 7 dígitos")
    
    # 4. Definir colunas a remover
    colunas_remover = [
        'percentual_venda',
        'posicao_venda',
        'percentual_acumulado',
        'valor_margem',
        'percentual_margem',
        'participacao',  # Sem acento
        'posicao_margem',
        'acumulo_margem',
        'ranking_margem',
        'cmv_bruto',
        'cmv_liquido',
        'fornecedor_principal',
        'tributacao',  # CORRIGIDO: Sem cedilha (como está no colunas.txt)
        'usuario',
        'departamento',
        'grupo',
        'subgrupo',
        'tipo_comercial',
        'rankin_venda'
    ]
    
    # Remover apenas colunas que existem no DataFrame
    colunas_existentes_para_remover = [col for col in colunas_remover if col in df.columns]
    
    if colunas_existentes_para_remover:
        print(f"\n[INFO] Removendo {len(colunas_existentes_para_remover)} colunas:")
        for col in colunas_existentes_para_remover:
            print(f"   - {col}")
        
        df = df.drop(columns=colunas_existentes_para_remover)
        print(f"[OK] Colunas removidas. Restaram {len(df.columns)} colunas")
    else:
        print("\n[AVISO] Nenhuma das colunas para remover foi encontrada no DataFrame")
    
    print(f"\n[INFO] Colunas finais: {list(df.columns)}")
    
    # 5. Solicitar data de venda
    data_venda = solicitar_data_venda()
    
    # 6. Filtrar linhas
    print(f"\n[INFO] Filtrando linhas...")
    linhas_originais = len(df)
    print(f"   Total de linhas antes dos filtros: {linhas_originais}")
    
    # Filtro 1: Manter apenas seções específicas (10, 13, 14, 16, 17, 23)
    secoes_validas = ['10', '13', '14', '16', '17', '23']
    if 'secao' in df.columns:
        # Filtra seções que começam com os números especificados
        df = df[df['secao'].astype(str).str[:2].isin(secoes_validas)]
        linhas_removidas_secao = linhas_originais - len(df)
        print(f"   [OK] Removidas {linhas_removidas_secao} linhas (seções diferentes de {secoes_validas})")
    else:
        print(f"   [AVISO] Coluna 'secao' não encontrada, pulando filtro de seção")
        linhas_removidas_secao = 0
    
    linhas_antes = len(df)
    
    # Filtro 2: Remove linhas onde ponto_pedido OU embalagem são zero
    if 'ponto_pedido' in df.columns and 'embalagem' in df.columns:
        df = df[(df['ponto_pedido'] != 0) & (df['embalagem'] != 0)]
        linhas_removidas_zeros = linhas_antes - len(df)
        print(f"   [OK] Removidas {linhas_removidas_zeros} linhas com ponto_pedido=0 ou embalagem=0")
        print(f"   [OK] Linhas restantes: {len(df)}")
    else:
        print(f"   [AVISO] Colunas ponto_pedido ou embalagem não encontradas, pulando filtro")
        linhas_removidas_zeros = 0
    
    # 7. Adicionar coluna data_venda
    df['data_venda'] = data_venda
    print(f"\n[OK] Coluna 'data_venda' adicionada com valor: {data_venda}")
    
    # 8. Mostrar preview dos dados
    print("\n" + "="*60)
    print("PREVIEW DOS DADOS (primeiras 5 linhas)")
    print("="*60)
    print(df.head())
    
    # 9. Salvar em Excel
    print(f"\n[INFO] Salvando arquivo Excel: {arquivo_saida}")
    try:
        df.to_excel(arquivo_saida, index=False)
        print(f"[OK] Arquivo salvo com sucesso!")
        print(f"   Total de linhas: {len(df)}")
        print(f"   Total de colunas: {len(df.columns)}")
    except Exception as e:
        print(f"[ERRO] Erro ao salvar Excel: {e}")
        return
    
    # 10. Salvar no banco de dados Parquet (incremental)
    arquivo_parquet = 'data/vendas_historico.parquet'
    salvar_no_banco_parquet(df, arquivo_parquet, data_venda)
    
    # 11. Estatísticas finais
    print("\n" + "="*60)
    print("ESTATÍSTICAS")
    print("="*60)
    print(f"Linhas originais: {linhas_originais}")
    print(f"Linhas removidas (filtro seção): {linhas_removidas_secao}")
    print(f"Linhas removidas (ponto_pedido/embalagem): {linhas_removidas_zeros if 'linhas_removidas_zeros' in locals() else 0}")
    print(f"Total removido: {linhas_removidas_secao + (linhas_removidas_zeros if 'linhas_removidas_zeros' in locals() else 0)}")
    print(f"Linhas finais: {len(df)}")
    print(f"Colunas finais: {len(df.columns)}")
    print(f"Data de venda: {data_venda}")
    print(f"\nColunas mantidas:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print("\n" + "="*60)
    print("PROCESSAMENTO CONCLUÍDO!")
    print("="*60)


def main():
    """Função principal"""
    
    # Define arquivos
    arquivo_csv = 'data/grid_tmp_abcmerc.csv'
    arquivo_colunas = 'data/colunas.txt'
    arquivo_saida = 'data/resultado_abc.xlsx'
    
    # Processa
    processar_arquivo_abc(arquivo_csv, arquivo_colunas, arquivo_saida)


if __name__ == "__main__":
    main()
