package cmd

import (
	"github.com/spf13/cobra"
)

func init() {
	errcheck := &cobra.Command{
		Use:   "govet [files...]",
		Short: "Run go vet on go files",
		Run: func(cmd *cobra.Command, args []string) {
			args = append([]string{"vet"}, filterArgs(args)...)
			runCmd("go", args...)
		},
	}

	rootCmd.AddCommand(errcheck)
}
