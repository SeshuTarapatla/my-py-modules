from my_modules import kubernetes

__all__ = ["connection_string"]


# read data from kubernetes
POSTGRES_CONFIGMAP  = kubernetes.get_json("postgres-configmap", "configmap")
POSTGRES_SECRET     = kubernetes.get_json("postgres-auth-secret", "secret")

# read postgres properties
POSTGRES_DB         = POSTGRES_CONFIGMAP.get("POSTGRES_DB", "database")
POSTGRES_HOST       = POSTGRES_CONFIGMAP.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT       = POSTGRES_CONFIGMAP.get("POSTGRES_PORT", "5432")
POSTGRES_USERNAME   = POSTGRES_SECRET.get("username", "seshu")
POSTGRES_PASSWORD   = POSTGRES_SECRET.get("password", "seshu")

# parse psql connection string
connection_string   = f"postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
