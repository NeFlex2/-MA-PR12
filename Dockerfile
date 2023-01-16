name: Docker Image CI

on:
  push:
    branches: [ "master" ]

jobs:
  build_and_push:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      # Build Image
      - name: Build Docker Image
        run: docker build . --file Dockerfile -t ortreke/ma-docs-service:latest

      # Test container
      - name: Run Docker Container
        run: docker run -p 8000:80 -d ortreke/ma-docs-service:latest
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install requirements
        run: pip install pytest requests
      - name: Run tests
        run: pytest

      # Push tag
      - name: Login into Docker Hub
        uses: docker/login-action@f054a8b539a109f9f41c372932f1ae047eff08c9
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Push tag to Docker Hub
        run: docker push ortreke/ma-docs-service:latest