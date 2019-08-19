node {
    try {
        stage('Pre-build') {
            checkout scm
        }

        stage 'Build'
        def image = docker.build "door-${BUILD_TAG.toLowerCase()}"

        stage('Lint') {
            image.inside {
                sh '''
                pip install mypy pycodestyle pydocstyle
                pycodestyle --max-line-length=120 /app
                pydocstyle /app/door
                mypy --strict --ignore-missing-imports /app/door
                '''
            }
        }
    }
    catch (ex) {
        currentBuild.result = 'FAILURE'
    }
    finally {
        stage('Cleanup') {
            cleanWs()
            sh "docker rmi door-${BUILD_TAG.toLowerCase()}"
        }
    }
}
