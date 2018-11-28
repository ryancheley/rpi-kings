git add $1

echo "Enter your commit message:" 

read commit_msg

git commit -m "$commit_msg"

git push
