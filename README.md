# ClamAV Email Gateway EICAR Lab

A small Docker-based email gateway lab that scans incoming email with ClamAV and demonstrates rejecting the harmless EICAR antivirus test file.

## Architecture

`send.py` sends email to the gateway on port `2525`. The gateway scans each message with ClamAV; clean mail is forwarded to Mailpit, while infected mail receives a `554` rejection.

Mailpit's inbox is available at <http://localhost:8025>.

EICAR is a harmless, industry-standard antivirus test string, not real malware. On first start, ClamAV can take 1 to 2 minutes to become healthy.

## Prerequisites

- Docker Desktop

## Run (PowerShell)

```powershell
docker compose up -d --wait
docker compose ps
docker compose exec gateway python send.py show
docker compose exec gateway python send.py
docker compose exec gateway python send.py eicar
docker compose logs gateway | findstr CLAMAV
docker compose logs clamav | findstr FOUND
docker compose down
```
