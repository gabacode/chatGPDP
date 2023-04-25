from chatgpdp.app import app
import warnings

if __name__ == "__main__":
    warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
    app()
