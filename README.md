
Meridian AI
A small web app that does two jobs, using AI:

Ask questions about your documents. Upload PDFs (policies, contracts, reports), then ask in plain English. The app answers using only what is in your documents.
Check a purchase before paying. Paste a purchase request. Three AI "specialists" review it (risk, tax, accounting). A final "CFO" step writes one short memo with a decision.
It is built to learn from. The company in the examples, Aldermoor Industries, is fictional, and the sample documents contain made-up data.

The "checks" in the audit are done by the AI from its general knowledge (only the exchange-rate check uses a live data source). This is a demo of how such a system is built, not a real compliance tool.

New here? Read the Learner Guide: the story, every file explained, exercises and examples.

Jump to: Learn in depth · Technologies · How it fits together · Why many files? · What is in this repo · Run it on your computer · Why the cloud? · Settings · Problems

Learn in depth
This README is the short version. The docs/ folder explains everything step by step:

If you want to…	Read
Understand the problem the app solves	The case
See how it all fits together	The big picture
Learn the basic words (repo, .env, API…)	Basics for newcomers
See every folder and why the code is split	Project tour
Understand every file	Backend · Frontend · Root files
Follow a request from button to answer	Follow a request
Learn FastAPI, settings and logging, RAG, agents	09 · 10 · 11 · 12
See how it is packed and set up in the cloud	Docker · GitHub Actions
Check what you need, and the $300 free credit	Requirements and costs
Practise	Exercises · runnable examples
Fix an error	Troubleshooting
Is Terraform used? No. The cloud is set up by GitHub Actions running gcloud commands (see docs/14)

The technologies, in plain words
Think of a restaurant. Each technology plays one part.

Technology	What it is	Restaurant analogy
React (frontend)	The web page you click on	The dining room, menu and buttons
FastAPI (Python)	Receives requests from the page and sends back answers	The waiter: takes your order to the kitchen and brings the food back
Pydantic	Checks that requests are filled in correctly	The order form: "you forgot the table number"
LangChain	A toolkit for connecting AI steps together	The kitchen's recipe book and workflow
Gemini (Google's AI model)	Reads text and writes answers	The chef
Embeddings	Turn text into a list of numbers that capture its meaning	GPS coordinates for ideas: similar ideas get nearby coordinates
Vertex AI Vector Search	A database that finds the stored text closest in meaning to your question	A library catalogue organised by meaning, not by title
Chroma	The same kind of database, but a folder on your laptop (used when APP_MODE=local)	A home bookshelf with the same catalogue system
RAG (Retrieval-Augmented Generation)	Find the right pages first, then answer from them	An open-book exam: the chef checks the cookbook before answering
Agents and tools	AI that can decide to run small programs (tools) to get facts	A chef who can use a scale, a thermometer and a timer
Middleware (LangChain v1)	Checks that wrap every agent step: hide e-mails, stop loops, retry errors, log tool calls	The kitchen's head of hygiene and safety, watching every step
Cloud Storage	Keeps files in Google Cloud	A filing cabinet
Docker	Packs the app and everything it needs into one box	A lunchbox: opens the same anywhere
Cloud Run	Runs that box on the internet, only when someone visits	A pop-up shop that opens only when customers arrive
Secret Manager	Stores passwords and keys safely	A safe
GitHub Actions	Builds and delivers the app automatically	A delivery robot
Logging (structlog)	The app writes down what it does	The kitchen's diary: when something goes wrong, you read it
How it fits together
 YOU (browser)
   │  click "Ask"
   ▼
 FRONTEND (React)                       the dining room
   │  sends a request
   ▼
 BACKEND (FastAPI)                      the waiter
   │
   ├── Document Q&A (RAG) ───────────┐
   │     1. cut PDFs into small pieces│   Vertex AI: turns pieces into numbers
   │     2. store them ───────────────┼─► Vector Search: finds pieces closest to your question
   │     3. find pieces for question ◄┘
   │     4. ask Gemini to answer from those pieces ─► Gemini
   │
   └── Purchase audit (agents)
         Risk agent    ─ tools ┐
         Tax agent     ─ tools ├─► each calls Gemini, then a "CFO" step writes the memo
         Control agent ─ tools ┘
What happens when you ask a question

You type a question in the page. The page sends it to the backend.
The backend turns your question into numbers (an embedding).
Vector Search returns the three stored pieces of your documents closest to it.
The backend gives Gemini those pieces and your question: "Answer using only this."
Gemini's answer travels back to your page.
What happens when you run an audit

You submit a purchase request.
The risk, tax and control agents each read it. Each one decides which tools to use (for example, "check the exchange rate") and writes a short report.
A final step reads the three reports and writes one memo with a decision: approved, conditional hold, or rejected.
Why is the code split into many files?
You could put everything in one file. For a ten-line experiment that is fine. For a real app it becomes a problem. Think of a kitchen where everyone cooks on one table: you cannot find anything, people get in each other's way, and one spill ruins every dish.

The app is split so that each folder and file has one job, like stations in a kitchen:

Problem with one big file	How splitting helps
Hard to find things ("where is the tax prompt?")	The name tells you where to look
Changing one thing can break another	A change stays inside its own file
Hard to test ("it needs the internet just to start")	Parts can be tested alone
Copy-pasted code drifts apart	One function is written once and reused
Many people editing the same file clash	People work in different files
Intimidating to read	Read one small file at a time
Rule of thumb: one file, one job. The web layer does not know how AI works. The AI code does not know what a web address is.

What's in this repo
backend/                      The Python server
├── api/                      The "waiter": web addresses and rules
│   ├── main.py                 Creates the app and plugs everything together
│   ├── endpoints.py            Every web address (e.g. POST /api/rag/ask)
│   └── schemas.py              The shape of requests and replies (the order forms)
├── rag/                      Document Q&A (the "library")
│   ├── llm.py                  Gets the Gemini chat model
│   ├── embeddings.py           Text → numbers
│   ├── vector_store.py         Connects to Vector Search
│   ├── data_ingestion.py       PDF → pieces → stored
│   └── retrieval.py            Question → find pieces → answer
├── agent/                    The purchase audit
│   ├── tools.py                The five tools agents can use
│   ├── prompts.py              The written instructions for each agent
│   └── agents.py               Creates the agents and runs them in order
├── config/settings.py        Reads settings (keys, names) from outside the code
├── logger/custom_logger.py   The app's diary (JSON log lines)
└── tests/                    Automatic checks that need no accounts

frontend/                     The web page (React + TypeScript)
└── src/lib/api.ts            The only file that talks to the backend

sample_docs/                  Four made-up PDFs to try the app with
docs/                         The learner guide (19 pages) and docs/examples/ (6 small programs)
.github/workflows/deploy.yml  Robot that sets up the cloud and deploys the app
Dockerfile                    Recipe to pack the app into one box
requirements.txt              Python packages (exact versions)
.env.example                  Template for your private settings
DEPLOY.md                     How to put the app on the internet
Each package depends only on the ones below it:

api  →  rag, agent  →  config, logger
Run it on your computer
What you need
For	You need
Everything	Python 3.12, Git. For the web page also Node.js 20+
Local mode (audit and document Q&A)	Only a free Gemini API key from https://aistudio.google.com/apikey
Cloud mode	A Google Cloud project (see DEPLOY.md)
Local or cloud? One switch
APP_MODE in .env decides where the app keeps its data. Nothing else in the code changes.

APP_MODE=local (default)	APP_MODE=cloud
Chat model	Gemini API (API key)	Gemini API (key from Secret Manager)
Embeddings	gemini-embedding-001 via Gemini API	text-embedding-005 via Vertex AI
Vector database	Chroma, a folder on your disk (.meridian/chroma)	Vertex AI Vector Search
Uploaded PDFs	.meridian/uploads/	Cloud Storage bucket
Logs	logs/ folder	logs/ + copied to the bucket on shutdown
Google Cloud project needed?	No	Yes
The System Status tab (and GET /api/status) shows which mode is running.

Quick start: everything locally (about 10 minutes, no Google Cloud)
# 1. Get the code (or download the ZIP from GitHub and unzip it)
git clone https://github.com/mayank953/meridian-ai-learner.git
cd meridian-ai-learner

# 2. Make a private Python environment and install the packages
python3.12 -m venv .venv
source .venv/bin/activate            # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt

# 3. Create your settings file and add your Gemini key
cp .env.example .env                 # Windows: copy .env.example .env
#    open .env and set:  GOOGLE_API_KEY=your-key   (leave APP_MODE=local)

# 4. Start the backend
uvicorn api.main:app --app-dir backend --reload --port 8080
Now open http://localhost:8080/docs. This page is made automatically by FastAPI and lets you try every address:

Open GET /api/health → Try it out → Execute. You should see {"status": "ok"}.
Open POST /api/agent/audit → Try it out. Paste a request such as:
{"request_text": "Purchase of 200 PLC controllers from Takumi Controls Europe B.V. (Netherlands). Total 480,000 EUR. Origin JP, destination DE. FX rate quoted: 1 EUR = 163.5 JPY."}
Press Execute and wait: several AI calls are happening, so it can take up to a minute or more.
You get four texts: risk, tax and control reports, and the CFO memo. Wording changes each time (an AI writes it), but the layout stays the same.
Run every command from the project's main folder. The app looks for .env in the folder where you start it.

Add the web page (optional)
Open a second terminal and keep the backend running:

cd frontend
npm install
npm run dev
Open http://localhost:3000.

Try document Q&A
Works in local mode with just your Gemini key (in cloud mode, see DEPLOY.md):

Upload the PDFs in sample_docs/ (Index Documents tab, or POST /api/rag/upload).
Ask: "What is Aldermoor Industries total revenue in FY2024?" → about EUR 2.84 billion. Also try: payment terms for servo motor suppliers (Net-45), customs duty on PLC controllers from Japan (2.2 %), depreciation of filling line equipment (10 years).
Ask something that is not in the documents. The answer should say it does not know.
Check that everything is wired up
pytest backend/tests
Expected: 17 passed. These tests need no accounts and no internet: they include a full local run (PDF → Chroma → answer) and an agent run through the middleware, with fake AI models.

Run it in Docker (optional)
docker build -t meridian-ai .
docker run -p 8080:8080 --env-file .env -v "$(pwd)/.meridian:/app/.meridian" meridian-ai
Then open http://localhost:8080. The box does not contain your .env, so you pass it in. The -v part keeps your local vector database and uploads on your disk, so they survive restarting the container.

Why would you need the cloud?
You do not need it to learn or to run every feature: local mode does it all on your laptop. You do need it for these reasons:

Reason	Explanation
A managed vector database	Chroma on your disk is perfect for one person. Vertex AI Vector Search is shared, backed up and scales to millions of chunks.
Sharing	On your laptop, only you can open localhost. In the cloud, anyone with the link can.
Always on	Your laptop sleeps and goes offline. A cloud service keeps running.
Automatic delivery	Each time you save changes, a robot can rebuild and publish the app.
Scaling	Many users at once? The cloud can start more copies.
It costs money. The vector database is billed by the hour while it is running, even if nobody uses it. New Google Cloud customers get a $300 credit for 90 days. DEPLOY.md explains the costs, how to set a budget alert, and how to switch everything off.

Deploying to a Brand New GCP Project (From Scratch)
If you are moving this codebase to an entirely new GCP project where nothing has been configured, follow these exact manual steps once. After this initial setup, the GitHub Action will fully manage the project for you.

Step 1: Create the Project and Enable Billing
Go to the Google Cloud Console.
Create a new project (e.g., meridian-ai-prod).
Link an active Billing Account to the project.
Important

Cloud Run and Vertex AI require active billing to function. The deployment pipeline will fail silently without it.

Step 2: Create a Powerful Service Account
The GitHub Action acts as a "robot administrator". It needs permission to enable APIs, create storage buckets, provision vector indexes, and deploy services.

Open Google Cloud Shell (or your local terminal authenticated to your account) and run:

# Set your active project
export PROJECT_ID="meridian-ai-prod"
gcloud config set project $PROJECT_ID

# Create the GitHub Deployer service account
gcloud iam service-accounts create github-deployer \
  --display-name="GitHub Actions Deployer" \
  --project=$PROJECT_ID

# Grant the "Editor" role so it can build infrastructure
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-deployer@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/editor"

# Grant IAM Admin role so it can manage service-level permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-deployer@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/resourcemanager.projectIamAdmin"

# Generate the JSON key file
gcloud iam service-accounts keys create github-deployer-key.json \
  --iam-account=github-deployer@${PROJECT_ID}.iam.gserviceaccount.com
Caution

The github-deployer-key.json file contains highly privileged credentials. Never commit this file to version control. Store it securely and delete the local copy after adding it to GitHub Secrets.

Troubleshooting: "Key creation is not allowed on this service account"
If the last command fails with this error:

ERROR: (gcloud.iam.service-accounts.keys.create) FAILED_PRECONDITION: Key creation is not allowed on this service account.
  ...
    type: constraints/iam.disableServiceAccountKeyCreation
your project belongs to a Google Cloud Organization that blocks service account keys by default (the iam.disableServiceAccountKeyCreation organization policy). You need to switch that policy off for your project.

Changing it requires the Organization Policy Administrator role (roles/orgpolicy.policyAdmin). This role cannot be granted at the project level (you get an INVALID_ARGUMENT error if you try). It must be granted on the Organization, even though you only change the policy for one project.

1. Find your Organization ID. Copy the numeric ID from the output:

gcloud organizations list
2. Grant yourself the role on the Organization (replace YOUR_ORGANIZATION_ID and YOUR_EMAIL):

gcloud organizations add-iam-policy-binding YOUR_ORGANIZATION_ID \
  --member="user:YOUR_EMAIL" \
  --role="roles/orgpolicy.policyAdmin"
3. Turn off the policy for your project. Wait about 60 seconds for the role to take effect, then run:

gcloud resource-manager org-policies disable-enforce \
  iam.disableServiceAccountKeyCreation \
  --project=$PROJECT_ID
4. Create the JSON key again:

gcloud iam service-accounts keys create github-deployer-key.json \
  --iam-account=github-deployer@${PROJECT_ID}.iam.gserviceaccount.com
Note

If Step 2 fails with "permission denied", your account is not an Organization Administrator and cannot change Organization IAM. Ask the person who manages your Google Cloud Organization to run Step 2 for you, or to set up Workload Identity Federation for GitHub, which needs no key file at all.

Tip

Once the key is created you can turn the policy back on with gcloud resource-manager org-policies enable-enforce iam.disableServiceAccountKeyCreation --project=$PROJECT_ID. The key you already made keeps working; only new keys are blocked.

Step 3: Configure GitHub Secrets
Navigate to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret.

Add the following three secrets:

Secret Name	Value
GCP_PROJECT_ID	Your new project ID (e.g., meridian-ai-prod)
GCP_CREDENTIALS_JSON	The entire contents of github-deployer-key.json
GOOGLE_API_KEY	Your Gemini API key from AI Studio (starts with AI, 39 characters)
Step 4: Trigger the Pipeline
Push your code to the main branch (or manually trigger the workflow via the Actions tab).

git add .
git commit -m "<Commit Message>"
git push
The GitHub Action (.github/workflows/deploy.yml) will now automatically:

✅ Enable all necessary GCP APIs natively.
✅ Provision the Cloud Storage buckets.
✅ Create the Vertex AI Vector Search Index & Endpoint (expect ~30+ min on first run).
✅ Inject your GOOGLE_API_KEY into GCP Secret Manager.
✅ Grant the build and Cloud Run service account the permissions it needs (Secret Manager, Cloud Build, Vertex AI, Cloud Storage).
✅ Build the Docker image and push to Artifact Registry.
✅ Deploy the Cloud Run service with public access.
Note

The very first deployment can take 30–45 minutes due to Vector Search index creation. Subsequent deployments typically complete in 3–5 minutes.

Once complete, the Action logs will print your live Cloud Run URL. Your application is now fully automated and live! 🚀

Settings
Settings live in .env (copy .env.example). .env is never uploaded to Git.

Setting	Meaning	Needed for
APP_MODE	local (default) or cloud	Always
GOOGLE_API_KEY	Your Gemini key	Both modes
VERTEX_LLM_MODEL_NAME	Chat model, default gemini-3.8-flash	Optional
LLM_TEMPERATURE	0 = most repeatable answers	Optional
LOCAL_EMBEDDING_MODEL_NAME	Default gemini-embedding-001	Optional, local
LOCAL_DATA_DIR	Where Chroma and uploads live, default .meridian/	Optional, local
AGENT_MAX_MODEL_CALLS / AGENT_MAX_TOOL_CALLS / AGENT_MAX_RETRIES	Middleware limits, defaults 8 / 6 / 2	Optional
GCP_PROJECT_ID	Your Google Cloud project	Cloud
GCP_REGION	Where it runs, e.g. us-central1	Cloud
GCS_BUCKET_NAME	Cloud Storage bucket name	Cloud
GCS_PREFIX	Folder for uploads, uploads/	Cloud
VECTOR_SEARCH_INDEX_ID	ID of your vector index	Cloud
VECTOR_SEARCH_INDEX_ENDPOINT_ID	ID of its endpoint	Cloud
GCP_SERVICE_ACCOUNT_PATH	Path to your key file	Cloud mode run from a laptop
VERTEX_EMBEDDING_MODEL_NAME	Embedding model, default text-embedding-005	Optional, cloud
AI model names are retired from time to time. If you see "model not found", look up a current name at https://ai.google.dev/gemini-api/docs/models and set VERTEX_LLM_MODEL_NAME.

Common problems
What you see	What to do
ModuleNotFoundError: No module named 'api'	Run from the main folder and keep --app-dir backend
Settings seem empty	Run from the main folder (where .env is)
ModuleNotFoundError for other packages	Activate the environment (source .venv/bin/activate) and run pip install -r requirements.txt
503 with "APP_MODE=cloud but these settings are empty"	Fill in the listed settings, or set APP_MODE=local
503 with "GOOGLE_API_KEY is empty"	Add your Gemini key to .env and restart
Old answers after changing documents	Local mode: delete the .meridian/ folder and upload again
403 from Google Cloud	Your login or key lacks permission, or the wrong account is used; see DEPLOY.md
"model not found"	Change VERTEX_LLM_MODEL_NAME to a current model
Port already in use	Stop the other program, or use --port 8081
Browser says "blocked by CORS"	The backend is not running on port 8080
When something fails, read the last lines in the terminal. The app writes a diary of what it did as one JSON line per event; the error is usually there.

Aldermoor Industries and all sample data are fictional.
