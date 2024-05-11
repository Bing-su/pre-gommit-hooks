package cmd

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"slices"
)

func runCmd(bin string, args ...string) {
	c := exec.Command(bin, args...)
	c.Stdout = os.Stdout
	c.Stderr = os.Stderr

	err := c.Run()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error running %s: %s", bin, err)
		os.Exit(1)
	}
}

func pkgNames(paths []string) []string {
	var dirs []string
	for _, path := range paths {
		dir := fmt.Sprintf("./%s", filepath.Dir(path))
		if !slices.Contains(dirs, dir) {
			dirs = append(dirs, dir)
		}
	}
	return dirs
}
