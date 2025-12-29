#!/usr/bin/env python3
"""
Test comprehensivo de todos los comandos brain
"""
import subprocess
import sys
import time

def run_command(cmd):
    """Ejecuta un comando y retorna (success, output)"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)

def test_brain_commands():
    """Prueba todos los comandos brain"""
    print("\n" + "="*70)
    print("🧠 TEST COMPREHENSIVO - SUPER CEREBRO v2.0")
    print("="*70 + "\n")
    
    tests = [
        ("✅ brain --help", "python3 -m aiphalab.cli brain --help", "group"),
        ("✅ test-connection", "python3 -m aiphalab.cli brain test-connection", "test"),
        ("✅ health", "python3 -m aiphalab.cli brain health", "health"),
        ("✅ diagnose", "python3 -m aiphalab.cli brain diagnose", "diagnose"),
        ("✅ propose", "python3 -m aiphalab.cli brain propose", "propose"),
    ]
    
    results = []
    for name, cmd, test_type in tests:
        print(f"\n🔍 Probando: {name}")
        print(f"   Comando: {cmd}")
        
        success, output = run_command(cmd)
        
        # Validaciones específicas por tipo
        if test_type == "group":
            valid = "test-connection" in output and "diagnose" in output
        elif test_type == "test":
            valid = ("Conexión exitosa" in output or "✨" in output) and success
        elif test_type == "health":
            valid = "Estado" in output and success
        elif test_type == "diagnose":
            valid = ("DIAGNÓSTICO" in output or "diagnóstico" in output) and success
        elif test_type == "propose":
            valid = "propuesta" in output.lower() or success
        else:
            valid = success
        
        status = "✅ PASS" if valid else "❌ FAIL"
        results.append((name, valid))
        print(f"   {status}")
        
        if not valid and output:
            print(f"   Output (primeras 200 chars): {output[:200]}")
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN")
    print("="*70)
    passed = sum(1 for _, valid in results if valid)
    total = len(results)
    
    for name, valid in results:
        status = "✅" if valid else "❌"
        print(f"{status} {name}")
    
    print(f"\n✨ Resultados: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n🎉 ¡TODO FUNCIONANDO PERFECTAMENTE!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(test_brain_commands())
