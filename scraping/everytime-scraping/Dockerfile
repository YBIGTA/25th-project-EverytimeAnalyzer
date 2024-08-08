FROM eclipse-temurin:17
WORKDIR /app
COPY ./build/libs/selenium_demo-1.0-SNAPSHOT.jar foo.jar
ENTRYPOINT ["java", "-jar", "foo.jar", "--major_nth", "2", "--detailed_major_nth", "3", "--sleep_time", "7"]

