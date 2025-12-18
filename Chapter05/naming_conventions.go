package main

import (
	"fmt"
	"strings"
)

// Good: Descriptive variable names
var networkDeviceHostname string = "router-core-01"
var maximumRetryAttempts int = 3
var connectionTimeoutSeconds int = 30

// Good: Function with clear naming
func ValidateIPAddress(ipAddress string) bool {
	parts := strings.Split(ipAddress, ".")
	if len(parts) != 4 {
		return false
	}
	return true
}

// Good: Struct with clear field names
type NetworkDevice struct {
	Hostname        string
	IPAddress       string
	ManagementPort  int
	DeviceType      string
	LastHealthCheck string
}

// Good: Constants with descriptive names
const (
	DefaultSSHPort       = 22
	DefaultTelnetPort    = 23
	MaxConnectionRetries = 5
	ConnectionTimeout    = 60
)

func main() {
	device := NetworkDevice{
		Hostname:       "core-router-01",
		IPAddress:      "192.168.1.1",
		ManagementPort: DefaultSSHPort,
		DeviceType:     "Cisco IOS",
	}

	fmt.Println("Device Configuration:")
	fmt.Printf("Hostname: %s\n", device.Hostname)
	fmt.Printf("IP Address: %s\n", device.IPAddress)
	fmt.Printf("Port: %d\n", device.ManagementPort)
	
	if ValidateIPAddress(device.IPAddress) {
		fmt.Println("IP Address is valid")
	}
}