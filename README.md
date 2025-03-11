# pre-gommit-hooks

My pre-commit hooks for golang.

## Usage

```yaml
- repo: https://github.com/Bing-su/pre-gommit-hooks
  rev: v2025.03.11
  hooks:
    - id: errcheck
    - id: goimports
    - id: golangci-lint
    - id: gofumpt
    - id: staticcheck
    - id: gofmt
    - id: govet
    - id: gofix
```

## See

- https://github.com/lietu/go-pre-commit