import os
import subprocess
import venv

def create_venv(venv_dir="venv"):
    """Create a virtual environment."""
    if not os.path.exists(venv_dir):
        venv.create(venv_dir, with_pip=True)
        print(f"Virtual environment created in {venv_dir}")
    else:
        print(f"Virtual environment already exists in {venv_dir}")

def install_requirements(venv_dir="venv"):
    """Install requirements from requirements.txt."""
    pip_executable = os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip.exe")
    subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])
    print("Dependencies installed.")

def main():
    """Main setup logic."""
    venv_dir = "venv"
    create_venv(venv_dir)
    install_requirements(venv_dir)
    print("Setup complete. Activate the virtual environment using:")
    print(f"source {venv_dir}/bin/activate" if os.name != "nt" else f"{venv_dir}\\Scripts\\activate")

if __name__ == "__main__":
    main()
