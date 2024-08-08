package org.example

import org.example.entity.LectureReview
import org.example.repo.MongoRepository
import org.example.request.LoginOut
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.remote.RemoteWebDriver
import java.net.URL

fun main(args: Array<String>) {
    // parse args
    val args: ReviewArgs = reviewArgParser(args)

    // get mongoUrl and remoteDriverUrl from env
    // mongoURL(in docker network): "mongodb://mongo_db:27017" mongoURL(in local): "mongodb://localhost:27017"
    // remoteDriverURL(in docker network): "http://selenium:4444" remoteDriverUrl(in local): "http://localhost:4444"
    val mongoUrl: String = System.getenv("MONGO_URL")
        ?: throw IllegalStateException("environment variable MONGO_URL is not set in system")
    val remoteDriverUrl: String = System.getenv("REMOTE_DRIVER_URL")
        ?: throw IllegalStateException("environment variable MONGO_URL is not set in system")
    val everytimeId: String = System.getenv("EVERY_TIME_ID")
        ?: throw IllegalStateException("environment variable EVERY_TIME_ID is not set in system")
    val everytimePassword: String = System.getenv("EVERY_TIME_PASSWORD")
        ?: throw IllegalStateException("environment variable EVERY_TIME_PASSWORD is not set in system")


    // prepare connection
    val mongoRepository: MongoRepository<LectureReview> = MongoRepository.of<LectureReview>(mongoUrl, "reviews")

    // create remote web driver
    val driver: WebDriver = RemoteWebDriver(URL(remoteDriverUrl), ChromeOptions())

    val timeout: Long = 7
    val sleepTime: Int = 3
    val loginOut = LoginOut(driver, timeout.toLong(), sleepTime, everytimeId, everytimePassword)

    val lectureReviewScraper: LectureReviewScraper = LectureReviewScraper(
        driver,
        sleepTime,
        timeout,
        mongoRepository,
        loginOut
    )

    lectureReviewScraper.login()
    lectureReviewScraper.scrape(args.majorNth, args.detailedMajorNth)
    lectureReviewScraper.logout()

    driver.quit()
}
