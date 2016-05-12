#!/usr/bin/sh
# Jenkinsのアップデートコマンド
systemctl stop jenkins
if [ -e /usr/share/jenkins/jenkins_old.war ];then
	rm /usr/share/jenkins/jenkins_old.war
fi
mv /usr/share/jenkins/jenkins.war /usr/share/jenkins/jenkins_old.war
wget http://mirrors.jenkins-ci.org/war/latest/jenkins.war /usr/share/jenkins/ 
systemctl start jenkins
