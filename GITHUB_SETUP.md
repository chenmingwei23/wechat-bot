# GitHub Connection Guide

This document explains how to connect your local repository to GitHub.

## Steps to Connect to GitHub

1. **Create a GitHub repository**:
   - Go to [GitHub](https://github.com/) and sign in to your account
   - Click on the "New" button to create a new repository
   - Name the repository "wechat-bot" or whatever name you prefer
   - Choose if the repository should be public or private
   - Do NOT initialize the repository with a README, .gitignore, or license (since you already have these locally)
   - Click "Create repository"

2. **Link your local repository to GitHub**:
   - After creating the repository, GitHub will show instructions to push your existing repository
   - Run the following commands in your terminal, replacing `YOUR_USERNAME` with your GitHub username:

   ```
   git remote add origin https://github.com/YOUR_USERNAME/wechat-bot.git
   git branch -M main
   git push -u origin main
   ```

   - If you prefer to use SSH over HTTPS, use this format instead:
   
   ```
   git remote add origin git@github.com:YOUR_USERNAME/wechat-bot.git
   git branch -M main
   git push -u origin main
   ```

3. **Verify the connection**:
   - Run `git remote -v` to verify that the GitHub remote has been added
   - Visit your GitHub repository in the browser to confirm that your code has been pushed

## Additional Git Commands

Here are some useful Git commands for managing your repository:

- `git status`: Check the status of your working directory
- `git add <file>`: Stage specific file changes
- `git add .`: Stage all changes
- `git commit -m "Message"`: Commit staged changes with a message
- `git push`: Push committed changes to the remote repository
- `git pull`: Pull changes from the remote repository
- `git branch`: List branches
- `git checkout -b <branch-name>`: Create and switch to a new branch

## Working with the Virtual Environment

Remember to always activate your virtual environment before working on the project:

```
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

To install the project dependencies:

```
pip install -r requirements.txt
``` 