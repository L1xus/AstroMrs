FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Install OpenJDK for PySpark
RUN apt-get update && apt-get install -y openjdk-17-jdk && apt-get clean

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "main.py"]
