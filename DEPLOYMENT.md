# Deploy OrderGuard AI (Streamlit Community Cloud)

The repository is prepared for a standard Streamlit deployment. A public app URL is not created automatically by GitHub; the owner must connect the repository to Streamlit Community Cloud and verify the result.

## Steps
1. Push the latest repository changes to the default branch.
2. Sign in to Streamlit Community Cloud using the GitHub account that can access this public repository.
3. Choose **Create app**.
4. Select repository `feresdouik/orderguard-ai`, branch `main`, and main file path `app.py`.
5. Use Python 3.12 if the deployment settings offer a Python version selector.
6. Deploy the app and wait for dependency installation and startup.
7. Open the generated app URL in a private/incognito browser window.
8. Test Overview, Orders, Analytics, How it works, CSV upload, filtering, inspection, and export.
9. Add the verified public URL to the hackathon project page and README only after the live app works.

## Privacy and safety
- Do not add real customer data to the repository.
- Do not add API keys or secrets; the current MVP does not need them.
- The app has no authentication. Do not upload confidential order data to a public deployment.
- A successful deployment does not make this prototype production-ready.
