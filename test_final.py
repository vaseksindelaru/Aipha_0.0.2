#!/usr/bin/env python3
"""
Test Final - Verificación completa del sistema AIPHA v2.0
Comprueba que todo funciona: .env, LLMClient, API connection
"""
import os
import sys
from dotenv import load_dotenv

print("\n" + "="*70)
print("🧪 VERIFICACIÓN FINAL - TODO LISTO")
print("="*70 + "\n")

# 1. Verificar .env
print("1️⃣  ¿Existe .env?", end="       ")
if os.path.exists(".env"):
    print("✅ SÍ")
else:
    print("❌ NO - Ejecuta: cp .env.example .env")
    sys.exit(1)

# 2. Verificar AIPHA_BRAIN_KEY
print("2️⃣  ¿AIPHA_BRAIN_KEY está configurada?", end="      ")
load_dotenv()
if os.environ.get("AIPHA_BRAIN_KEY"):
    print("✅ SÍ")
else:
    print("❌ NO")
    sys.exit(1)

# 3. Cargar .env
print("3️⃣  Cargando .env...", end="    ")
load_dotenv()
# Verify environment is loaded
if os.environ.get("AIPHA_BRAIN_KEY"):
    print("✅ Cargadas\n")
else:
    print("❌ Error loading .env\n")
    sys.exit(1)

# 4. Inicializar LLMClient
print("4️⃣  Inicializando LLMClient...", end="    ")
try:
    from core.llm_client import LLMClient
    client = LLMClient()
    print("✅ OK\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    sys.exit(1)

# 5. Probar conexión
print("5️⃣  Probando conexión con Qwen 2.5 Coder 32B...", end="       ")
try:
    response = client.health_check()
    if response:
        print("✅ Conexión OK\n")
    else:
        print("❌ Health-check falló\n")
        sys.exit(1)
except Exception as e:
    print(f"❌ Health-check falló: {e}\n")
    print("   ⚠️  Posibles causas:")
    print("   • Sin conexión a internet")
    print("   • API Key incorrecta")
    print("   • HuggingFace caído")
    sys.exit(1)

print("="*70)
print("✅ ¡TODO FUNCIONA CORRECTAMENTE!")
print("="*70)
print("\nPuedes usar ahora:")
print("  aipha brain diagnose    # Diagnóstico del sistema")
print("  aipha brain propose     # Generar propuestas")
print("  aipha brain health      # Ver salud del sistema\n")
