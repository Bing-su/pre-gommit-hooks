package cmd

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"slices"
	"strings"
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

func filterArgs(args []string) []string {
	var result []string
	for _, arg := range args {
		if strings.HasPrefix(arg, "-") {
			result = append(result, arg)
			continue
		}

		dir := fmt.Sprintf("./%s", filepath.Dir(arg))
		if !slices.Contains(result, dir) {
			result = append(result, dir)
		}
	}
	return result
}
