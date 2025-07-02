import os
import sys

# Get the current directory where the app.py is located
base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
app_path = os.path.join(base_dir, "app.py")

# Launch Streamlit
os.system(f'streamlit run "{app_path}"')
