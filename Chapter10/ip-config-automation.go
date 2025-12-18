package main

import (
	"fmt"
	"strings"
)

type IPConfig struct {
	Interface  string
	IPAddress  string
	SubnetMask string
}

func GenerateCiscoConfig(hostname string, configs []IPConfig) string {
	var config strings.Builder
	config.WriteString(fmt.Sprintf("hostname %s\n!\n", hostname))
	for _, cfg := range configs {
		config.WriteString(fmt.Sprintf("interface %s\n", cfg.Interface))
		config.WriteString(fmt.Sprintf(" ip address %s %s\n", 
			cfg.IPAddress, cfg.SubnetMask))
		config.WriteString(" no shutdown\n!\n")
	}
	return config.String()
}

func main() {
	configs := []IPConfig{
		{"GigabitEthernet0/0", "192.168.1.1", "255.255.255.0"},
		{"GigabitEthernet0/1", "10.0.0.1", "255.255.255.252"},
	}
	
	ciscoConfig := GenerateCiscoConfig("router-core-01", configs)
	fmt.Println("=== Cisco Configuration ===")
	fmt.Println(ciscoConfig)
}