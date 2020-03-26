import click
import pkgutil
import os
import re

@click.option('--image-name', default='dockerized-app', help='Image name to use for build.')
@click.option('--port', type=int, default=-1, help='The port to run the image on.')
@click.option('--app_type', required=True, help='The type of app(PYTHON_FLASK, NODE_JS, JAVA_SPRING_BOOT).')
@click.command()
def cli(image_name, port, app_type):
    """Main cli"""

    click.echo(app_type + ' app detected')

    # Port was not passed in argument, set default values based on app_type
    if (port == -1):
        if (app_type == 'PYTHON_FLASK'):
            port = 5000
        else:
            port = 8080

    if(app_type == 'NODE_JS'):
        handle_nodejs(image_name, port)
    elif(app_type == 'JAVA_SPRING_BOOT'):
        handle_java_spring_boot(image_name, port)
    elif(app_type == 'PYTHON_FLASK'):
        handle_python_flask(image_name, port)

def handle_java_spring_boot(image_name, port):
    # Generate Dockerfile
    click.echo('Generating Dockerfile...')
    if (not os.path.exists('target')):
        click.echo('No target/ present')
        exit(1)
    found_file = ''
    for filename in os.listdir('target/'):
        if re.search('.*\.jar', filename):
            found_file = filename
            break
    if (found_file == ''):
        click.echo('No jar file present. Make sure your target/ contains a jar file')
        exit(1)
    text = pkgutil.get_data(__name__, "templates/Java.Dockerfile").decode()

    open("Dockerfile", "w").writelines([l for l in text])
    click.echo('Dockerfile generated')

    # Build Docker image
    click.echo('Building Docker image...')
    os.system('docker build -t {} .'.format(image_name))
    click.echo('Built image {}'.format(image_name))

    # Run Docker image
    click.echo('Running Docker image...')
    os.system('docker run -p {}:{} {}'.format(8080, port, image_name))

def handle_python_flask(image_name, port):
    python_entrypoint_file = 'app.py'

    # Generate Dockerfile
    click.echo('Generating Dockerfile...')
    python_entrypoint_file = click.prompt('Enter python entrypoint file')
    os.environ["FLASK_ENTRYPOINT_FILE"] = python_entrypoint_file
    text = pkgutil.get_data(__name__, "templates/Python-Flask.Dockerfile").decode()

    open("Dockerfile", "w").writelines([l for l in text])
    click.echo('Dockerfile generated')

    # Build Docker image
    click.echo('Building Docker image...')
    os.system('docker build -t {} --build-arg FLASK_ENTRYPOINT_FILE={} .'.format(image_name, python_entrypoint_file))
    click.echo('Built image {}'.format(image_name))

    # Run Docker image
    click.echo('Running Docker image...')
    os.system('docker run -p {}:{} {}'.format(5000, port, image_name))

def handle_nodejs(image_name, port):
    # Generate Dockerfile
    click.echo('Generating Dockerfile...')
    text = pkgutil.get_data(__name__, "templates/NodeJS.Dockerfile").decode()
    open("Dockerfile", "w").writelines([l for l in text])
    click.echo('Dockerfile generated')

    # Build Docker image
    click.echo('Building Docker image...')
    os.system('docker build -t {} .'.format(image_name))
    click.echo('Built image {}'.format(image_name))

    # Run Docker image
    click.echo('Running Docker image...')
    os.system('docker run -it -p {}:{} {}'.format(8080, port, image_name))
