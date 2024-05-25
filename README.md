# LaTeXCloudBuilder

```bash
cd app
docker build -t latex-build-app .
docker run -p 8080:8080 latex-build-app
```
In an other shell
```bash
python3 script/compile_tex.py templates/example_template.tex templates/references.bib
# ENJOY
```



# Once it works locally.

This may help ;)

Great! If the script builds and runs locally, you can proceed to deploy it on AWS App Runner. Here’s a step-by-step guide to ensure your Flask application with the updated `compile_tex.py` script is deployed and running on AWS App Runner.

### Step-by-Step Guide for Deployment on AWS App Runner

1. **Ensure Your Repository is Up-to-Date**

   Make sure your local repository contains all the latest changes and push them to GitHub.

   ```bash
   git add .
   git commit -m "Updated Flask application and added compile_tex.py script"
   git push origin main
   ```

2. **Update JSON Configuration File**

   Ensure your `source-configuration.json` is correctly set up. Here’s an example configuration:

   ```json
   {
     "CodeRepository": {
       "RepositoryUrl": "https://github.com/mr-koya/LaTeXCloudBuilder",
       "SourceCodeVersion": {
         "Type": "BRANCH",
         "Value": "main"
       },
       "SourceDirectory": "/app",
       "CodeConfiguration": {
         "ConfigurationSource": "API",
         "CodeConfigurationValues": {
           "Runtime": "PYTHON_3",
           "BuildCommand": "docker build -t latex-build-app .",
           "StartCommand": "python app.py"
         }
       }
     },
     "AutoDeploymentsEnabled": true,
     "AuthenticationConfiguration": {
       "ConnectionArn": "arn:aws:apprunner:us-east-2:500412137024:connection/mr-koya-latex/d7031c07fd4847f29c128064cdb5ddda"
     }
   }
   ```

3. **Deploy the Application on AWS App Runner**

   Use the AWS CLI to deploy the application.

   ### Update the Existing Service
   If the service already exists, update it:

   ```bash
   aws apprunner update-service \
       --service-arn arn:aws:apprunner:us-east-2:500412137024:service/LaTeXCloudBuilder/b399eb6af870443aa37ce2cd3afde4e4 \
       --source-configuration file://source-configuration.json \
       --region us-east-2
   ```

   ### Create a New Service (if the update fails or if you prefer to start fresh)
   1. **Delete the Existing Service (if necessary):**

      ```bash
      aws apprunner delete-service \
          --service-arn arn:aws:apprunner:us-east-2:500412137024:service/LaTeXCloudBuilder/b399eb6af870443aa37ce2cd3afde4e4 \
          --region us-east-2
      ```

   2. **Create the New Service:**

      ```bash
      aws apprunner create-service \
          --service-name LaTeXCloudBuilder \
          --source-configuration file://source-configuration.json \
          --region us-east-2
      ```

4. **Monitor the Deployment**

   Monitor the deployment status in the AWS App Runner console. Ensure that the service status changes to "RUNNING".

   You can also monitor the deployment using the AWS CLI:

   ```bash
   aws apprunner describe-service --service-arn arn:aws:apprunner:us-east-2:500412137024:service/LaTeXCloudBuilder/b399eb6af870443aa37ce2cd3afde4e4 --region us-east-2
   ```

5. **Test the Deployed Application**

   Once the application is running, you can test it by sending a request using the provided Python script. Update the URL in the script to point to your AWS App Runner service.

   ```python
   import requests
   import base64
   import json
   import sys
   import os

   def compile_tex(tex_content, bib_content):
       url = "http://<YOUR_APP_RUNNER_URL>/compile"  # Replace with your AWS App Runner URL
       headers = {
           "Content-Type": "application/json"
       }
       data = {
           "tex": tex_content,
           "bib": bib_content
       }
       response = requests.post(url, headers=headers, data=json.dumps(data))
       
       if response.status_code == 200:
           response_data = response.json()
           pdf_base64 = response_data.get("pdf")
           if pdf_base64:
               pdf_data = pdf_base64.encode('latin1')
               with open("output.pdf", "wb") as pdf_file:
                   pdf_file.write(pdf_data)
               print("PDF successfully generated and saved as output.pdf")
           else:
               print("No PDF data found in the response")
       else:
           print(f"Failed to compile. Status code: {response.status_code}")
           print(response.json())

   def read_file_content(file_path):
       if not os.path.isfile(file_path):
           print(f"File not found: {file_path}")
           sys.exit(1)
       
       with open(file_path, 'r') as file:
           return file.read()

   if __name__ == "__main__":
       if len(sys.argv) != 3:
           print("Usage: python compile_tex.py <tex_file> <bib_file>")
           sys.exit(1)
       
       tex_file = sys.argv[1]
       bib_file = sys.argv[2]
       
       tex_content = read_file_content(tex_file)
       bib_content = read_file_content(bib_file)
       
       compile_tex(tex_content, bib_content)
   ```

6. **Run the Python Script**

   Execute the Python script to test the deployed service:

   ```bash
   python compile_tex.py path/to/latex_file.tex path/to/bib_file.bib
   ```

By following these steps, you can deploy your Flask application with the updated script on AWS App Runner, ensuring it works correctly both locally and in the cloud. If you encounter any issues or need further assistance, feel free to ask.
