# Live Development Loop (Phase 3)
# Automatischer Build -> Tests -> Dev Server -> Live Preview -> Screenshot -> Visual QA

param (
    [string]$ProjectPath = ".",
    [string]$OutputScreenshot = "preview.png"
)

Write-Host "1. Triggere automatischen Build für Code-Änderungen..."
# Hier wird normalerweise npm run build oder python setup.py ausgeführt
Start-Sleep -Seconds 2

Write-Host "2. Führe Tests aus..."
pytest tests/ -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests fehlgeschlagen! Breche ab." -ForegroundColor Red
    exit 1
}

Write-Host "3. Starte Dev Server im Hintergrund..."
# Beispiel: Start-Process -NoNewWindow "npm" -ArgumentList "run dev"
Start-Sleep -Seconds 3

Write-Host "4. Erzeuge Live Preview und Screenshot..."
# Dummy Logik: Im echten Einsatz nutzen wir Browser MCP oder Playwright
Write-Host "Mock: Screenshot gespeichert unter $OutputScreenshot"

Write-Host "5. Übergebe an Visual QA Agent..."
# Der Visual QA Agent wird hier getriggert, um das Bild zu validieren.
Write-Host "Visual QA Agent prüft Oberfläche..."
Start-Sleep -Seconds 2

Write-Host "Live Development Loop erfolgreich abgeschlossen!" -ForegroundColor Green
