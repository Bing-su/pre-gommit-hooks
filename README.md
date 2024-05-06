# pre-gommit-hooks

My pre-commit hooks for golang.

## Usage

```yaml
- repo: https://github.com/Bing-su/pre-gommit-hooks
  rev: v2024.05.06
  hooks:
    - id: errcheck
    - id: goimports
    - id: golangci-lint
    - id: gofumpt
```

## See

- https://github.com/lietu/go-pre-commit
