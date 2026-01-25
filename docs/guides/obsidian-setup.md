# Obsidian Setup Guide

This guide explains how to connect your local Obsidian vault to the Eritora Wiki system.

## 1. Install Obsidian
If you haven't already, download [Obsidian](https://obsidian.md).

## 2. Clone the Repository
You need the raw markdown files on your computer.
```bash
git clone https://github.com/ncuskey/Eritora.git Documents/Eritora
```
Open this folder as a **Vault** in Obsidian.

## 3. Install "Obsidian Git"
This plugin handles the synchronization magic.

1. Open Obsidian Settings -> **Community Plugins**.
2. Turn on "Restricted Mode" (if off) to enable plugins.
3. Browse -> Search "Obsidian Git" -> Install -> **Enable**.

## 4. Configuration
1. Open Plugin Settings -> Obsidian Git.
2. **Vault backup interval (minutes)**: Set to `5` or `10`.
3. **Auto backup after file change**: Enable.
4. **Desktop**: Use "Source Control View" (sidebar) to manually sync if needed.

## Workflow
- **Write**: Just write notes normally in Obsidian.
- **Sync**: The plugin auto-commits your changes.
- **Publish**: The Bot detects the commit and rebuilds the website in ~1 minute.

## Troubleshooting
- **Conflict**: If you edit a file that someone else changed, the plugin might pause. Open the Source Control view to resolve conflicts (usually by "Pulling" first).
