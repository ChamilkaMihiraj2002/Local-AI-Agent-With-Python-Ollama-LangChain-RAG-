# Database Permission Error - Quick Fix

## Error Message
```
❌ Error updating knowledge base
📋 Details: Query error: Database error: error returned from database: 
(code: 1032) attempt to write a readonly database
```

## Root Cause
The Chroma database directory has read-only permissions. This happens when:
1. Database was created with limited permissions
2. File ownership changed
3. Directory is mounted read-only
4. System has strict permission policies

## ⚡ Quick Fix (Run Now)

### Option 1: Fix Permissions (Recommended)
```bash
chmod -R u+w App/db/
```

Then try uploading documents again.

### Option 2: Complete Reset
```bash
# Remove the entire database
rm -rf App/db/chroma_db_generic

# The app will automatically recreate it with correct permissions
```

### Option 3: Manual Cleanup
```bash
# If above doesn't work, try:
rm -rf App/db/
mkdir -p App/db/chroma_db_generic
chmod -R u+w App/db/
```

## Detailed Steps

### Step 1: Fix Current Permissions
```bash
cd /Users/chamilkamihiraj/Desktop/GitHub/Local-AI-Agent-With-Python-Ollama-LangChain-RAG-

# Make database directory writable
chmod -R u+w App/db/

# Verify permissions are fixed
ls -la App/db/
# Should show "drwx------" or "drwxr-xr-x"
```

### Step 2: Refresh the App
```bash
# In Streamlit UI: Click "🗑️ Clean Documents" button
# Or manually remove and restart
```

### Step 3: Upload Documents Again
- Try uploading your documents
- Status should show "✅ Upload complete"

## Why This Happens

When Chroma creates the database, it needs write permissions. If it's created in a restricted location or with strict permissions, subsequent writes fail.

**Example scenario:**
1. First upload creates database with limited permissions ❌
2. Second upload tries to write → gets "readonly database" error ❌

## Prevention

The code now includes automatic permission fixing:
- `ensure_writable_directory()` runs before creating database
- Automatically fixes permissions on write operations
- Handles permission errors gracefully

## If Problem Persists

### Check Current Permissions
```bash
ls -la App/db/chroma_db_generic/
```

### Debug the Issue
```bash
# Check if you can write to the directory
touch App/db/chroma_db_generic/test.txt

# If that fails, the directory is still read-only
```

### Nuclear Option (Complete Reset)
```bash
# Remove everything and start fresh
rm -rf App/db/
rm -rf App/data/*

# Restart the app
cd App && streamlit run app.py

# Upload documents (fresh start)
```

## Advanced Troubleshooting

### If "chmod" doesn't work
```bash
# Check who owns the directory
ls -la App/db/

# If owned by different user, use sudo:
sudo chown -R $USER App/db/
sudo chmod -R u+w App/db/

# Or fix all at once:
sudo chmod -R 755 App/db/
sudo chown -R $USER:$USER App/db/
```

### If directory is mounted read-only
```bash
# Check mount status
mount | grep "App/db"

# If mounted read-only, the database won't work
# Move App/db to writable location or remount
```

### Check Disk Space
```bash
# Ensure you have space
df -h App/db/

# Check inode count
df -i App/db/
```

## Verification Steps

After applying the fix:

### 1. Verify Permissions
```bash
ls -la App/db/chroma_db_generic/
# Should show user can write (w flag)
```

### 2. Test Write Access
```bash
touch App/db/test.txt && echo "✅ Writable" || echo "❌ Read-only"
rm App/db/test.txt
```

### 3. Restart App
```bash
cd App
streamlit run app.py
```

### 4. Upload Test Document
- Upload a small PDF or TXT
- Monitor the progress
- ✅ Should show "Upload complete"

## Automated Permission Fixing

The code now includes `ensure_writable_directory()` function that:
1. Creates directories with proper permissions
2. Fixes existing directory permissions
3. Recursively fixes nested directories
4. Handles permission errors gracefully

This means **permission issues should be automatically resolved** when you:
- Upload documents
- Refresh knowledge base
- Create new vector store

## Timeline of Events

```
User uploads document
    ↓
App tries to rebuild vector store
    ↓
Code calls ensure_writable_directory() → Fixes permissions ✅
    ↓
Chroma creates database with write permissions ✅
    ↓
✅ "Upload complete" shown
```

## If Nothing Works

Contact support with:
1. Output of `ls -la App/db/`
2. Output of `ls -la App/`
3. Your OS and Streamlit version: `streamlit --version`
4. Python version: `python --version`
5. Full error message from Streamlit console

## Summary

| Issue | Fix |
|-------|-----|
| "readonly database" error | `chmod -R u+w App/db/` |
| Fresh permission issues | `rm -rf App/db/` (auto-recreate) |
| Persistent read-only | `sudo chown -R $USER App/db/` |
| Can't fix permissions | Move App to different location |

The app now handles permissions automatically, but if you see this error:

**Run this command immediately:**
```bash
chmod -R u+w App/db/
```

Then try uploading again! 🚀
