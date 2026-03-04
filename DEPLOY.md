# Deployment Guide: TRAE-D-SME-Pricing

This guide deploys the demo to Streamlit Community Cloud.

## 1. Prerequisites
- GitHub account
- Streamlit Community Cloud account

## 2. Push Code to GitHub
```bash
git init
git add .
git commit -m "chore: initial commit"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/TRAE-D-SME-Pricing.git
git push -u origin main
```

## 3. Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io and sign in.
2. Click `New app`.
3. Select the repository: `<YOUR_USERNAME>/TRAE-D-SME-Pricing`.
4. Branch: `main`.
5. Main file path: `ui_streamlit/app.py`.
6. Click `Deploy`.

## 4. Share Link
Typical URL format:
`https://<your-app-name>.streamlit.app/`

## 5. Troubleshooting
- `ModuleNotFoundError`: ensure `requirements.txt` is complete.
- App boot failure: verify main file path is `ui_streamlit/app.py`.
- Empty page: check Streamlit logs for import/runtime errors.
