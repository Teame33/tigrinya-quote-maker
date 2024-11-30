import os
import shutil

# Remove the instance directory and its contents
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
if os.path.exists(instance_path):
    shutil.rmtree(instance_path)
    print("Database cleaned up successfully!")
