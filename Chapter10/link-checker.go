package main

import (
	"fmt"
	"net"
	"time"
)

type Link struct {
	Source      string
	Destination string
	Port        int
}

func CheckLink(link Link) (bool, time.Duration) {
	address := fmt.Sprintf("%s:%d", link.Destination, link.Port)
	start := time.Now()
	conn, err := net.DialTimeout("tcp", address, 2*time.Second)
	latency := time.Since(start)
	
	if conn != nil {
		conn.Close()
	}
	return err == nil, latency
}

func main() {
	links := []Link{
		{"router-1", "google.com", 80},
		{"router-1", "cloudflare.com", 443},
		{"switch-1", "192.168.1.1", 22},
	}
	
	upCount := 0
	for _, link := range links {
		status, latency := CheckLink(link)
		if status {
			fmt.Printf("UP - %s -> %s:%d (latency: %v)\n",
				link.Source, link.Destination, link.Port, latency)
			upCount++
		} else {
			fmt.Printf("DOWN - %s -> %s:%d\n",
				link.Source, link.Destination, link.Port)
		}
	}
	fmt.Printf("\nSummary: %d Up, %d Down\n", upCount, len(links)-upCount)
}