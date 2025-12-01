"""
Interface CLI para o sistema de gestão de estoque
"""
import sys
from datetime import datetime
from typing import Optional

from .modelos import Produto, Loja, CentroDistribuicao
from .gerenciador import GerenciadorEstoque
from .agente_estoque import AgenteEstoque
from .analisador import AnalisadorEstoque


class CLI:
    """Interface de linha de comando"""
    
    def __init__(self):
        self.gerenciador = GerenciadorEstoque()
        self.agente = AgenteEstoque()
        self.analisador = AnalisadorEstoque()
    
    def exibir_menu_principal(self):
        """Exibe menu principal"""
        print("\n" + "="*60)
        print("  SISTEMA DE GESTÃO DE ESTOQUE COM IA - LLaMA 3")
        print("="*60)
        print("\n1. Gerenciar Produtos")
        print("2. Gerenciar Lojas")
        print("3. Gerenciar Centro de Distribuição")
        print("4. Consultar Agente IA")
        print("5. Visualizar Alertas")
        print("6. Relatórios")
        print("0. Sair")
        print("-"*60)
    
    def menu_produtos(self):
        """Menu de produtos"""
        while True:
            print("\n--- PRODUTOS ---")
            print("1. Listar produtos")
            print("2. Adicionar produto")
            print("3. Buscar produto")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_produtos()
            elif opcao == "2":
                self.adicionar_produto()
            elif opcao == "3":
                self.buscar_produto()
            elif opcao == "0":
                break
    
    def listar_produtos(self):
        """Lista todos os produtos"""
        print("\n" + "="*60)
        print("CATÁLOGO DE PRODUTOS")
        print("="*60)
        
        if not self.gerenciador.catalogo_produtos:
            print("Nenhum produto cadastrado.")
            return
        
        for produto in self.gerenciador.catalogo_produtos.values():
            print(f"\n[{produto.id}] {produto.nome}")
            print(f"  Categoria: {produto.categoria}")
            print(f"  Preço: R$ {produto.preco_venda:.2f}")
            print(f"  Estoque mínimo: {produto.estoque_minimo} {produto.unidade}")
    
    def adicionar_produto(self):
        """Adiciona novo produto"""
        print("\n--- ADICIONAR PRODUTO ---")
        
        id_produto = input("ID do produto: ")
        nome = input("Nome: ")
        categoria = input("Categoria: ")
        unidade = input("Unidade (un, kg, cx): ")
        preco_custo = float(input("Preço de custo: R$ "))
        preco_venda = float(input("Preço de venda: R$ "))
        estoque_minimo = int(input("Estoque mínimo: "))
        
        produto = Produto(
            id=id_produto,
            nome=nome,
            categoria=categoria,
            unidade=unidade,
            preco_custo=preco_custo,
            preco_venda=preco_venda,
            estoque_minimo=estoque_minimo
        )
        
        self.gerenciador.adicionar_produto_catalogo(produto)
        print(f"\n✓ Produto '{nome}' adicionado com sucesso!")
    
    def buscar_produto(self):
        """Busca produto por ID"""
        id_produto = input("\nID do produto: ")
        produto = self.gerenciador.catalogo_produtos.get(id_produto)
        
        if produto:
            print(f"\n{produto.nome}")
            print(f"ID: {produto.id}")
            print(f"Categoria: {produto.categoria}")
            print(f"Preço: R$ {produto.preco_venda:.2f}")
            print(f"Estoque mínimo: {produto.estoque_minimo}")
        else:
            print("Produto não encontrado.")
    
    def menu_lojas(self):
        """Menu de lojas"""
        while True:
            print("\n--- LOJAS ---")
            print("1. Listar lojas")
            print("2. Adicionar loja")
            print("3. Ver estoque da loja")
            print("4. Adicionar estoque à loja")
            print("5. Registrar venda")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_lojas()
            elif opcao == "2":
                self.adicionar_loja()
            elif opcao == "3":
                self.ver_estoque_loja()
            elif opcao == "4":
                self.adicionar_estoque_loja()
            elif opcao == "5":
                self.registrar_venda()
            elif opcao == "0":
                break
    
    def listar_lojas(self):
        """Lista lojas"""
        print("\n" + "="*60)
        print("LOJAS")
        print("="*60)
        
        if not self.gerenciador.lojas:
            print("Nenhuma loja cadastrada.")
            return
        
        for loja in self.gerenciador.lojas.values():
            print(f"\n[{loja.id}] {loja.nome}")
            print(f"  Endereço: {loja.endereco}")
            print(f"  Produtos: {len(loja.estoque)}")
            print(f"  Críticos: {len(loja.listar_produtos_criticos())}")
            print(f"  Ocupação: {loja.calcular_ocupacao_volume():.1f}%")
    
    def adicionar_loja(self):
        """Adiciona nova loja"""
        print("\n--- ADICIONAR LOJA ---")
        
        id_loja = input("ID da loja: ")
        nome = input("Nome: ")
        endereco = input("Endereço: ")
        capacidade = float(input("Capacidade (m³): "))
        
        loja = Loja(
            id=id_loja,
            nome=nome,
            endereco=endereco,
            capacidade_m3=capacidade
        )
        
        self.gerenciador.adicionar_loja(loja)
        print(f"\n✓ Loja '{nome}' adicionada com sucesso!")
    
    def ver_estoque_loja(self):
        """Visualiza estoque de uma loja"""
        id_loja = input("\nID da loja: ")
        loja = self.gerenciador.lojas.get(id_loja)
        
        if not loja:
            print("Loja não encontrada.")
            return
        
        print(f"\n{'='*60}")
        print(f"ESTOQUE - {loja.nome}")
        print('='*60)
        
        if not loja.estoque:
            print("Estoque vazio.")
            return
        
        for item in loja.estoque.values():
            print(f"\n{item.produto.nome}")
            print(f"  Quantidade: {item.quantidade_atual} {item.produto.unidade}")
            print(f"  Status: {item.status}")
            print(f"  Mínimo: {item.produto.estoque_minimo}")
    
    def adicionar_estoque_loja(self):
        """Adiciona estoque a uma loja"""
        id_loja = input("\nID da loja: ")
        id_produto = input("ID do produto: ")
        quantidade = int(input("Quantidade: "))
        
        resultado = self.gerenciador.adicionar_estoque_loja(
            id_loja, id_produto, quantidade
        )
        
        print(f"\n{resultado['mensagem']}")
    
    def registrar_venda(self):
        """Registra uma venda"""
        id_loja = input("\nID da loja: ")
        id_produto = input("ID do produto: ")
        quantidade = int(input("Quantidade vendida: "))
        
        resultado = self.gerenciador.registrar_venda(
            id_loja, id_produto, quantidade
        )
        
        print(f"\n{resultado['mensagem']}")
    
    def menu_agente(self):
        """Menu do agente IA"""
        while True:
            print("\n--- AGENTE IA (LLaMA 3) ---")
            print("1. Analisar necessidade de abastecimento")
            print("2. Otimizar distribuição entre lojas")
            print("3. Consulta livre")
            print("4. Ver histórico")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.analisar_abastecimento()
            elif opcao == "2":
                self.otimizar_distribuicao()
            elif opcao == "3":
                self.consulta_livre_agente()
            elif opcao == "4":
                self.ver_historico_agente()
            elif opcao == "0":
                break
    
    def analisar_abastecimento(self):
        """Solicita análise ao agente"""
        id_loja = input("\nID da loja: ")
        loja = self.gerenciador.lojas.get(id_loja)
        
        if not loja:
            print("Loja não encontrada.")
            return
        
        if not self.gerenciador.centros_distribuicao:
            print("Nenhum CD cadastrado.")
            return
        
        cd = list(self.gerenciador.centros_distribuicao.values())[0]
        
        print("\n🤖 Consultando agente LLaMA 3...\n")
        resposta = self.agente.analisar_necessidade_abastecimento(loja, cd)
        
        print("="*60)
        print(resposta)
        print("="*60)
    
    def otimizar_distribuicao(self):
        """Otimiza distribuição"""
        if not self.gerenciador.lojas:
            print("\nNenhuma loja cadastrada.")
            return
        
        if not self.gerenciador.centros_distribuicao:
            print("Nenhum CD cadastrado.")
            return
        
        cd = list(self.gerenciador.centros_distribuicao.values())[0]
        lojas = list(self.gerenciador.lojas.values())
        
        print("\n🤖 Consultando agente LLaMA 3...\n")
        resposta = self.agente.otimizar_distribuicao(cd, lojas)
        
        print("="*60)
        print(resposta)
        print("="*60)
    
    def consulta_livre_agente(self):
        """Consulta livre ao agente"""
        print("\nFaça uma pergunta ao agente (ou 'sair' para voltar):")
        pergunta = input("> ")
        
        if pergunta.lower() == 'sair':
            return
        
        print("\n🤖 Consultando agente LLaMA 3...\n")
        resposta = self.agente.consulta_livre(pergunta)
        
        print("="*60)
        print(resposta)
        print("="*60)
    
    def ver_historico_agente(self):
        """Visualiza histórico de consultas"""
        historico = self.agente.obter_historico()
        
        print(f"\n{'='*60}")
        print(f"HISTÓRICO DE CONSULTAS ({len(historico)} total)")
        print('='*60)
        
        for i, consulta in enumerate(historico[-10:], 1):
            print(f"\n{i}. {consulta['tipo']} - {consulta['timestamp']}")
    
    def visualizar_alertas(self):
        """Visualiza alertas do sistema"""
        print(f"\n{'='*60}")
        print("ALERTAS DO SISTEMA")
        print('='*60)
        
        if not self.gerenciador.lojas:
            print("Nenhuma loja cadastrada.")
            return
        
        if not self.gerenciador.centros_distribuicao:
            print("Nenhum CD cadastrado.")
            return
        
        cd = list(self.gerenciador.centros_distribuicao.values())[0]
        
        total_alertas = 0
        for loja in self.gerenciador.lojas.values():
            alertas = self.analisador.gerar_alertas_loja(loja, cd)
            
            if alertas:
                print(f"\n{loja.nome}:")
                for alerta in alertas:
                    print(f"  [{alerta['prioridade']}] {alerta['mensagem']}")
                    total_alertas += 1
        
        if total_alertas == 0:
            print("\nNenhum alerta no momento! ✓")
    
    def executar(self):
        """Executa a CLI"""
        while True:
            self.exibir_menu_principal()
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.menu_produtos()
            elif opcao == "2":
                self.menu_lojas()
            elif opcao == "3":
                print("\nFuncionalidade em desenvolvimento.")
            elif opcao == "4":
                self.menu_agente()
            elif opcao == "5":
                self.visualizar_alertas()
            elif opcao == "6":
                print("\nFuncionalidade em desenvolvimento.")
            elif opcao == "0":
                print("\nAté logo!")
                break
            else:
                print("\nOpção inválida!")


def main():
    """Função principal"""
    cli = CLI()
    cli.executar()


if __name__ == "__main__":
    main()
