git pull origin main
rm -rf .git/
git init
git remote add origin git@github.com:demobin8/notes.git
git add --all
git commit -am 'reset commits'
git branch -m master main
git push -f origin main
