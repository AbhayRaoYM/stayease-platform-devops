pipeline {
agent any

stages {

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
bat 'docker build -t airbnb-python .'
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
    bat 'docker tag airbnb-clone abhiramraghunand/airbnb-clone:latest'

    bat 'docker push abhiramraghunand/airbnb-clone:latest'
}

stage('Start Monitoring') {
    steps {

        bat '''
        docker stop prometheus || exit 0
        docker rm prometheus || exit 0

        docker stop grafana || exit 0
        docker rm grafana || exit 0

        docker run -d ^
        -p 9090:9090 ^
        -v %cd%/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml ^
        --name prometheus ^
        prom/prometheus

        docker run -d ^
        -p 3000:3000 ^
        --name grafana ^
        grafana/grafana
        '''
    }
}
}
}
}