
# Prosty skrypt do backupu bazy danych

$DB_NAME = "app_database"
$BACKUP_DIR = "C:\Backups\db"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$FILENAME = Join-Path $BACKUP_DIR "${DB_NAME}_${DATE}.sql.gz"

# Sprawdź czy katalog istnieje
if (-not (Test-Path -Path $BACKUP_DIR -PathType Container)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
    Write-Host "Utworzono katalog $BACKUP_DIR"
}

# Wykonaj backup
Write-Host "Rozpoczynam backup bazy $DB_NAME..."

# Uruchom mysqldump i przekaż wynik do gzip
try {
    & mysqldump -u root -p $DB_NAME |
        & gzip -c > $FILENAME

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Backup zakończony sukcesem: $FILENAME" -ForegroundColor Green
    }
    else {
        Write-Host "Błąd podczas wykonywania backupu!" -ForegroundColor Red
        Remove-Item $FILENAME -ErrorAction SilentlyContinue
        exit 1
    }
}
catch {
    Write-Host "Wystąpił błąd: $_" -ForegroundColor Red
    Remove-Item $FILENAME -ErrorAction SilentlyContinue
    exit 1
}
