---
name: github-cli-tokenless
description: >-
  Tokenless GitHub CLI (`gh`) execution using active Windows Git Credential Manager OAuth token.
  Enables creating issues, managing milestones, querying PRs, and interacting with GitHub
  without Python scripts and without storing personal access tokens in `.env`.
---

# Tokenless GitHub CLI (`gh`) Skill

Use this workflow to run any `gh` command (create issues, list milestones, view PRs) by securely borrowing the active GitHub session token from the Windows Git Credential Manager into `$env:GH_TOKEN` in a single PowerShell command.

## 1. The Core One-Liner Pattern

In PowerShell, always prefix the command by extracting the credential and feeding it into `GH_TOKEN`:

```powershell
$cred = "protocol=https`nhost=github.com" | git credential fill; $env:GH_TOKEN = ($cred | Select-String "password=(.*)").Matches.Groups[1].Value; gh <command>
```

## 2. Common GitHub Workflows

### List Issues:
```powershell
$cred = "protocol=https`nhost=github.com" | git credential fill; $env:GH_TOKEN = ($cred | Select-String "password=(.*)").Matches.Groups[1].Value; gh issue list --repo netflix2023/DFWCareerDevelopment-
```

### Create an Issue with Milestone and Labels:
```powershell
$cred = "protocol=https`nhost=github.com" | git credential fill; $env:GH_TOKEN = ($cred | Select-String "password=(.*)").Matches.Groups[1].Value; gh issue create --repo netflix2023/DFWCareerDevelopment- --title "feat(component): title" --body "Issue description" --milestone "Phase 0: Prototyping, Research & Direct ATS Ingestion Pipeline" --label "enhancement,phase-0"
```

### List Milestones:
```powershell
$cred = "protocol=https`nhost=github.com" | git credential fill; $env:GH_TOKEN = ($cred | Select-String "password=(.*)").Matches.Groups[1].Value; gh api repos/netflix2023/DFWCareerDevelopment-/milestones
```

### Create a Milestone:
```powershell
$cred = "protocol=https`nhost=github.com" | git credential fill; $env:GH_TOKEN = ($cred | Select-String "password=(.*)").Matches.Groups[1].Value; gh api repos/netflix2023/DFWCareerDevelopment-/milestones -f title="Module 1: Multi-Persona Resume Builder" -f state="open"
```

## 3. Why This Pattern is Preferred
- **Zero Python Overhead**: No temporary Python scripts or subprocess calls needed.
- **Zero Leaks**: No personal access tokens or secret keys stored in `.env` or files.
- **Native `gh` CLI**: Uses the official GitHub CLI installed on the system.
