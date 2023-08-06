# Hash JupyterHub Authenticator

An authenticator for [JupyterHub](https://jupyterhub.readthedocs.io/en/latest/) where the password for each user is a secure hash of its username. Useful for environments where it's not suitable for users to authenticate with their Google/GitHub/etc. accounts.

## Installation

```bash
pip install jupyterhub-hashauthenticator
```

Should install it. It has no additional dependencies beyond JupyterHub, oauthenticator, and their dependencies.

## Basic usage

The package provides a basic `HashAuthenticator` class, which requires all users to log in with their hash password.  You can use this as your authenticator by adding the following lines to your `jupyterhub_config.py`:

```python
c.JupyterHub.authenticator_class = 'hashauthenticator.HashAuthenticator'
c.HashAuthenticator.secret_key = 'my secret key'  # Defaults to ''
c.HashAuthenticator.password_length = 10          # Defaults to 6
c.HashAuthenticator.show_logins = True            # Optional, defaults to False
```

You can generate a good secret key with:
```bash
$ openssl rand -hex 32
0fafb0682a493485ed4e764d92abab1199d73246477c5daac7e0371ba541dd66
```

If the `show_logins` option is set to true, a CSV file containing login names and passwords will be served (to admins only) at `/hub/login_list`.

## Advanced usage

You may also combine the hash authenticator for standard users with an existing authenticator for admin users.  The `make_hash_authenticator` function can create a new class with this bifurcated login system.  It takes two arguments, the name of the new class (important for use in configuration files) and the Authenticator class to be used for admin users.

The function should work with any Authenticator that defines a `.login_url` attribute, instead of relying on the username/password entry form.  To get to that URL, you must enter a username in that entry form that is recognized as an admin name by virtue of ending with the *admin_suffix*, which defaults to `@`.  That username is not actually used (so you can just enter the suffix on its own)&mdash;instead the admin authenticator takes over.  The username returned by that will thave the *admin_suffix* appended for JupyterHub.  These users will be added to the JupyterHub whitelist, if one is in use.

A mixed authenticator using Google's OAuthenticator has already been constructed, as `GoogleHashAuthenticator`.  Below is an outline of the necessary configuration to use it.

```python
c.JupyterHub.authenticator_class = 'hashauthenticator.GoogleHashAuthenticator'
c.GoogleHashAuthenticator.secret_key = "my secret key"
c.GoogleHashAuthenticator.password_length = 10
c.GoogleHashAuthenticator.oauth_callback_url = 'http://<jupyterhub URL>/hub/oauth_callback'
c.GoogleHashAuthenticator.client_id = 'client ID'
c.GoogleHashAuthenticator.client_secret = 'client secret'
c.GoogleHashAuthenticator.hosted_domain = 'company.com'
```

## Generating the password

This package comes with a command called `hashauthpw`. Example usage:

```bash
$ hashauthpw
usage: hashauthpw [-h] [--length LENGTH] username [secret_key]

$ hashauthpw pminkov my_key
939fd4
```
