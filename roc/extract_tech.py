"""Compatibility entry point for the installed-definition grant exporter."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"tools"))
from export_grants import main
if __name__=="__main__":main()
