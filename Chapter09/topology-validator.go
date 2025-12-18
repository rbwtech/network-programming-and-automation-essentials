package main

import "fmt"

type Device struct {
	Name       string
	Interfaces []Interface
}

type Interface struct {
	Name      string
	IPAddress string
	Connected bool
}

func ValidateTopology(devices []Device) []string {
	var issues []string
	ipMap := make(map[string][]string)
	
	for _, device := range devices {
		for _, iface := range device.Interfaces {
			if iface.IPAddress != "" {
				ipMap[iface.IPAddress] = append(ipMap[iface.IPAddress], 
					fmt.Sprintf("%s:%s", device.Name, iface.Name))
			}
			if !iface.Connected {
				issues = append(issues, 
					fmt.Sprintf("Disconnected: %s:%s", device.Name, iface.Name))
			}
		}
	}
	
	for ip, devs := range ipMap {
		if len(devs) > 1 {
			issues = append(issues, fmt.Sprintf("Duplicate IP %s: %v", ip, devs))
		}
	}
	return issues
}

func main() {
	devices := []Device{
		{Name: "Router-1", Interfaces: []Interface{
			{Name: "eth0", IPAddress: "10.0.0.1/24", Connected: true},
			{Name: "eth1", IPAddress: "192.168.1.1/24", Connected: false},
		}},
		{Name: "Router-2", Interfaces: []Interface{
			{Name: "eth0", IPAddress: "10.0.0.2/24", Connected: true},
		}},
	}
	
	issues := ValidateTopology(devices)
	if len(issues) == 0 {
		fmt.Println("No issues found")
	} else {
		for _, issue := range issues {
			fmt.Println("Warning:", issue)
		}
	}
}