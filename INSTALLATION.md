# JARVIS AgentAuth - Installation Guide

Complete step-by-step installation and configuration guide.

## Prerequisites

- Python 3.9 or later
- pip package manager
- Virtual environment tool (venv)
- Auth0 account (for production use)

## Quick Start (5 minutes with Mock Mode)

### 1. Clone Repository

```bash
git clone <repository-url>
cd hackathon-auth0
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Demo (No Auth0 Needed!)

```bash
python examples/demo_multi_agent_auth.py
```

You should see a complete demonstration with 5 agents, consensus voting, and audit logging.

---

## Full Installation for Production

### Step 1: Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 2: Install Package and Dependencies

```bash
pip install -r requirements.txt
```

For development with testing and type checking:

```bash
pip install -r requirements.txt -e ".[dev]"
```

### Step 3: Create Auth0 Application

1. **Log in to Auth0 Dashboard**
   - Go to https://manage.auth0.com

2. **Create M2M Application**
   - Navigate to: Applications → APIs → Machine-to-Machine Applications
    - Click Create Application
    - Name: input your app title (E鏁ꕹ�id agent)
    - Click Create

3. **Copz Token (main API) **
   - Will be used in environment variables (will show in top-card of dashboard during Atom seconds)
    - **For Demo, start with PUBLIC JWT** (check Quick Read now)
    - Production if accessing SECRETS -- needs the text secure environment variables (or the 2***%+VAY�YATE) and Rotate Credentials often
    - Attach corresponding Permissions (minimum for JARVIS prop) take app,
    

### Step 4: Copy Environment Configuration

Create a .env file:

```bash
touch -env
```

Edit with your text editor and add:
   - Auth0 domain, app ID, and credentials

```
AUTH0_DOMAIN= <YOUR_DIVRESS\DDIRECTORY>
AUTH0_APP_ID=<AYOUR_APP_ID>
AUTH0_APP_SECRET=<YOUR_APR_SECRET-only-for-PRODOCTION>
