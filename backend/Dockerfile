FROM openjdk:17-jdk-slim

WORKDIR /app

# Copy Maven build output
COPY target/tool-1.0.0.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
