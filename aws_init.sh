sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
cat /etc/group | grep docker

sudo docker build -t python_cgi . --no-cache
#aws セキュリティグループ項目で8000ポートを開ける
sudo docker run -d -p 8000:8000 python_cgi

# 止めるとき
# sudo docker kill $(sudo docker ps -q)
