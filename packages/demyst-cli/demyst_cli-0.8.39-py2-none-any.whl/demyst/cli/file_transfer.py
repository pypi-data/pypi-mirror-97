import os
import requests
import yattag
from IPython.core.display import HTML

from demyst.common.config import load_config

# For all functions:
# If region is not specified, use user's region from config.
# If organization is not specified, use user's organization.
# If env is not specified, use production.

# Upload file.
def upload_file(file_path, region=None, org_id=None, env=None):
    c = load_config(env=env)
    if region == None:
        region = c.get("REGION")
    if org_id == None:
        org_id = c.get_organization()
    params = {
        "filename": os.path.basename(file_path),
        "region_code": region,
        "organization_id": org_id
        }
    # Get signed URL
    url_resp = c.auth_get(c.get("MANTA_URL") + "upload/get_url", params=params)
    url_json = url_resp.json()
    url = url_json["signed_url"]
    s3_object_id = url_json["s3_object_id"]
    with open(file_path, "rb") as f:
        # Put file
        upload_resp = requests.put(url, data=f)
        if (upload_resp.status_code == 200):
            params["s3_object_id"] = s3_object_id
            # Causes all Demyst users to become permitted, if org = Demyst
            params["permitted_users"] = ""
            # Notify Manta of upload
            c.auth_get(c.get("MANTA_URL") + "upload/new_file_uploaded", params=params)
            print("Successfully uploaded file " + file_path + " to organization " + str(org_id))
        else:
            c.raise_http_request_error(upload_resp)

# List uploaded files as JSON.
def list_files(direction, region=None, org_id=None, env=None):
    c = load_config(env=env)
    if region == None:
        region = c.get("REGION")
    if org_id == None:
        org_id = c.get_organization()
    params = {
        "region_code": region,
        "organization_id": org_id,
        "direction": direction
        }
    list_resp = c.auth_get(c.get("MANTA_URL") + "download/get_file_list", params=params)
    files = list_resp.json()["file_list"]
    return [{ "name": f[0], "size": f[1], "date": f[2], "url": f[3] } for f in files]

# Display files in Jupyter.
def demyst_uploaded_files(region=None, org_id=None, env=None):
    return __display_files(list_files("upload", region, org_id, env))

def client_uploaded_files(region=None, org_id=None, env=None):
    return __display_files(list_files("download", region, org_id, env))

def __display_files(files):
    doc = yattag.Doc()
    with doc.tag("table"):
        with doc.tag("tr"):
            doc.line("th", "ID")
            doc.line("th", "Name")
            doc.line("th", "Date")
            doc.line("th", "Size")
        if len(files) > 0:
            for i, f in enumerate(files):
                with doc.tag("tr"):
                    doc.line("td", str(i + 1))
                    with doc.tag("td"):
                        doc.line("a", f["name"], href=f["url"])
                    doc.line("td", f["date"])
                    doc.line("td", f["size"])
        else:
            doc.line("td", "No files available", colspan="3")
    return HTML(doc.getvalue())

# Must specify either numeric file_id or file_name.
# If local_file_name is not specified, will use name of uploaded file.
def download_client_file(file_id=None, file_name=None, local_file_name=None, org_id=None, region=None, env=None):
    c = load_config(env=env)
    if region == None:
        region = c.get("REGION")
    if org_id == None:
        org_id = c.get_organization()
    files = list_files("download", region=region, org_id=org_id, env=env)
    if file_name != None:
        for f in files:
            if f["name"] == file_name:
                file = f
                break
    elif file_id != None:
        file = files[file_id - 1]
    else:
        raise RuntimeError("Must specify either file_id or file_name")
    if not file:
        raise RuntimeError("File not found")
    if not local_file_name:
        local_file_name = file["name"]
    print("Downloading file " + file["name"] + " (" + file["size"] + ")")
    resp = requests.get(file["url"])
    if resp.status_code == 200:
        with open(local_file_name, "wb") as local_file:
            local_file.write(resp.content)
        print("Successfully written file to " + local_file_name)
    else:
        raise RuntimeError(resp.status_code)

def show_org(env=None):
    c = load_config(env=env)
    print("Organization Name: " + c.get_organization_name())
    print("Organization ID:   " + c.get_organization())
