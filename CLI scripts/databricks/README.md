# Azure Databricks CLI scripts

This folder contains PowerShell helper scripts to connect to and inspect an Azure Databricks workspace. They follow the style used in the repository's other CLI scripts and load connection details from a top-level `.env` file.

Files added:

- `connect_databricks.ps1` — loads `.env`, authenticates using a service principal if `CLIENT_ID`/`CLIENT_SECRET` are provided; otherwise prompts interactive login. Looks up the Databricks workspace and opens the workspace URL in your default browser. Also sets `DATABRICKS_HOST` (process scope).
- `get_databricks_workspace.ps1` — loads `.env`, sets subscription context and writes the workspace resource JSON to `./<workspaceName>_workspace.json` in this folder.
- `.env.example` — example environment file showing required variables.

Usage

1. Copy `.env.example` to a file named `.env` in the repository root (one level above this folder) and fill in values.
2. From PowerShell run:

   .\"CLI scripts\databricks\connect_databricks.ps1"

   or

   .\"CLI scripts\databricks\get_databricks_workspace.ps1"

Notes

- These scripts assume the `.env` file is located in the parent directory of this scripts folder (the repo root). This matches the pattern used elsewhere in `CLI scripts`.
- The scripts do not create Databricks service principals or PATs. They only authenticate to Azure, find the workspace resource and open/inspect it. Creating tokens or automating Databricks API calls requires workspace-level permissions.
