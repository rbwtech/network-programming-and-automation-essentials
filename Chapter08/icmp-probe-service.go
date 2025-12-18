package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
	probing "github.com/prometheus-community/pro-bing"
)

func main() {
	listen := ":9900"
	if port, ok := os.LookupEnv("PORT"); ok {
		listen = ":" + port
	}
	http.HandleFunc("/latency", probeTargets)
	log.Fatal(http.ListenAndServe(listen, nil))
}

func probeTargets(w http.ResponseWriter, r *http.Request) {
	targetList := r.URL.Query()["target"]
	if len(targetList) == 0 {
		fmt.Fprintf(w, "no targets specified\n")
		return
	}
	if len(targetList) > 1000 {
		fmt.Fprintf(w, "too many targets, max is 1000\n")
		return
	}

	var wg sync.WaitGroup
	for _, target := range targetList {
		wg.Add(1)
		go probe(w, target, &wg)
	}
	wg.Wait()
}

func probe(w http.ResponseWriter, host string, wg *sync.WaitGroup) {
	defer wg.Done()

	p, err := probing.NewPinger(host)
	if err != nil {
		fmt.Fprintf(w, "error creating pinger: %v\n", err)
		return
	}
	p.Count = 1
	p.Timeout = time.Second * 2
	p.SetPrivileged(true)

	if err := p.Run(); err != nil {
		fmt.Fprintf(w, "error running ping: %v\n", err)
		return
	}

	stats := p.Statistics()
	if stats.PacketLoss == 0 {
		fmt.Fprintf(w, "%s latency is %s\n", host, stats.AvgRtt)
	} else {
		fmt.Fprintf(w, "%s no response\n", host)
	}
}
