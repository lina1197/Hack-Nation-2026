import mlflow
import mlflow.pyfunc
from typing import Dict, Any, List
import json
import time


class IDPExperimentTracker:
    """MLflow integration for tracking IDP agent experiments."""
    
    def __init__(self, experiment_name: str = "virtue-foundation-idp"):
        """
        Initialize experiment tracker.
        
        Args:
            experiment_name: Name of the MLflow experiment
        """
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)
        
    def log_agent_run(
        self,
        query: str,
        response: Dict[str, Any],
        metrics: Dict[str, float] = None
    ) -> str:
        """
        Log an agent run to MLflow.
        
        Args:
            query: User query
            response: Agent response dictionary
            metrics: Optional metrics to log
            
        Returns:
            Run ID
        """
        with mlflow.start_run() as run:
            # Log parameters
            mlflow.log_param("query", query)
            mlflow.log_param("query_type", response.get('analysis', {}).get('query_type', 'unknown'))
            mlflow.log_param("num_citations", len(response.get('citations', [])))
            mlflow.log_param("num_reasoning_steps", len(response.get('reasoning_steps', [])))
            
            # Log metrics
            if metrics:
                for key, value in metrics.items():
                    mlflow.log_metric(key, value)
            
            # Log agent steps as artifacts
            if 'agent_steps' in response:
                steps_json = json.dumps(response['agent_steps'], indent=2)
                mlflow.log_text(steps_json, "agent_steps.json")
            
            # Log citations
            if 'citations' in response:
                citations_json = json.dumps(response['citations'], indent=2)
                mlflow.log_text(citations_json, "citations.json")
            
            # Log full response
            response_json = json.dumps(response, indent=2, default=str)
            mlflow.log_text(response_json, "full_response.json")
            
            # Log response text
            mlflow.log_text(response.get('response', ''), "response.txt")
            
            return run.info.run_id
    
    def log_desert_detection(
        self,
        specialty: str,
        region: str,
        analysis: Dict[str, Any]
    ) -> str:
        """
        Log a medical desert detection run.
        
        Args:
            specialty: Medical specialty analyzed
            region: Region analyzed
            analysis: Desert analysis results
            
        Returns:
            Run ID
        """
        with mlflow.start_run() as run:
            # Log parameters
            mlflow.log_param("analysis_type", "medical_desert_detection")
            mlflow.log_param("specialty", specialty or "all")
            mlflow.log_param("region", region or "all")
            
            # Log metrics
            mlflow.log_metric("total_facilities", analysis.get('total_facilities', 0))
            mlflow.log_metric("specialty_facilities", analysis.get('specialty_facilities', 0))
            mlflow.log_metric("is_desert", 1 if analysis.get('is_medical_desert') else 0)
            
            severity_score = {
                'none': 0,
                'moderate': 1,
                'severe': 2,
                'critical': 3
            }.get(analysis.get('desert_severity', 'none'), 0)
            mlflow.log_metric("desert_severity_score", severity_score)
            
            # Log analysis as artifact
            analysis_json = json.dumps(analysis, indent=2, default=str)
            mlflow.log_text(analysis_json, "desert_analysis.json")
            
            return run.info.run_id
    
    def log_validation_run(
        self,
        facility_name: str,
        validation: Dict[str, Any]
    ) -> str:
        """
        Log a facility validation run.
        
        Args:
            facility_name: Name of validated facility
            validation: Validation results
            
        Returns:
            Run ID
        """
        with mlflow.start_run() as run:
            # Log parameters
            mlflow.log_param("analysis_type", "facility_validation")
            mlflow.log_param("facility_name", facility_name)
            
            # Log metrics
            mlflow.log_metric("completeness_score", validation.get('completeness_score', 0))
            mlflow.log_metric("num_suspicious_claims", len(validation.get('suspicious_claims', [])))
            mlflow.log_metric("num_missing_fields", len(validation.get('missing_critical_fields', [])))
            mlflow.log_metric("num_quality_issues", len(validation.get('data_quality_issues', [])))
            
            # Log validation as artifact
            validation_json = json.dumps(validation, indent=2, default=str)
            mlflow.log_text(validation_json, "validation_report.json")
            
            return run.info.run_id
    
    def compare_runs(self, run_ids: List[str]) -> Dict[str, Any]:
        """
        Compare multiple runs.
        
        Args:
            run_ids: List of run IDs to compare
            
        Returns:
            Comparison results
        """
        runs_data = []
        
        for run_id in run_ids:
            run = mlflow.get_run(run_id)
            runs_data.append({
                'run_id': run_id,
                'params': run.data.params,
                'metrics': run.data.metrics,
                'start_time': run.info.start_time,
                'end_time': run.info.end_time
            })
        
        return {
            'runs': runs_data,
            'num_runs': len(runs_data)
        }