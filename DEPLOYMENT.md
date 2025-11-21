# Vercel Deployment Guide

## Prerequisites
1. A Vercel account (sign up at https://vercel.com)
2. A Google Gemini API key (get it from https://makersuite.google.com/app/apikey)
3. Git installed on your computer
4. Node.js installed (for Vercel CLI)

## Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

## Step 2: Login to Vercel
```bash
vercel login
```
This will open your browser to authenticate.

## Step 3: Set Up Environment Variable
Before deploying, you need to set your Gemini API key:

### Option A: Set via Vercel Dashboard (Recommended)
1. Go to https://vercel.com/dashboard
2. Create a new project or select your project
3. Go to **Settings** → **Environment Variables**
4. Add a new variable:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key
   - **Environment**: Production, Preview, and Development (select all)

### Option B: Set via CLI
```bash
vercel env add GEMINI_API_KEY
```
Then paste your API key when prompted.

## Step 4: Deploy to Vercel

### First Deployment
From your project directory:
```bash
vercel
```
Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? (Select your account)
- Link to existing project? **No** (for first time)
- Project name? (Press Enter for default or enter a custom name)
- Directory? (Press Enter for current directory)

### Subsequent Deployments
```bash
vercel --prod
```

## Method 2: Deploy via GitHub (Recommended for Continuous Deployment)

### Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### Step 2: Import to Vercel
1. Go to https://vercel.com/dashboard
2. Click **Add New** → **Project**
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

### Step 3: Add Environment Variable
1. In the project settings, go to **Environment Variables**
2. Add `GEMINI_API_KEY` with your API key
3. Make sure it's enabled for **Production**, **Preview**, and **Development**

### Step 4: Deploy
Click **Deploy** and wait for the build to complete.

## Method 3: Deploy via Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click **Add New** → **Project**
3. If you have a Git repository, import it
4. If not, you can drag and drop your project folder
5. Configure environment variables (add `GEMINI_API_KEY`)
6. Click **Deploy**

## Testing Your Deployment

After deployment, Vercel will provide you with a URL like:
- `https://your-project-name.vercel.app`

Test your endpoints:
- Home: `https://your-project-name.vercel.app/`
- Detect: `https://your-project-name.vercel.app/detect.html`
- Summarize: `https://your-project-name.vercel.app/summarize.html`
- Generate: `https://your-project-name.vercel.app/generate.html`

## Troubleshooting

### API Key Not Working
- Make sure `GEMINI_API_KEY` is set in Vercel environment variables
- Redeploy after adding environment variables
- Check that the variable is enabled for the correct environment

### Build Errors
- Check that `requirements.txt` has the correct package: `google-generativeai`
- Ensure Python 3.x is available (Vercel uses Python 3.9 by default)

### CORS Issues
- The API endpoints already include CORS headers
- If you still have issues, check browser console for errors

### Function Timeout
- Current timeout is set to 60 seconds in `vercel.json`
- For longer operations, you may need to increase this

## Local Development

To test locally before deploying:
```bash
vercel dev
```
This will start a local server that mimics Vercel's environment.

**Important**: Create a `.env.local` file with:
```
GEMINI_API_KEY=your_api_key_here
```

## Updating Your Deployment

After making changes:
1. Commit your changes to Git
2. Push to GitHub (if using GitHub integration)
3. Vercel will automatically redeploy
4. Or run `vercel --prod` if using CLI

## Project Structure

Your project should have:
```
├── api/
│   ├── detect.py
│   ├── generate.py
│   └── summarize.py
├── public/
│   ├── index.html
│   ├── detect.html
│   ├── summarize.html
│   ├── generate.html
│   ├── detect.js
│   ├── summarize.js
│   ├── generate.js
│   └── styles.css
├── requirements.txt
├── vercel.json
└── package.json
```

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support

