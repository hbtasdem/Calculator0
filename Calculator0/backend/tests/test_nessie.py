import sys
from pathlib import Path

# Add backend root so imports like nessie_client work when running from tests/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nessie_client import create_demo_customers

customers = create_demo_customers()
print(customers)