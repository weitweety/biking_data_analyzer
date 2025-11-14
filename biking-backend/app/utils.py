import requests
import logging
import os
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


def _get_airflow_config() -> Tuple[str, Optional[Tuple[str, str]]]:
	"""Resolve Airflow base URL and optional basic auth creds from env."""
	airflow_url = os.getenv("AIRFLOW_URL", "http://localhost:8080").rstrip("/")
	username = os.getenv("AIRFLOW_USERNAME")
	password = os.getenv("AIRFLOW_PASSWORD")
	auth = (username, password) if username and password else None
	return airflow_url, auth


def trigger_airflow_dag(dag_id: str = "etl_pipeline", airflow_url: Optional[str] = None) -> Dict[str, Any]:
	"""
	Trigger an Airflow DAG manually via the stable REST API.
	Honors env vars: AIRFLOW_URL, AIRFLOW_USERNAME, AIRFLOW_PASSWORD.
	"""
	try:
		base_url, auth = _get_airflow_config() if airflow_url is None else (airflow_url.rstrip("/"), None)
		url = f"{base_url}/api/v1/dags/{dag_id}/dagRuns"

		headers = {
			"Content-Type": "application/json",
			"Accept": "application/json",
		}

		data = {
			"conf": {},
			"dag_run_id": f"manual_trigger_{int(__import__('time').time())}",
		}

		resp = requests.post(url, json=data, headers=headers, auth=auth, timeout=10)
		if resp.status_code in (200, 201):
			logger.info("Successfully triggered DAG %s", dag_id)
			return {"status": "success", "message": f"DAG {dag_id} triggered", "response": resp.json() if resp.content else {}}

		logger.error("Failed to trigger DAG %s: %s - %s", dag_id, resp.status_code, resp.text)
		return {"status": "error", "message": f"Failed to trigger DAG: HTTP {resp.status_code}", "details": resp.text}

	except Exception as e:
		logger.error("Error triggering DAG %s: %s", dag_id, str(e))
		return {"status": "error", "message": f"Error triggering DAG: {str(e)}"}


def check_airflow_health(airflow_url: Optional[str] = None) -> Dict[str, Any]:
	"""
	Check Airflow health endpoint. Returns unhealthy with details on failures.
	"""
	try:
		base_url, auth = _get_airflow_config() if airflow_url is None else (airflow_url.rstrip("/"), None)
		url = f"{base_url}/api/v1/health"
		resp = requests.get(url, auth=auth, timeout=5)
		if resp.status_code == 200:
			return {"status": "healthy", "airflow_url": base_url, "details": resp.json()}
		return {"status": "unhealthy", "airflow_url": base_url, "error": resp.text, "code": resp.status_code}
	except Exception as e:
		return {"status": "unhealthy", "airflow_url": airflow_url or os.getenv("AIRFLOW_URL", "http://localhost:8080"), "error": str(e)}
