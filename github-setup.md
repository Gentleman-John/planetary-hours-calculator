# GitHub Setup Instructions

Follow these steps to push your Planetary Hours Calculator to GitHub:

## 1. Initialize Git Repository

```bash
git init
```

## 2. Add all files to repository

```bash
git add .
```

## 3. Make initial commit

```bash
git commit -m "Initial commit: Planetary Hours Calculator with database integration"
```

## 4. Create GitHub Repository

1. Go to GitHub.com and sign in to your account
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository (e.g., "planetary-hours-calculator")
4. Add a description: "A Python web application that calculates planetary hours and their ruling entities according to The Greater Key of Solomon."
5. Choose public or private visibility
6. Do NOT initialize with README, .gitignore, or license as we already have these
7. Click "Create repository"

## 5. Connect local repository to GitHub

Replace `yourusername` with your actual GitHub username:

```bash
git remote add origin https://github.com/yourusername/planetary-hours-calculator.git
```

## 6. Push to GitHub

```bash
git push -u origin master
```

## 7. Check Your Repository

Your code should now be on GitHub. Visit `https://github.com/yourusername/planetary-hours-calculator` to confirm.

## Important Notes

1. Make sure to not include sensitive information like API keys or passwords in your repository.
2. The `.gitignore` file is already set up to exclude Python cache files and virtual environments.
3. Make sure to update the repository URL in the README.md to match your actual GitHub repository.