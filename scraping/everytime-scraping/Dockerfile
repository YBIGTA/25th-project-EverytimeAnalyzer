FROM eclipse-temurin:17
WORKDIR /app
COPY ./build/libs/selenium_demo-1.0-SNAPSHOT.jar foo.jar
ENTRYPOINT ["java", "-jar", "foo.jar", "--url_prefix", "385546" ,"--start_page", "10", "--page_num", "0" ,"--sleep_time" ,"5"]