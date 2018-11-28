echo "Enter your commit message:" 

read commit_msg

git commit -m "$commit_msg"

#git remote add origin git@github.com:ryancheley/rpi-kings.git

#git remote -v

git push
