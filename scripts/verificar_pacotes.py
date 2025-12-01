import sys

packages = [
    'fastapi',
    'uvicorn', 
    'pandas',
    'numpy',
    'openpyxl',
    'ollama',
    'requests',
    'pydantic'
]

print("Verificando pacotes instalados...\n")

missing = []
installed = []

for package in packages:
    try:
        __import__(package)
        installed.append(package)
        print(f"✅ {package}")
    except ImportError:
        missing.append(package)
        print(f"❌ {package}")

print(f"\n{'='*50}")
if missing:
    print(f"⚠️  {len(missing)} pacote(s) faltante(s): {', '.join(missing)}")
    print(f"\nPara instalar:")
    print(f"pip install {' '.join(missing)}")
else:
    print(f"✅ Todos os {len(installed)} pacotes estão instalados!")
print(f"{'='*50}")
