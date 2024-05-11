package cmd

import (
	"github.com/spf13/cobra"
)

func init() {
	errcheck := &cobra.Command{
		Use:   "errcheck [files...]",
		Short: "Run errcheck on go files",
		Run: func(cmd *cobra.Command, args []string) {
			runCmd("errcheck", filterArgs(args)...)
		},
	}

	rootCmd.AddCommand(errcheck)
}
