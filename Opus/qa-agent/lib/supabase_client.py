from datetime import datetime, timezone
from supabase import create_client

SUPABASE_URL = "https://bvqvmpqfibhrfpnngkim.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ2cXZtcHFmaWJocmZwbm5na2ltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5MDI3MzcsImV4cCI6MjA4OTQ3ODczN30.palzFFHUj4aXabw5HmalBPmJZUYEvz8GqJLq1cuyvBY"

client = create_client(SUPABASE_URL, SUPABASE_KEY)


def create_run(app_name, app_url, triggered_by="manual"):
    data = {
        "app_name": app_name,
        "app_url": app_url,
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "warnings": 0,
        "skipped": 0,
        "status": "running",
        "duration_ms": 0,
        "triggered_by": triggered_by,
    }
    result = client.table("qa_runs").insert(data).execute()
    return result.data[0]["id"]


def add_result(run_id, test_result):
    data = {
        "run_id": run_id,
        "category": test_result.category,
        "test_name": test_result.test_name,
        "status": test_result.status,
        "severity": test_result.severity,
        "message": test_result.message,
        "details": test_result.details,
        "duration_ms": test_result.duration_ms,
    }
    client.table("qa_results").insert(data).execute()


def complete_run(run_id, total, passed, failed, warnings, skipped, duration_ms):
    status = "passed" if failed == 0 and warnings == 0 else "failed" if failed > 0 else "warning"
    data = {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "skipped": skipped,
        "duration_ms": duration_ms,
        "status": status,
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    client.table("qa_runs").update(data).eq("id", run_id).execute()
