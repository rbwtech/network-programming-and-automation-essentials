package main

import (
	"fmt"
	"os"
	"path/filepath"
	"time"
)

type BackupManager struct {
	BackupDir string
}

func (bm *BackupManager) Backup(deviceName, config string) error {
	timestamp := time.Now().Format("2006-01-02_15-04-05")
	filename := fmt.Sprintf("%s_%s.cfg", deviceName, timestamp)
	path := filepath.Join(bm.BackupDir, filename)
	
	err := os.WriteFile(path, []byte(config), 0644)
	if err != nil {
		return err
	}
	fmt.Printf("Backed up: %s\n", path)
	return nil
}

func main() {
	os.MkdirAll("./backups", 0755)
	manager := &BackupManager{BackupDir: "./backups"}
	
	devices := map[string]string{
		"router-1": "hostname router-1\ninterface eth0\n ip address 192.168.1.1",
		"switch-1": "hostname switch-1\nvlan 10\n name Management",
	}
	
	for name, config := range devices {
		manager.Backup(name, config)
	}
	
	fmt.Println("\nBackup complete. Files saved to ./backups/")
}