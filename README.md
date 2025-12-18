# Network Programming and Automation Essentials (Chapters 04–11) + Socket-App

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

### Chapter 11 – Socket Programming

- Dasar socket programming dengan Python.
- TCP & UDP client-server, echo server, SNTP client, socket error handling.
- File penting:

  - `11_1_local_machine_info.py`
  - `11_2_remote_machine_info.py`
  - `11_3_ip4_address_conversion.py`
  - `11_4_finding_service_name.py`
  - `11_5_integer_conversion.py`
  - `11_6_socket_timeout.py`
  - `11_7_socket_errors.py`
  - `11_8_modify_buff_size.py`
  - `11_9_socket_modes.py`
  - `11_10_reuse_socket_address.py`
  - `11_11_print_machine_time.py`
  - `11_12_sntp_client.py`
  - `11_13a_echo_server.py`
  - `11_13b_echo_client.py`
  - `11_14a_echo_server_udp.py`
  - `11_14b_echo_client_udp.py`

### Socket-App

- Project Python untuk chat app berbasis socket dan UDP.
- Struktur folder:

  ```
  main.py
  network/
      udp_client.py
      message_handler.py
  ui/
      chat_window.py
      components.py
  utils/
      helpers.py
  ```

- Fitur:

  - GUI chat window
  - UDP client-server messaging
  - Message handling & helper utilities
