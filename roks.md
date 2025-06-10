https://ibm.github.io/workshop-setup/ROKS/#:~:text=oc%20login%20%2Du%20apikey%20%2Dp%20%24IBMCLOUD_APIKEY


You can achieve full automation for deploying to your ROKS (OpenShift) cluster using your IBM Cloud API key. Here are several approaches:

## Option 1: Service Account with Long-lived Token (Recommended)

Create a service account in your OpenShift cluster with the necessary permissions:

```bash
# Login to OpenShift using IBM Cloud CLI
ibmcloud login --apikey YOUR_API_KEY
ibmcloud ks cluster config --cluster YOUR_ROKS_CLUSTER_NAME

# Create a service account
oc create serviceaccount cicd-deployer -n your-namespace

# Create a role with necessary permissions
oc create role cicd-role --verb=get,list,create,update,patch,delete --resource=deployments,services,configmaps,secrets -n your-namespace

# Bind the role to the service account
oc create rolebinding cicd-binding --role=cicd-role --serviceaccount=your-namespace:cicd-deployer -n your-namespace

# Get the service account token
TOKEN=$(oc create token cicd-deployer -n your-namespace --duration=8760h) # 1 year duration
echo $TOKEN
```

Then in your CI/CD pipeline:
```bash
oc login --token=$TOKEN --server=YOUR_OPENSHIFT_API_URL
```

## Option 2: Automated Login Script

Create a script that handles the full login process:

```bash
#!/bin/bash
set -e

# IBM Cloud login
ibmcloud login --apikey $IBM_CLOUD_API_KEY -r $IBM_CLOUD_REGION

# Get cluster config
ibmcloud ks cluster config --cluster $ROKS_CLUSTER_NAME

# This automatically configures oc CLI
oc whoami  # Should work now without explicit oc login
```

## Option 3: Using IBM Cloud CLI in CI/CD

In your CI/CD pipeline (e.g., GitHub Actions, Jenkins):

```yaml
# Example for GitHub Actions
- name: Login to IBM Cloud and OpenShift
  run: |
    ibmcloud login --apikey ${{ secrets.IBM_CLOUD_API_KEY }} -r us-south
    ibmcloud ks cluster config --cluster your-roks-cluster-name
    oc version  # Verify oc is configured
    
- name: Deploy to OpenShift
  run: |
    oc apply -f your-deployment.yaml
    oc rollout status deployment/your-app
```

## Option 4: Using OpenShift CLI with IBM Cloud OAuth

Get the OAuth token programmatically:

```bash
# Get cluster info
CLUSTER_INFO=$(ibmcloud ks cluster get --cluster $ROKS_CLUSTER_NAME --output json)
MASTER_URL=$(echo $CLUSTER_INFO | jq -r '.masterURL')

# Get OAuth token using IBM Cloud API key
OAUTH_TOKEN=$(ibmcloud iam oauth-tokens --output json | jq -r '.iam_token')

# Login to OpenShift
oc login --token=$OAUTH_TOKEN --server=$MASTER_URL
```

## Recommended CI/CD Environment Variables

Set these in your CI/CD system:
- `IBM_CLOUD_API_KEY`: Your IBM Cloud API key
- `IBM_CLOUD_REGION`: Your IBM Cloud region (e.g., us-south)  
- `ROKS_CLUSTER_NAME`: Your ROKS cluster name
- `OPENSHIFT_NAMESPACE`: Target namespace for deployment

## Complete CI/CD Script Example

```bash
#!/bin/bash
set -euo pipefail

echo "Logging into IBM Cloud..."
ibmcloud login --apikey "$IBM_CLOUD_API_KEY" -r "$IBM_CLOUD_REGION"

echo "Configuring cluster access..."
ibmcloud ks cluster config --cluster "$ROKS_CLUSTER_NAME"

echo "Verifying OpenShift access..."
oc whoami
oc project "$OPENSHIFT_NAMESPACE" || oc new-project "$OPENSHIFT_NAMESPACE"

echo "Deploying application..."
oc apply -f deployment.yaml
oc rollout status deployment/your-app -n "$OPENSHIFT_NAMESPACE"

echo "Deployment completed successfully!"
```

The key insight is that `ibmcloud ks cluster config` automatically configures the `oc` CLI with the necessary authentication, so you shouldn't need a separate `oc login` step when using the IBM Cloud CLI approach.

Which CI/CD platform are you using? I can provide more specific examples based on your setup.








## Automating OpenShift (ROKS) Authentication with IBM Cloud IAM API Key

You can achieve fully automated, non-interactive authentication to your IBM Cloud Red Hat OpenShift (ROKS) cluster for CI/CD pipelines by using your IBM Cloud IAM API key. This avoids any need to manually retrieve tokens from the UI or re-login via the console.

### **How It Works**

IBM Cloud integrates IAM with OpenShift. You can use your IAM API key to obtain a session token and log in to your cluster with the `oc` CLI or programmatically, which is ideal for automation and CI/CD[1][4][6].

### **Automated Login Using API Key**

- **Direct CLI Login (Recommended for CI/CD):**

  You can log in to your OpenShift cluster using your API key directly with the `oc login` command:

  ```
  oc login -u apikey -p  --server=
  ```

  - Replace `` with your actual IBM Cloud IAM API key.
  - Replace `` with your cluster's API endpoint (the "Master URL"). You can retrieve it with:

    ```
    ibmcloud oc cluster get -c 
    ```

  This approach is fully automatable and does not require manual intervention[1][4].

- **Token Lifetime:**
  
  The access token you obtain this way is typically valid for 24 hours. For long-running automation, simply repeat the `oc login` command as part of your pipeline steps to refresh the session token as needed[1][3].

### **Programmatic Token Retrieval (Advanced)**

If you need to interact with the OpenShift API directly (for example, scripting API calls without `oc`), you can programmatically exchange your API key for an OpenShift OAuth token:

1. **Get the OAuth token endpoint:**

   ```
   curl /.well-known/oauth-authorization-server | jq -r .token_endpoint
   ```

2. **Request an access token:**

   ```
   curl -u 'apikey:' -H "X-CSRF-Token: a" '/oauth/authorize?client_id=openshift-challenging-client&response_type=token' -v
   ```

   - The `access_token` will be in the `Location` header of the HTTP 302 response[1][3].

3. **Use this token in your API calls as a Bearer token.**

### **IAM Policy Requirements**

- Ensure your API key (or the service ID it belongs to) has the necessary IAM policies to access your OpenShift cluster. You can scope access as needed for security[2].

### **Summary Table**

| Method             | Automation Level | Token Lifetime | Manual Steps | Best For                |
|--------------------|-----------------|---------------|--------------|-------------------------|
| `oc login -u apikey -p ` | Full            | 24h          | None         | CI/CD, CLI automation  |
| Programmatic OAuth | Full            | 24h           | None         | Custom API integrations |

### **Best Practice**

- For CI/CD, simply script the `oc login` command with your API key at the start of your pipeline. This is secure, repeatable, and does not require any UI interaction[1][4].

> **You do not need to retrieve a permanent token or interact with the UI. The API key is your permanent credential; use it to programmatically obtain temporary tokens as needed.**

---

**References:**  
[1] IBM Cloud Docs: Accessing Red Hat OpenShift clusters  
[4] IBM Cloud Docs: Managing the Logging agent for Red Hat OpenShift  
[6] IBM Cloud Docs: Setting up the API  
[3] StackOverflow: How to get Openshift session token using REST API calls  
[2] OpenShift Docs: Configuring an IBM Cloud account

[1] https://cloud.ibm.com/docs/openshift?topic=openshift-access_cluster
[2] https://docs.openshift.com/container-platform/4.14/installing/installing_ibm_cloud_public/installing-ibm-cloud-account.html
[3] https://stackoverflow.com/questions/49501133/how-to-get-openshift-session-token-using-rest-api-calls
[4] https://cloud.ibm.com/docs/cloud-logs?topic=cloud-logs-agent-openshift
[5] https://access.redhat.com/solutions/6407211
[6] https://cloud.ibm.com/docs/openshift?topic=openshift-cs_api_install
[7] https://docs.openshift.com/container-platform/4.9/authentication/using-service-accounts-in-applications.html
[8] https://ibm.github.io/workshop-setup/ROKS/
[9] https://github.com/IBM/roks-openshift-ai-da
[10] https://docs.redhat.com/en/documentation/openshift_container_platform/4.10/html/installing/installing-on-ibm-cloud-vpc
[11] https://suedbroecker.net/2021/11/07/configure-a-project-in-an-ibm-cloud-red-hat-openshift-cluster-to-access-the-ibm-cloud-container-registry/
[12] https://cloud.ibm.com/docs/Registry?topic=Registry-registry_access
[13] https://cloud.ibm.com/docs/account?topic=account-iamtoken_from_apikey
[14] https://github.com/IBM/ibmcloud-iam-operator
[15] https://www.redhat.com/en/blog/cicd-with-openshift
[16] https://www.redhat.com/en/technologies/cloud-computing/openshift/ci-cd
