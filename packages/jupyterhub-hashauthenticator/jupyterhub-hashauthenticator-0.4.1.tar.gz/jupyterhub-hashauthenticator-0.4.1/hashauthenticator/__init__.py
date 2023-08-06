from .passwordhash import generate_password_digest
# To let the password script be run where JupyterHub isn't installed:
try:
  from .hashauthenticator import HashAuthenticator, GoogleHashAuthenticator, make_hash_authenticator
except ImportError as e:
  print("Warning: Unable to import HashAuthenticator.\n"
        "Only generate_password_digest will be available.")
  HashAuthenticator = None
  GoogleHashAuthenticator = None
  make_hash_authenticator = None


__all__ = ['HashAuthenticator', 'GoogleHashAuthenticator', 'make_hash_authenticator', 'generate_password_digest']
