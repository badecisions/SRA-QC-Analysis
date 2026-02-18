import subprocess

def save_environment_info():
    """Salva um log detalhando o ambiente conda e as versões das ferramentas dele."""
    with open("logs/environment_snapshot.log", "w") as f:
        subprocess.run(["conda", "list"], stdout=f)

