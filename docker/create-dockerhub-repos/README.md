# 🐳 Docker Hub Repository Creator

A simple Python CLI tool to **bulk-create Docker Hub repositories** (private or public) using the **official Docker Hub API**.  
Supports authentication via Personal Access Token or password, and allows customization like descriptions, organization namespace, and visibility.

---

## 🚀 Features

✅ Create **multiple repositories** from a list  
✅ Supports **private** (default) and **public** repositories  
✅ Works with both **user** and **organization** namespaces  
✅ Adds **short and full descriptions** automatically  
✅ Uses **modern Docker Hub API v2** with JWT authentication  
✅ Graceful error handling and fallback for legacy endpoints  

---

## 📦 Requirements

- **Python 3.8+**
- `requests` library  
  Install with:
  ```bash
  pip install requests
  ```

---

## ⚙️ Setup

1. **Generate a Docker Hub Access Token**  
   Visit [Docker Hub → Account Settings → Security → Access Tokens](https://hub.docker.com/settings/security).

2. **Create a file** (e.g. `repos.txt`) with one repository name per line:
   ```txt
   api-service
   web-dashboard
   worker
   analytics-engine
   ```
   You can add comments with `#` — these lines will be ignored.

3. **Save the script**  
   Download or copy the file [`create_dockerhub_repos.py`](./create_dockerhub_repos.py) into your working directory.

---

## 🧠 Usage

### Basic Example
```bash
python create_dockerhub_repos.py   --user username   --token $DOCKER_TOKEN   --file repos.txt
```

This will create **private repositories** under your personal namespace.

---

### 🏢 Create under an Organization
```bash
python create_dockerhub_repos.py   --user username   --token $DOCKER_TOKEN   --file repos.txt   --org myorg
```

---

### 🌍 Create Public Repositories
```bash
python create_dockerhub_repos.py   --user username   --token $DOCKER_TOKEN   --file repos.txt   --public
```

---

### 📝 Add Descriptions
```bash
python create_dockerhub_repos.py   --user username   --token $DOCKER_TOKEN   --file repos.txt   --desc "Microservice for Backend API"   --full-desc "This repository contains the backend service for Example Backend APIs."
```

---

## ⚡ How It Works

1. Logs in to Docker Hub using your credentials or token (`/v2/users/login/`)  
2. Obtains a **JWT token** for API authorization  
3. Creates each repository via:
   - `POST /v2/repositories/` (preferred modern endpoint)
   - Falls back to `POST /v2/repositories/{namespace}/` if required  
4. Handles both success and failure cases with detailed logging  

---

## 🧩 CLI Arguments

| Flag | Description | Required | Default |
|------|--------------|-----------|----------|
| `--user` | Docker Hub username | ✅ | — |
| `--token` | Docker Hub access token or password | ✅ | — |
| `--file` | Path to file with repository names | ✅ | — |
| `--org` | Namespace or organization name | ❌ | `<username>` |
| `--public` | Create public repositories | ❌ | Private |
| `--desc` | Short description | ❌ | — |
| `--full-desc` | Full repository description | ❌ | — |

---

## 🔐 Authentication Notes

- **Recommended:** Use a **Docker Hub Access Token** (not your password).  
- The script exchanges it for a **JWT token** to interact with the Hub API.  
- If your token has limited scopes, ensure it includes `repo:write` permissions.

---

## 📚 References

- [Docker Hub REST API Reference](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/operation/CreateRepository)
- [Docker Hub Authentication](https://docs.docker.com/reference/api/hub/latest/#tag/users/operation/LoginUser)
- [Docker Hub API Deprecated Endpoints](https://docs.docker.com/reference/api/hub/deprecated/)
