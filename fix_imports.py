# fix_imports.py - Run this to fix the import issue
import os

print("🔧 Fixing module imports...")

# Create __init__.py files
folders = ['utils', 'models']

for folder in folders:
    init_file = os.path.join(folder, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Package initialization\n')
        print(f"✅ Created: {init_file}")
    else:
        print(f"✅ Already exists: {init_file}")

print("🎉 Fix complete! Now run: py -3.11 app.py")