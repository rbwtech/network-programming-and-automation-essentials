package main

import (
	"fmt"
	"math/rand"
	"time"
)

type NetworkCondition struct {
	Latency    time.Duration
	PacketLoss float64
	Jitter     time.Duration
}

type NetworkEmulator struct {
	Condition NetworkCondition
}

func (ne *NetworkEmulator) SendPacket(data string) (string, error) {
	if rand.Float64()*100 < ne.Condition.PacketLoss {
		return "", fmt.Errorf("packet dropped")
	}
	time.Sleep(ne.Condition.Latency)
	return fmt.Sprintf("ACK: %s", data), nil
}

func main() {
	conditions := []NetworkCondition{
		{Latency: 10 * time.Millisecond, PacketLoss: 0.1},
		{Latency: 200 * time.Millisecond, PacketLoss: 10.0},
		{Latency: 500 * time.Millisecond, PacketLoss: 30.0},
	}
	
	for _, cond := range conditions {
		emulator := &NetworkEmulator{Condition: cond}
		success := 0
		for i := 0; i < 10; i++ {
			if _, err := emulator.SendPacket(fmt.Sprintf("Packet-%d", i+1)); err == nil {
				success++
			}
		}
		fmt.Printf("Latency: %v, Loss: %.1f%% - Success: %d/10\n",
			cond.Latency, cond.PacketLoss, success)
	}
}