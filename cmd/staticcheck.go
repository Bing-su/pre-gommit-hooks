package cmd

import (
	"github.com/spf13/cobra"
)

func init() {
	staticcheck := &cobra.Command{
		Use:   "staticcheck [files...]",
		Short: "Run staticcheck on go files",
		Run: func(cmd *cobra.Command, args []string) {
			runCmd("staticcheck", filterArgs(args)...)
		},
	}

	rootCmd.AddCommand(staticcheck)
}
