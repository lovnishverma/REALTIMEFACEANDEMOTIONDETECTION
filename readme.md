Your workflow for setting up and running a Streamlit project with a virtual environment:

### **First Time Setup**
**Step 1: Install CMake**
Download CMake:
https://github.com/Kitware/CMake/releases/download/v3.31.3/cmake-3.31.3-windows-x86_64.msi

2. **Create the Virtual Environment**:
  
   python -m venv venv

3. **Activate the Virtual Environment**:
  
   venv\Scripts\activate

4. **Install Required Dependencies**:

   pip install -r requirements.txt
  
   Ensure that your `requirements.txt` file lists all necessary libraries.

5. **Run the Streamlit Application**:
  
   streamlit run app.py

### **Subsequent Runs **
1. **Activate the Virtual Environment**:
 
   venv\Scripts\activate
  
2. **Run the Streamlit Application**:
  
   streamlit run app.py

### **When Done Working**
1. **Deactivate the Virtual Environment**:
  
   deactivate

This workflow ensures that:
- Your dependencies are isolated within the virtual environment.
- The application runs with the exact versions of libraries specified in `requirements.txt`.

If you frequently switch between projects, this is an excellent approach to maintain a clean and organized Python environment.
