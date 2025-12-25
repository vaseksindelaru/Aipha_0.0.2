import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock
from core.orchestrator import CentralOrchestrator
from core.change_proposer import ChangeProposal

class TestFullIntegration:
    @pytest.fixture
    def workspace(self):
        """Crea un entorno de trabajo temporal aislado."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # Estructura básica
            (root / "memory").mkdir()
            (root / "core").mkdir()
            
            # Archivo de configuración dummy
            config_path = root / "memory" / "aipha_config.json"
            config_path.write_text("{}")
            
            yield root

    @pytest.fixture
    def dummy_component(self, workspace):
        """Crea un componente dummy para ser modificado."""
        component_path = workspace / "core" / "dummy_component.py"
        component_path.write_text("class Dummy:\n    def __init__(self):\n        self.value = 100\n")
        
        # Crear también un test dummy para que el AtomicUpdateSystem lo pase
        test_path = workspace / "tests" / "test_dummy.py"
        test_path.parent.mkdir(exist_ok=True)
        test_path.write_text("def test_dummy():\n    assert True\n")
        
        return component_path, test_path

    def test_closed_loop_self_correction(self, workspace, dummy_component, monkeypatch):
        """
        Simula un ciclo completo de auto-corrección:
        1. Orchestrator detecta métricas (simulado).
        2. Proposer genera propuesta (mockeado para apuntar al dummy).
        3. Evaluator aprueba.
        4. AtomicSystem aplica el cambio.
        5. Se verifica persistencia.
        """
        component_path, test_path = dummy_component
        
        # Inicializar Orchestrator en el workspace temporal
        orchestrator = CentralOrchestrator(storage_root=workspace / "memory")
        
        # Mockear ChangeProposer para que devuelva una propuesta controlada
        # que apunte a nuestro componente dummy en el workspace temporal
        
        # El target_component debe ser importable o manejable por AtomicUpdateSystem.
        # AtomicUpdateSystem usa: Path(proposal.target_component.replace(".", "/") + ".py")
        # Así que necesitamos construir un target_component que resuelva a component_path
        
        # Truco: AtomicUpdateSystem usa rutas relativas desde el CWD.
        # En este test, el CWD es el real (/home/vaclav/Aipha_0.0.2).
        # Pero nuestro componente está en /tmp/...
        # Para que AtomicUpdateSystem lo encuentre, necesitamos que target_path sea absoluto o relativo correcto.
        # AtomicUpdateSystem implementación actual: self.target_path = Path(...)
        # Si le pasamos una ruta absoluta en target_component (hack), funcionará si replace no la rompe.
        # Mejor opción: Monkeypatch AtomicUpdateSystem.execute para que use la ruta correcta o
        # Monkeypatch ChangeProposer para devolver una propuesta con la ruta absoluta "disfrazada".
        
        # Vamos a modificar la propuesta para que target_component sea la ruta absoluta sin extensión
        # AtomicUpdateSystem hace: Path(target_component.replace(".", "/") + ".py")
        # Si target_component es "/tmp/foo/bar", replace no hace nada malo, y + ".py" lo completa.
        target_component_str = str(component_path.with_suffix(""))
        
        def mock_propose_changes(lookback_days=7):
            # Registrar la acción como lo haría el ChangeProposer real
            orchestrator.sentinel.add_action(
                agent="ChangeProposer",
                action_type="PROPOSAL_GENERATED",
                proposal_id="INTEGRATION-TEST-001",
                details={"title": "Fix Dummy Component"}
            )
            return [
                ChangeProposal(
                    proposal_id="INTEGRATION-TEST-001",
                    title="Fix Dummy Component",
                    target_component=target_component_str,
                    impact_justification="Integration Test",
                    estimated_difficulty="Low",
                    diff_content="-         self.value = 100\n+         self.value = 200",
                    test_plan=f"pytest {test_path}",
                    metrics={"expected_improvement": 0.5},
                    priority="critical",
                    estimated_complexity="trivial"
                )
            ]
        
        monkeypatch.setattr(orchestrator.proposer, "propose_changes", mock_propose_changes)
        
        # Ejecutar el ciclo
        result = orchestrator.run_improvement_cycle()
        
        # Verificaciones
        
        # 1. El ciclo terminó correctamente
        assert result["proposals_generated"] == 1
        assert result["proposals_approved"] == 1
        assert result["changes_applied"] == 1
        
        # 2. El archivo fue modificado (Fase 3)
        content = component_path.read_text()
        assert "self.value = 200" in content
        assert "self.value = 100" not in content
        
        # 3. La memoria registró todo (Fase 1)
        history = orchestrator.sentinel.get_action_history()
        
        # Buscar eventos clave
        actions = [h["action_type"] for h in history]
        assert "PROPOSAL_GENERATED" in actions
        assert "PROPOSAL_EVALUATED" in actions
        assert "ATOMIC_COMMIT" in actions
        assert "improvement_cycle_completed" in actions
        
        # Verificar detalles de la evaluación (Fase 2)
        eval_event = next(h for h in history if h["action_type"] == "PROPOSAL_EVALUATED")
        assert eval_event["details"]["approved"] is True
