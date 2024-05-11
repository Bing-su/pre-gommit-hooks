package cmd

import (
	"github.com/spf13/cobra"
)

func init() {
	gofmt := &cobra.Command{
		Use:   "gofmt [files...]",
		Short: "Run go fmt on go files",
		Run: func(cmd *cobra.Command, args []string) {
			args = append([]string{"fmt"}, filterArgs(args)...)
			runCmd("go", args...)
		},
	}

	rootCmd.AddCommand(gofmt)
}
