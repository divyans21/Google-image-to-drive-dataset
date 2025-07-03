import importlib

modules = [
    'requests',
    'cv2',             # from opencv-python
    'numpy',
    'icrawler',
    'pydrive'
]

print("🔍 Checking for required modules...\n")
missing = []

for module in modules:
    try:
        importlib.import_module(module)
        print(f"✅ {module} is installed")
    except ImportError:
        print(f"❌ {module} is NOT installed")
        missing.append(module)

if missing:
    print("\n💡 Run the following to install missing packages:")
    pip_names = {
        'cv2': 'opencv-python',
        'pydrive': 'PyDrive'
    }
    install_cmd = "pip install " + " ".join([pip_names.get(m, m) for m in missing])
    print(f"\n{install_cmd}")
else:
    print("\n🎉 All dependencies are satisfied!")
