import os
from functools import partial
from hashlib import md5
from tempfile import TemporaryDirectory
import logging

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.appconfiguration import AzureAppConfigurationClient
from azure.core.exceptions import ResourceNotFoundError
from psycopg2 import connect
from compose import compose

def cert_con_str(host,port,user,dbname,cert,key,rootcert):
    constring = f"""
        host={host}
        port={port}
        user={user}
        dbname={dbname}
        sslcert={os.path.abspath(cert)}
        sslkey={os.path.abspath(key)}
        sslrootcert={os.path.abspath(rootcert)}
        sslmode=require
    """
    logging.info(constring)
    return constring

def vault_url(name):
    return f"https://{name}.vault.azure.net"

def get_secret(name,vault,credential):
    client = SecretClient(vault_url=vault_url(vault),credential=credential)
    return client.get_secret(name).value

def cleanup_wrapper(files):
    def wrapper(fn):
        def inner(*args,**kwargs):
            for f in files:
                os.unlink(f)
            return fn(*args,**kwargs)
        return inner
    return wrapper

def save_hash(string,directory):
    fname = os.path.join(directory,md5(string.encode()).hexdigest())
    with open(fname,"w") as f:
        f.write(string)
    return fname

def fix_kf_permissions(filename):
    """
    Necessary for using key file
    """
    os.chmod(filename,0x700)
    return filename

def secure_connect(host:str,port:str,user:str,dbname:str,keyvault:str,cert:str,key:str,rootcert:str,
        credential=None,cert_folder:str=None,cleanup:bool=True):

    if cert_folder is None:
        temp_cert_folder = TemporaryDirectory()
        cert_folder = temp_cert_folder.name

    if credential is None:
        credential=DefaultAzureCredential()

    store_secret = compose(
            fix_kf_permissions,
            partial(save_hash,directory=cert_folder),
            partial(get_secret,vault=keyvault,credential=credential),
        )

    secrets = [*map(store_secret,[cert,key,rootcert])]

    con = connect(cert_con_str(host,port,user,dbname,*secrets))

    if cleanup:
        for f in secrets:
            os.unlink(f)
        try:
            temp_cert_folder.cleanup()
        except NameError:
            pass

    return con

def secure_connect_ac(appconfig_connnection_string,*args,**kwargs):
    """
    Performs secure connect with settings from azure appconfig store
    """
    client = AzureAppConfigurationClient.from_connection_string(appconfig_connnection_string)
    for setting in ["keyvault","host","port","user","dbname","cert","key","rootcert"]:
        logging.warning(f"getting {setting}")
        try:
            kwargs[setting] = client.get_configuration_setting(setting).value
        except ResourceNotFoundError:
            logging.warning(f"{setting} is not defined in appconfig")
    return secure_connect(*args,**kwargs)
