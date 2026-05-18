pipeline {
agent any

stages {

stage('Checkout Code') {
            steps {
                git branch: 'main',
                url: 'YOUR_GITHUB_REPO_URL'
            }
        }
        
stage('Install Dependencies') {
steps {
bat 'pip install -r requirements.txt'
}
}

// stage('Test') {
// steps {
// bat 'pytest'
// }
// }

stage('Build Docker Image') {
steps {
bat 'docker build -t airbnb-clone .'
}
}

stage('Deploy Container') {
steps {
bat '''
docker stop airbnb || exit 0
docker rm airbnb || exit 0
docker run -d -p 5000:5000 ^
-v airbnb_data:/app ^
--name airbnb ^
airbnb-clone
'''
}
}
stage('Push Image'){
steps{
     withCredentials([usernamePassword(
            credentialsId:'dockerhub-creds',
            usernameVariable:'DOCKER_USER',
            passwordVariable:'DOCKER_PASS'
        )]) {
            bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
            bat 'docker tag airbnb-clone abhiramraghunand/airbnb-clone:latest'
            bat 'docker push abhiramraghunand/airbnb-clone:latest'
        }
}
}

stage('Run Prometheus') {
    steps {
        bat '''
        docker stop prometheus || exit 0
        docker rm prometheus || exit 0

        docker run -d ^
        --name prometheus ^
        -p 9090:9090 ^
        -v %WORKSPACE%\\prometheus.yml:/etc/prometheus/prometheus.yml ^
        prom/prometheus
        '''
    }
}

}
}
