package cmd

import (
	"github.com/spf13/cobra"
)

func init() {
	errcheck := &cobra.Command{
		Use:   "errcheck [files...]",
		Short: "Run errcheck on go files",
		Run: func(cmd *cobra.Command, args []string) {
			runCmd("errcheck", pkgNames(args)...)
		},
	}

	rootCmd.AddCommand(errcheck)
}
