pipeline {
    agent any

    environment {
        // تأكد أن هذه القيم مطابقة لحسابك
        DOCKERHUB_USER = "hassanmaher2001" 
        IMAGE_NAME = "devops-notes-app-ci"
        IMAGE_TAG = "${env.BUILD_ID}"
        // إضافة رابط مستودع الـ GitOps الخاص بك
        GITOPS_REPO = "github.com/hassan-maher-dev/notes-app-gitops.git"
    }

    stages {
        // 1. مرحلة البناء
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        // 2. مرحلة الرفع لـ DockerHub
        stage('Push to DockerHub') {
            steps {
                echo "Logging into DockerHub and pushing image..."
                // استخدام الـ ID الخاص بك 'dockerhub-creds'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }

        // 3. المرحلة الجديدة: تحديث مستودع الـ GitOps
        stage('Update GitOps Manifests') {
            steps {
                echo "Updating GitOps Repository for ArgoCD..."
                // يجب إنشاء Credential في جينكينز باسم 'github-token'
                withCredentials([usernamePassword(credentialsId: 'github-token', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh '''
                        # استنساخ مستودع الـ GitOps
                        git clone https://$GIT_USERNAME:$GIT_PASSWORD@${GITOPS_REPO}
                        
                        cd notes-app-gitops

                        # إعداد بيانات المستخدم الخاصة بجينكينز ليتمكن من عمل Commit
                        git config user.email "jenkins@devops.com"
                        git config user.name "Jenkins CI"

                        # استبدال الـ Tag القديم بالـ Tag الجديد في ملف deployment.yaml
                        sed -i "s|image: ${DOCKERHUB_USER}/${IMAGE_NAME}:.*|image: ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}|g" deployment.yaml

                        # حفظ التعديلات ورفعها لمستودع الـ GitOps
                        git add deployment.yaml
                        git commit -m "Auto-update image tag to build ${IMAGE_TAG}"
                        git push origin main
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up local images from Jenkins container..."
            sh "docker rmi ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} || true"
            sh "docker rmi ${DOCKERHUB_USER}/${IMAGE_NAME}:latest || true"
            deleteDir()
        }
        success {
            echo "Hooray! Pipeline Finished Successfully. ArgoCD will sync the changes shortly."
        }
        failure {
            echo "Something went wrong. Check the logs above."
        }
    }
}