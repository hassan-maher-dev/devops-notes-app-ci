pipeline {

    agent any

    environment {
        // تحديد اسم الحساب واسم التطبيق (غير اسم الحساب لحسابك الفعلي)
        DOCKERHUB_USER = "hassanmaher2001"
        IMAGE_NAME = "devops-notes-app-ci"
        // استخدام رقم الـ Build الخاص بـ Jenkins ليكون هو الـ Tag للنسخة
        IMAGE_TAG = "${env.BUILD_ID}"
    }

    stages {

        stage('Checkout Code') {

            steps {

                echo " Checking out repository..."

                // غير هذا الرابط برابط المستودع الخاص بتطبيق الملاحظات
                git branch: 'main', url: 'https://github.com/hassan-maher-dev/NotesApp.git'

            }

        }

        stage('Build Docker Image') {

            steps {

                echo " Building Docker image..."

                sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"

            }

        }

        stage('Push to DockerHub') {

            steps {

                echo " Pushing Docker image to DockerHub..."

                // استخدام الـ Credentials التي أنشأناها في Jenkins
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    
                    // تسجيل الدخول بطريقة آمنة
                    sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                    
                    // رفع النسخة برقم الـ Build
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    
                    // رفع نسخة كـ latest
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"

                }

            }

        }

    }

    post {

        always {

            echo " Cleaning up workspace and local Docker images to save disk space..."
            
            // مسح الـ Images من سيرفر Jenkins بعد رفعها لتوفير المساحة
            sh "docker rmi ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} || true"
            sh "docker rmi ${DOCKERHUB_USER}/${IMAGE_NAME}:latest || true"
            
            // تنظيف مجلد العمل
            deleteDir() 

        }

        success {

            echo " Pipeline completed successfully! Image is on DockerHub."

        }

        failure {

            echo " Pipeline failed! Check the logs."

        }

    }

}