```markdown
## Setting Up Hyperon with a Virtual Environment  

If you encounter issues like `couldn't find hyperon package`, you may need to **downgrade your Python version to 3.12 or lower** before proceeding.  

### Steps to Install Hyperon  

1. **Create a Virtual Environment** (Ensure Python version is **≤ 3.12**)  
   ```bash
   python3 -m venv hyperon-env
   ```

2. **Activate the Virtual Environment** and Install Hyperon  
   - On **Linux/macOS**:  
     ```bash
     source hyperon-env/bin/activate
     ```  
   - On **Windows**:  
     ```powershell
     hyperon-env\Scripts\activate
     ```  
   - Install the Hyperon package:  
     ```bash
     pip install hyperon
     ```

3. **Verify Installation**  
   ```bash
   metta --version
   ```  
   Expected output: `0.2.2`
```