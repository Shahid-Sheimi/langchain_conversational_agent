"""
Setup verification script
Checks if all required dependencies are installed
"""

import sys

def check_imports():
    """Check if all required packages can be imported"""
    required_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'streamlit': 'Streamlit',
        'PyPDF2': 'PyPDF2',
        'langchain': 'LangChain',
        'langchain_community': 'LangChain Community',
        'openai': 'OpenAI',
        'faiss': 'FAISS',
        'requests': 'Requests',
        'dotenv': 'python-dotenv',
    }
    
    missing_packages = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name} is installed")
        except ImportError:
            print(f"❌ {name} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required packages are installed!")
        return True

if __name__ == "__main__":
    print("Checking dependencies...\n")
    success = check_imports()
    sys.exit(0 if success else 1)

