package cmd

import (
	"github.com/spf13/cobra"
)

func init() {
	golangciLint := &cobra.Command{
		Use:   "golangci-lint [files...]",
		Short: "Run golangci-lint on go files",
		Run: func(cmd *cobra.Command, args []string) {
			args = append([]string{"run"}, filterArgs(args)...)
			runCmd("golangci-lint", args...)
		},
	}

	rootCmd.AddCommand(golangciLint)
}
