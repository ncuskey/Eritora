# Discord-Wiki Sync System

> A seamless bridge between Discord, Obsidian, and a self-hosted Wiki.

## Overview
This project synchronizes knowledge across three platforms:
1.  **Obsidian (Local)**: The primary editor, backed by Git.
2.  **Wiki (Web)**: A self-hosted MkDocs site that auto-deploys from the repo.
3.  **Discord (Community)**: A bot that allows posting to the wiki and notifies of updates.

## Getting Started

### 1. Prerequisites
- Python 3.8+
- Git

### 2. Local Setup (for editing)
1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the wiki locally:
    ```bash
    mkdocs serve
    ```
    Open http://localhost:8000 to view.

### 3. Obsidian Setup
1.  Open the cloned folder as a Vault in Obsidian.
2.  Install the **Obsidian Git** plugin.
3.  Configure it to auto-backup every X minutes.

## Deployment
The wiki is hosted on a private VM. Updates to the `main` branch trigger a rebuild on the server.
