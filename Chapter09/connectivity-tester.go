package main

import (
	"fmt"
	"net"
	"time"
)

type ConnectivityTest struct {
	Target  string
	Port    int
	Timeout time.Duration
}

func (ct *ConnectivityTest) TestTCP() (bool, error) {
	address := fmt.Sprintf("%s:%d", ct.Target, ct.Port)
	conn, err := net.DialTimeout("tcp", address, ct.Timeout)
	if err != nil {
		return false, err
	}
	conn.Close()
	return true, nil
}

func main() {
	tests := []ConnectivityTest{
		{"google.com", 80, 5 * time.Second},
		{"google.com", 443, 5 * time.Second},
		{"cloudflare.com", 443, 5 * time.Second},
	}
	
	passCount := 0
	for i, test := range tests {
		success, err := test.TestTCP()
		if success {
			fmt.Printf("%d. PASS - %s:%d\n", i+1, test.Target, test.Port)
			passCount++
		} else {
			fmt.Printf("%d. FAIL - %s:%d (%v)\n", i+1, test.Target, test.Port, err)
		}
	}
	fmt.Printf("\nPassed: %d/%d\n", passCount, len(tests))
}