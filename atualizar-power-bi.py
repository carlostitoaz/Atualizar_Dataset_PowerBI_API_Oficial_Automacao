import msal
import requests

# Configurações (substitua com os valores do seu registro no Azure AD / Power BI)
TENANT_ID = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
WORKSPACE_ID = ""
DATASET_ID = ""

# Construir objeto MSAL
authority = f"https://login.microsoftonline.com/{TENANT_ID}"
app = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=authority
)

# Escopo padrão (Power BI)
scopes = ["https://analysis.windows.net/powerbi/api/.default"]

# Obter token de acesso
result = app.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    print("Token obtido com sucesso!")
    access_token = result["access_token"]

    # Testar se o token funciona listando workspaces
    test_url = "https://api.powerbi.com/v1.0/myorg/groups"
    test_headers = {"Authorization": f"Bearer {access_token}"}
    test_response = requests.get(test_url, headers=test_headers)
    print("Teste de listagem de workspaces:", test_response.status_code, test_response.text)

    # Chamada à API de refresh do Power BI (sem notifyOption)
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/datasets/{DATASET_ID}/refreshes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Payload vazio, já que notifyOption não é permitido para app-only
    response = requests.post(url, headers=headers, json={})
    print("Status da chamada:", response.status_code, response.text)

else:
    print("Falha ao obter o token:")
    print(result.get("error"), result.get("error_description"))
