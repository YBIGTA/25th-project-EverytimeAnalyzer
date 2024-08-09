FROM eclipse-temurin:17

RUN apt-get update

WORKDIR /app
COPY ./build/libs/selenium_demo-1.0-SNAPSHOT.jar scraper.jar

#ENTRYPOINT ["java", "-jar", "scraper.jar", "--major_nth", "2", "--detailed_major_nth", "3", "--sleep_time", "7"]
ENTRYPOINT ["tail", "-f", "/dev/null"]
