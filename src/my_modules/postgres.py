from my_modules import kubernetes

__all__ = ["connection_string"]


POSTGRES_CONFIGMAP  = kubernetes.get_json("postgres-configmap", "configmap")
POSTGRES_SECRET     = kubernetes.get_json("postgres-auth-secret", "secret", base64decode=True)

POSTGRES_HOST       = POSTGRES_CONFIGMAP.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT       = POSTGRES_CONFIGMAP.get("POSTGRES_PORT", "5432")
POSTGRES_DB         = POSTGRES_CONFIGMAP.get("POSTGRES_DB", "database")
POSTGRES_USERNAME   = POSTGRES_SECRET.get("username", "seshu")
POSTGRES_PASSWORD   = POSTGRES_SECRET.get("password", "")

connection_string   = f"postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
