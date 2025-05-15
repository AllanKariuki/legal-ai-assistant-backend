# 🚀 FastAPI Project Setup Instructions

## 📦 Requirements

- Python 3.8+
- pip (Python package manager)
- Git (for cloning the repo)
- (Optional) Docker & Docker Compose

---

## 🧰 Step-by-Step Setup

### 1. 📁 Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. 🧪 Create and Activate a Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. 📥 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt

```


### 4. ⚙️ Environment Variables (Optional)
Register your LLM API key as below
```bash
LLM_API_KEY=your_api_key
```

### 5. 🚀 Run the Development Server
```bash
Copy
Edit
uvicorn main:app --reload
main:app refers to your FastAPI entry point (main.py, and the FastAPI app inside it).

--reload enables hot-reloading during development.

Open your browser at: (http://127.0.0.1:8000)
```

### 6. 📚 API Docs
FastAPI automatically generates documentation:

- Swagger UI: (http://127.0.0.1:8000/docs)

- ReDoc: (http://127.0.0.1:8000/redoc)