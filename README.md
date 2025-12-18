# Network Programming and Automation Essentials (Chapters 04–10)

## 📚 Ringkasan Chapter

### Chapter 04 – Network Device Access

- Akses perangkat jaringan menggunakan berbagai metode:
  - **SSH / vSSH**: Remote command execution
  - **Scrapligo**: Multi-vendor automation
  - **SNMP**: Monitoring & telemetry
- File penting:
  - `Adelaide_router_config.txt`, `Brisbane_router_config.txt`, `Sydney_router_config.txt`
  - `cisco_template_go.txt`, `config_render.go`
  - `router_definitions.yaml`

### Chapter 05 – Template-Based Configuration

- Template-based configuration untuk vendor-agnostic automation.
- Fitur:
  - Template Go untuk generate konfigurasi otomatis
  - Mempermudah deploy ke banyak perangkat
- File penting: `naming_conventions.go`

### Chapter 06 – Error Handling & Logging

- Pentingnya error handling dan logging untuk production reliability.
- File penting:
  - `go-gomiko-example.go`, `gosnmp-example.go`
  - `scrapligo-example.go`, `ssh-example.go`, `vssh-example.go`
  - `logrus-logging.go`, `standard-logging.go`, `standard-logging-5-sev-levels.go`

### Chapter 07 – Concurrency & Scaling

- **Vertical vs Horizontal Scaling**:
  - Vertikal: tambah CPU/memori
  - Horizontal: tambah instance/service
- **Goroutines**: eksekusi paralel ringan di Go
- File penting:
  - `panic-example.go`, `panic-example-with-defer.go`
  - `division-by-zero-panic.go`, `division-by-zero-panic-recover.go`
  - `error-library-fmt-division.go`, `error-library-error-division.go`
  - `move-file-example.go`, `two.txt`

### Chapter 08 – ICMP Probe & Parallel Operations

- Microservice ICMP probe untuk cek latency target jaringan.
- Dockerfile dan Docker Compose untuk scaling horizontal.
- File penting:
  - `icmp-probe-service.go`, `dockerfile`, `docker-compose.yaml`
  - `goroutine-icmp-probe.go`, `goroutine-icmp-probe-wg-sync.go`
  - `parallelism.go`
- Contoh menjalankan:

```bash
# Build Docker image
docker build -t probe-service .

# Jalankan single instance
docker run -p 9900:9900 probe-service

# Scaling dengan Docker Compose
docker compose up

# Test endpoint
curl "http://localhost:9001/latency?target=8.8.8.8&target=1.1.1.1"
curl "http://localhost:9002/latency?target=8.8.4.4&target=1.0.0.1"
```

### Chapter 09 – Testing & Validation

- Validasi automation sebelum production.
- File penting:

  - `connectivity-tester.go`
  - `network-emulator.go`
  - `topology-validator.go`

### Chapter 10 – Kesimpulan dan Saran

- Go cocok untuk network automation: concurrency & performance tinggi.
- Template-based config management efektif dan scalable.
- Goroutines meningkatkan performa hingga 100x.
- Error handling, logging, dan testing sangat penting.
- File penting:

  - `config-backup.go`, `device-discovery.go`
  - `ip-config-automation.go`, `link-checker.go`
