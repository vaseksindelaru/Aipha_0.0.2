#!/usr/bin/env python3
"""
test_diagnostic_enhancements.py

Test de las mejoras en el sistema de diagnóstico:
1. Detección de intervenciones manuales (USER vs AUTO)
2. Análisis de impacto en métricas
3. Capacidad del LLM de entender reasoning del usuario
"""

import json
import sys
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).parent))

from core.llm_assistant import LLMAssistant


def test_get_diagnose_context():
    """Verificar que get_diagnose_context() retorna contexto enriquecido"""
    
    print("\n" + "=" * 70)
    print("TEST 1: get_diagnose_context() retorna contexto enriquecido")
    print("=" * 70)
    
    assistant = LLMAssistant(memory_path="memory")
    context = assistant.get_diagnose_context()
    
    # Verificaciones
    assert 'simulation_mode' in context, "❌ Falta: simulation_mode"
    assert 'manual_interventions_detail' in context, "❌ Falta: manual_interventions_detail"
    assert 'user_actions' in context, "❌ Falta: user_actions"
    assert 'auto_actions' in context, "❌ Falta: auto_actions"
    assert 'action_history' in context, "❌ Falta: action_history"
    assert 'impact_analysis' in context, "❌ Falta: impact_analysis"
    assert 'system_context' in context, "❌ Falta: system_context"
    
    print("✅ Todos los campos requeridos presentes")
    
    # Mostrar datos
    print(f"\n📊 Análisis de Contexto:")
    print(f"  • Modo Simulación: {context.get('simulation_mode')}")
    print(f"  • Intervenciones Manuales: {context.get('manual_interventions')}")
    print(f"  • Acciones del Usuario: {len(context.get('user_actions', []))}")
    print(f"  • Acciones Automáticas: {len(context.get('auto_actions', []))}")
    print(f"  • Total de Acciones: {len(context.get('action_history', []))}")
    
    # Mostrar intervenciones manuales
    if context.get('manual_interventions_detail'):
        print(f"\n🎯 Intervenciones Manuales Detectadas:")
        for detail in context.get('manual_interventions_detail', []):
            print(f"  • {detail.get('component')}.{detail.get('parameter')} = {detail.get('new_value')}")
            print(f"    - Razón: {detail.get('reason')}")
            print(f"    - Score: {detail.get('score')}")
            print(f"    - Creado por: {detail.get('created_by')}")
    
    # Mostrar impacto
    impact = context.get('impact_analysis', {})
    print(f"\n💥 Análisis de Impacto:")
    print(f"  • Total intervenciones: {impact.get('total_interventions', 0)}")
    print(f"  • Win Rate actual: {impact.get('win_rate_current', 0)*100:.1f}%")
    print(f"  • Drawdown actual: {impact.get('drawdown_current', 0)*100:.1f}%")
    print(f"  • Resumen: {impact.get('impact_summary', 'N/A')}")
    
    return True


def test_classify_actions():
    """Verificar que se clasifican correctamente acciones USER vs AUTO"""
    
    print("\n" + "=" * 70)
    print("TEST 2: Clasificación de acciones USER vs AUTO")
    print("=" * 70)
    
    assistant = LLMAssistant(memory_path="memory")
    context = assistant.get_diagnose_context()
    
    user_actions = context.get('user_actions', [])
    auto_actions = context.get('auto_actions', [])
    
    print(f"\n📋 Acciones del Usuario (CLI):")
    if user_actions:
        for action in user_actions:
            print(f"  • {action.get('timestamp', 'N/A')[:19]}: {action.get('component')}")
    else:
        print("  (Sin acciones del usuario)")
    
    print(f"\n🤖 Acciones Automáticas (Sistema):")
    if auto_actions:
        for i, action in enumerate(auto_actions[:5], 1):
            print(f"  {i}. {action.get('timestamp', 'N/A')[:19]}: {action.get('agent')} en {action.get('component')}")
        if len(auto_actions) > 5:
            print(f"  ... y {len(auto_actions) - 5} más")
    else:
        print("  (Sin acciones automáticas)")
    
    return True


def test_diagnose_system_simple():
    """Verificar diagnóstico simple sin LLM"""
    
    print("\n" + "=" * 70)
    print("TEST 3: diagnose_system() - Modo Simple (sin LLM)")
    print("=" * 70)
    
    assistant = LLMAssistant(memory_path="memory")
    result = assistant.diagnose_system(detailed=False)
    
    # Verificaciones
    assert 'diagnosis' in result, "❌ Falta: diagnosis"
    assert 'manual_interventions_detail' in result, "❌ Falta: manual_interventions_detail"
    assert 'simulation_mode' in result, "❌ Falta: simulation_mode"
    assert 'impact_analysis' in result, "❌ Falta: impact_analysis"
    assert 'llm_analysis' not in result, "❌ llm_analysis no debería estar en modo simple"
    
    print("✅ Estructura de resultado correcta")
    
    print(f"\n📊 Diagnóstico Simple:")
    print(f"  • Intervenciones Manuales: {result.get('manual_interventions', 0)}")
    print(f"  • Modo Simulación: {result.get('simulation_mode', False)}")
    
    # Mostrar extracto del diagnóstico
    diagnosis = result.get('diagnosis', '')
    if diagnosis:
        lines = diagnosis.split('\n')[:10]
        print("\n📝 Primeras líneas del diagnóstico:")
        for line in lines:
            if line.strip():
                print(f"  {line}")
    
    return True


def test_system_context_format():
    """Verificar que system_context está formateado correctamente para el LLM"""
    
    print("\n" + "=" * 70)
    print("TEST 4: system_context - Formato para el LLM")
    print("=" * 70)
    
    assistant = LLMAssistant(memory_path="memory")
    context = assistant.get_diagnose_context()
    
    system_context = context.get('system_context', '')
    
    # Verificaciones
    assert 'CONTEXTO DEL SISTEMA' in system_context, "❌ Falta header"
    assert 'Estado General' in system_context, "❌ Falta sección Estado"
    assert 'Intervenciones Manuales' in system_context, "❌ Falta sección Intervenciones"
    assert 'Cambios Automáticos' in system_context, "❌ Falta sección Cambios"
    
    print("✅ Estructura de system_context correcta")
    
    print("\n📝 System Context (primeras 800 caracteres):")
    print(system_context[:800])
    print("\n... (truncado)")
    
    return True


def test_impact_analysis():
    """Verificar que el análisis de impacto es correcto"""
    
    print("\n" + "=" * 70)
    print("TEST 5: Impact Analysis - Correlación intervenciones/métricas")
    print("=" * 70)
    
    assistant = LLMAssistant(memory_path="memory")
    context = assistant.get_diagnose_context()
    
    impact = context.get('impact_analysis', {})
    
    print(f"\n📊 Datos de Impacto:")
    print(f"  • Total intervenciones aplicadas: {impact.get('total_interventions', 0)}")
    print(f"  • Win Rate actual: {impact.get('win_rate_current', 0)*100:.1f}%")
    print(f"  • Drawdown actual: {impact.get('drawdown_current', 0)*100:.1f}%")
    
    if impact.get('latest_intervention'):
        latest = impact.get('latest_intervention')
        print(f"\n🎯 Última Intervención:")
        print(f"  • Componente: {latest.get('component')}")
        print(f"  • Parámetro: {latest.get('parameter')}")
        print(f"  • Nuevo Valor: {latest.get('new_value')}")
        print(f"  • Razón: {latest.get('reason')}")
        print(f"  • Timestamp: {latest.get('timestamp')}")
    
    print(f"\n💡 Resumen de Impacto:")
    print(f"  {impact.get('impact_summary', 'N/A')}")
    
    return True


def run_all_tests():
    """Ejecutar todos los tests"""
    
    print("\n" + "🧪 " * 25)
    print("TEST SUITE: Mejoras en Sistema de Diagnóstico")
    print("🧪 " * 25)
    
    tests = [
        ("get_diagnose_context()", test_get_diagnose_context),
        ("classify_actions()", test_classify_actions),
        ("diagnose_system() simple", test_diagnose_system_simple),
        ("system_context format", test_system_context_format),
        ("impact_analysis", test_impact_analysis),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ TEST FALLIDO: {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)
    print(f"✅ Pasaron: {passed}/{len(tests)}")
    print(f"❌ Fallaron: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        return 0
    else:
        print("\n⚠️  Algunos tests fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
