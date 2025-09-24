Write-Host "Activando el entorno virtual para PowerShell..."
. .\venv\Scripts\Activate.ps1
Write-Host "Entorno virtual activado. Usa 'deactivate' para salir."
Write-Host "Entorno virtual activado. Usa 'uvicorn main:app --reload --port 4000' iniciar el servidor."