from src.regras_negocio import obter_regras_completas, GIRO_ESTOQUE, ESTRATEGIAS

print("="*60)
print("VERIFICAÇÃO DAS REGRAS DE NEGÓCIO")
print("="*60)
print()

print("✅ Regras carregadas com sucesso!")
print()
print(f"📊 Giro de Estoque: {GIRO_ESTOQUE['dias_minimo']}-{GIRO_ESTOQUE['dias_maximo']} dias")
print(f"📈 Margem de segurança: {GIRO_ESTOQUE['margem_seguranca']} ({int((GIRO_ESTOQUE['margem_seguranca']-1)*100)}%)")
print(f"⚙️  Estratégias configuradas: {len(ESTRATEGIAS)}")
print()

print("="*60)
print("PREVIEW DAS REGRAS COMPLETAS")
print("="*60)
print(obter_regras_completas())
