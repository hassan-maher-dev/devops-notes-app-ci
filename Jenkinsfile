pipeline {
    agent any

    environment {
        // تأكد أن هذه القيم مطابقة لحسابك
        DOCKERHUB_USER = "hassanmaher2001" 
        IMAGE_NAME = "devops-notes-app-ci"
        IMAGE_TAG = "${env.BUILD_ID}"
    }

    stages {
        // 1. مرحلة البناء (لا نحتاج Checkout هنا لأن جينكينز يقوم به تلقائياً)
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                // تنفيذ الأمر مباشرة
                sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        // 2. مرحلة الرفع لـ DockerHub
        stage('Push to DockerHub') {
            steps {
                echo "Logging into DockerHub and pushing image..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up local images from Jenkins container..."
            // إضافة || true لضمان عدم فشل البايبلاين لو الصورة غير موجودة
            sh "docker rmi ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} || true"
            sh "docker rmi ${DOCKERHUB_USER}/${IMAGE_NAME}:latest || true"
            deleteDir()
        }
        success {
            echo "Hooray! Pipeline Finished Successfully."
        }
        failure {
            echo "Something went wrong. Check the logs above."
        }
    }
}