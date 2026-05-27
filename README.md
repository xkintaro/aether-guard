<a href="README.md">
  <img src="https://img.shields.io/badge/Language-English-blue?style=flat-square&logo=google-translate&logoColor=white" alt="English">
</a>
<a href="README-TR.md">
  <img src="https://img.shields.io/badge/Dil-Türkçe-red?style=flat-square&logo=google-translate&logoColor=white" alt="Türkçe">
</a>

  <br />
  <br />

<div align="center">
  <img src="logo.png" width="120" height="120">
  <br />
  <br />

  <p>
    A sleek, lightweight, and simple folder protection tool for Windows.
  </p>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

  <p>
    <a href="#features">Features</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a> •
    <a href="#configuration">Configuration</a> •
    <a href="#license">License</a> 
  </p>

  <br />
  <br />
</div>

## 📋 About

**Aether Guard** is a sleek, modern, and lightweight folder protection utility for Windows. It provides an additional layer of security by monitoring active Windows Explorer windows and requiring password authentication to access them.

<img src="md/20260312140807256.jpg" width="auto" />

## ✨ Features <a id="features"></a>

- **Real-time Protection**: Actively monitors Windows Explorer and closes unauthorized windows instantly.
- **Anti-Brute Force**: Sophisticated rate-limiting system that implements exponential backoff after failed attempts.
- **Session Grace Period**: Stay authenticated for a configurable amount of time (default: 5 minutes) without needing to re-enter your key.
- **Single Instance Enforcement**: Automatically detects if the application is already running to prevent redundant processes.
- **Stealthy Execution**: Support for VBS startup to run without a visible console window.

## 🚀 Installation <a id="installation"></a>

### Requirements

- **OS**: Windows 10/11 (Required for Windows API integration)
- **Python**: Version 3.8 or higher

### Installation

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/xkintaro/aether-guard.git
    cd aether-guard
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**

    ```bash
    python app.py
    ```

## ⚒️ Usage <a id="usage"></a>

1.  **Launch the Application**:
    - Run `run.bat` for a console-attached session.
    - Run `run-aether-guard.vbs` to start in the background.
2.  **Authentication**:
    - **Default Password**: `1234`
    - When you try to open a folder, a modern UI will prompt for your access key.
3.  **To Close**:
    - If running in a console, press `Ctrl+C`.
    - Otherwise, end the process via Task Manager.

## ⚙️ Configuration <a id="configuration"></a>

Open `app.py` to modify the `Config` class settings:

```python
class Config:
    DEFAULT_PASSWORD = "1234"    # Your master access key
    MAX_ATTEMPTS = 5             # Attempts allowed before lockout
    LOCKOUT_TIME = 60            # Initial lockout duration in seconds
    GRACE_PERIOD = 300           # Authorized session duration (5 mins)
```

## 📄 License <a id="license"></a>

This project is licensed under the MIT License. You can check the [LICENSE](LICENSE) file for details.

#

<p align="center">
  <sub>❤️ Developed by "Mustafa TAŞAL" (kintaro)</sub>
</p>