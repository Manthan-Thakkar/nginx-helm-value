from fastapi import FastAPI, BackgroundTasks
import subprocess
from pydantic import BaseModel

app = FastAPI()

class HelmUpgradeRequest(BaseModel):
    releaseName: str
    chartURL: str
    valuesURL: str

def upgrade_helm(data: HelmUpgradeRequest):
    result = subprocess.run(
        ['helm', 'upgrade', data.releaseName, data.chartURL, '-f', data.valuesURL],
        capture_output=True,
        text=True
    )
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

@app.post("/upgrade")
async def upgrade(
    data: HelmUpgradeRequest,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(upgrade_helm, data)
    return {"acknowledge": True}