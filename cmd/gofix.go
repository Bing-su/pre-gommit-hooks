package cmd

import (
	"github.com/spf13/cobra"
)

func init() {
	gofix := &cobra.Command{
		Use:   "govet [files...]",
		Short: "Run go fix on go files",
		Run: func(cmd *cobra.Command, args []string) {
			args = append([]string{"fix"}, filterArgs(args)...)
			runCmd("go", args...)
		},
	}

	rootCmd.AddCommand(gofix)
}
