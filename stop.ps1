# ============================================================
# Asset Management Platform - One-click Stop
# Kill processes listening on backend port 8000 and frontend port 5173
# ============================================================

function Stop-Port($port, $name) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if (-not $conns) {
        Write-Host "[--] $name (port $port) is not running"
        return
    }
    $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($processId in $pids) {
        try {
            Stop-Process -Id $processId -Force -ErrorAction Stop
            Write-Host "[OK] Stopped $name (PID $processId, port $port)" -ForegroundColor Green
        } catch {
            Write-Host "[X] Failed to stop PID $processId : $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

Stop-Port 8000 "Backend FastAPI"
Stop-Port 5173 "Frontend Vite"
