package main

import (
	"fmt"
	"net"
	"sync"
	"time"
)

type DiscoveredDevice struct {
	IPAddress string
	IsActive  bool
	Latency   time.Duration
}

func ScanIP(ip string, timeout time.Duration) DiscoveredDevice {
	start := time.Now()
	conn, err := net.DialTimeout("tcp", ip+":22", timeout)
	latency := time.Since(start)
	
	device := DiscoveredDevice{
		IPAddress: ip,
		Latency:   latency,
		IsActive:  err == nil,
	}
	if conn != nil {
		conn.Close()
	}
	return device
}

func main() {
	ips := []string{"192.168.1.1", "192.168.1.2", "192.168.1.3"}
	var wg sync.WaitGroup
	results := make(chan DiscoveredDevice, len(ips))
	
	for _, ip := range ips {
		wg.Add(1)
		go func(ip string) {
			defer wg.Done()
			results <- ScanIP(ip, 1*time.Second)
		}(ip)
	}
	
	go func() {
		wg.Wait()
		close(results)
	}()
	
	activeCount := 0
	for device := range results {
		if device.IsActive {
			fmt.Printf("Active: %s (latency: %v)\n", 
				device.IPAddress, device.Latency)
			activeCount++
		}
	}
	fmt.Printf("\nActive devices: %d/%d\n", activeCount, len(ips))
}