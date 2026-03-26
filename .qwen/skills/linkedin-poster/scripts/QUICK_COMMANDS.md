# Quick Commands - LinkedIn Poster Workflow

## ✅ Fixed Command

**Don't use `^` continuation on Windows** - it causes issues. Use one of these instead:

---

## Option 1: Single Line Command (Recommended)

```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\linkedin-poster\scripts

python linkedin_poster_workflow.py "Test post from AI Employee Silver Tier" --vault "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

---

## Option 2: Use Batch File (Easiest)

```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\linkedin-poster\scripts

linkedin-post.bat "Test post from AI Employee Silver Tier"
```

Or from anywhere:
```bash
C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\linkedin-poster\scripts\linkedin-post.bat "Your post topic"
```

---

## Option 3: PowerShell (If you need multi-line)

```powershell
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\linkedin-poster\scripts

python linkedin_poster_workflow.py `
  "Test post from AI Employee Silver Tier" `
  --vault "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

---

## Quick Reference

### Post Types

```bash
# Product update (default)
linkedin-post.bat "New AI feature released"

# Milestone
linkedin-post.bat "Reached 1000 customers" --type milestone

# Industry insight
linkedin-post.bat "AI trends in 2026" --type insight

# Promotion
linkedin-post.bat "50% off this week only" --type promotion

# Testimonial
linkedin-post.bat "Client increased revenue by 50%" --type testimonial
```

### With Content Type

```bash
python linkedin_poster_workflow.py "Your topic" --type milestone --vault "VAULT_PATH"
```

---

## Common Errors

### Error: `unrecognized arguments`

**Problem:**
```
linkedin_poster_workflow.py: error: unrecognized arguments: 4
```

**Cause:** Using `^` continuation incorrectly on Windows

**Solution:** Use single line command or batch file

---

### Error: `--vault is required`

**Problem:**
```
error: the following arguments are required: --vault
```

**Solution:** Always include `--vault "PATH"` at the end

---

### Error: `vault path does not exist`

**Problem:**
```
Error: Vault path does not exist: C:\path\to\vault
```

**Solution:** Check path is correct and vault exists

---

## Workflow Output

When it runs successfully, you'll see:

```
======================================================================
LINKEDIN POSTER WORKFLOW
Complete Automated Posting with Approval
======================================================================
Topic: Test post from AI Employee Silver Tier
Vault: C:\Users\...\AI_Employee_Vault
======================================================================

STEP 1: LinkedIn Login & Detection
...
```

---

## Files Created

| File | Purpose |
|------|---------|
| `linkedin-post.bat` | Quick launch batch file |
| `QUICK_COMMANDS.md` | This file - command reference |

---

*Quick Commands Reference v1.0*
*Created: 2026-03-26*
