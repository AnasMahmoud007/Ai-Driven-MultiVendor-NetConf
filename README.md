# **🚀 Multi-Vendor AI-Driven NetConfig**

**Universal Network Configuration & Deployment Assistant**

NetConfig AI bridges Generative AI (Google Gemini) with traditional Network Automation (Netmiko). It allows Network Engineers to type natural language intent (e.g., *"Create a site-to-site VPN"*), generates the exact vendor-specific syntax, and pushes it directly to lab or production devices via SSH.

## **✨ Features**

* **Hybrid Deployment:** The heavy AI Brain (Flowise) is containerized in Docker, while the deployment bridge runs natively on your machine for easy SSH/Network routing.  
* **Multi-Vendor Support:** Cisco, Fortinet, Juniper, Arista, Palo Alto, Huawei, MikroTik, and more.  
* **Format Options:** Ad-hoc CLI snippets, Full Configuration files, or Ansible Playbooks (YAML).  
* **Direct SSH Deployment:** Push generated configs straight to your network devices (GNS3, EVE-NG, or Production).  
* **Fully Local & Secure:** The UI and deployment bridge run entirely on your local machine.







## **🚀 Quick Start Guide**

### **Prerequisites**

1. [Docker](https://docs.docker.com/get-docker/) installed.  
2. [Python 3.10+](https://www.python.org/downloads/) installed.  
3. A free [Google Gemini API Key](https://aistudio.google.com/).

### **Step 1: Clone the Repository**

git clone https://github.com/AnasMahmoud007/Ai-Driven-MultiVendor-NetConf.git

cd Ai-Driven-MultiVendor-NetConf

### **Step 2: Start the AI Brain (Docker)**

We use Flowise version 3.0.12 to orchestrate our LLM logic. Start it using docker-compose:

docker-compose up \-d

*Note: This will expose Flowise on http://localhost:3000 with the default login admin / AdminPassword123\!*

### **Step 3: Configure Flowise**

1. Open your browser and go to http://localhost:3000.  
2. Go to **Credentials** \-\> **Add Credential** \-\> Search for **Google Generative AI**.  
3. Paste your Gemini API Key and save it.  
4. Go to **Chatflows** \-\> **Add New** \-\> Click the Settings Gear (Top Right) \-\> **Load Chatflow**.  
5. Select the network\_assistant.json file included in this repository.  
6. Connect your newly saved Gemini API Key inside the *ChatGoogleGenerativeAI* node.  
7. Click the **Save (Floppy Disk)** icon.

### **⚠️ Step 4: Link the Frontend (CRITICAL)**

Because Flowise generates a unique ID for every user, you must link your new Chatflow to the website:

1. In your Flowise Chatflow, click the **API Endpoint (\</\>)** button at the top right.  
2. Copy the **Chatflow ID** (the long string of letters and numbers).  
3. Open index.html in any text editor.  
4. Scroll down to **Line 118** and paste your ID:  
   const FLOWISE\_ID \= "PASTE-YOUR-ID-HERE".trim();

5. Save index.html.

### **Step 5: Start the Python Bridge**

Create a virtual environment and start the application server:

\# Create and activate a Python virtual environment  
python3 \-m venv venv  
source venv/bin/activate  \# On Windows use: venv\\Scripts\\activate

\# Install the required libraries  
pip install \-r requirements.txt

\# Run the backend  
python app.py

### **Step 6: Use the Application\!**

Open your browser and navigate to: **👉 http://localhost:8000**

1. Select your Network Vendor.  
2. Type your requirement (e.g. "ping", "show system interfaces").  
3. Click **Generate Configuration**.  
4. Enter your Target Device IP/Username/Password.  
5. Click **Push to Device** to deploy it via SSH\!

## **⚠️ Disclaimer**

**You must always be in control.** AI is a powerful engine for syntax generation, but you are the architect. Always review and validate the generated configuration code before pushing it to production networks.
