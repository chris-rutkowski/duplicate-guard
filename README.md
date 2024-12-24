
# Duplicate Guard

**Duplicate Guard** is a lightweight GitHub Action designed to prevent duplicate files from being added or modified in a repository. This helps reduce repository bloat, minimize downloadable app sizes, and optimize asset management. Duplicate files can significantly increase the size of compressed artifacts (such as ZIP files) because they are not optimized against themselves during compression. This action ensures your repository remains clean and efficient by detecting and blocking redundant files.

---

## 🚀 Features
- Detects and blocks unintentionally duplicated files in pull requests.
- Helps reduce downloadable app sizes by eliminating redundant assets.
- Supports .gitignore-like syntax to exclude specific files or directories.

---

## 🛠️ Usage

### 1. **Create an Ignore File**
Add a `duplicate_guard.ignore` file to the root of your repository to define patterns for files or directories to exclude from duplicate checks. The syntax follows `.gitignore` conventions.

**Example `duplicate_guard.ignore`:**
```gitignore
test/*
logs/*
*.log
```

---

### 2. **Add the GitHub Action**
Create a GitHub Actions workflow in `.github/workflows/duplicate_guard.yml`:

```yaml
name: Duplicate Guard
on:
  pull_request:
    branches:
      - master
  workflow_dispatch:

jobs:
  filesize_guard:
    runs-on: ubuntu-latest
    steps:
      - name: Duplicate Guard
        uses: chris-rutkowski/duplicate-guard@v1.0.0
```

---

## ⚙️ Configuration

### **Specify a Custom Ignore File Path**
If your `duplicate_guard.ignore` file is not in the root directory, specify its location using the `ignore_file` input:

```yaml
steps:
  - name: Duplicate Guard
    uses: chris-rutkowski/filesize-guard@v1.0.0
      with:
        ignore_file: ./my/path/my_filesize_guard.ignore
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
