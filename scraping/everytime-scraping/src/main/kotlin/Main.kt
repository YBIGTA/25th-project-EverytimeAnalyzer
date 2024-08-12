package org.example

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.parameters.options.default
import com.github.ajalt.clikt.parameters.options.option
import com.github.ajalt.clikt.parameters.options.required
import com.github.ajalt.clikt.parameters.options.varargValues
import com.github.ajalt.clikt.parameters.types.boolean
import com.github.ajalt.clikt.parameters.types.int
import org.example.entity.LectureReviewWithMetaData
import org.example.repo.MongoRepository
import org.example.request.LoginOut
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.remote.RemoteWebDriver
import java.net.URL

class ReviewScrap : CliktCommand() {
    val mongoUrl by option(envvar = "MONGO_URL")
    val remoteDriverUrl by option(envvar = "REMOTE_DRIVER_URL")
    val everytimeId by option(envvar = "EVERY_TIME_ID")
    val everytimePW by option(envvar = "EVERY_TIME_PASSWORD")

    val sleepTime: Int by option("-st").int().default(5)
    val scrollLimit: Int by option("-sl").int().default(3)
    val majorNth: Int by option("-m").int().required()
    val detailedMajorList: List<Int> by option("-dm").int().varargValues().required()
    val argParseDebug: Boolean by option("-debug").boolean().default(false)

    override fun run() {
        if (argParseDebug) {
            echo("mongoURL: ${mongoUrl}")
            echo("remoteDriverUrl: ${remoteDriverUrl}")
            echo("everytimeId: ${everytimeId}")
            echo("everytimePW: ${everytimePW}")
            echo("sleepTime: ${sleepTime}")
            echo("scrollLimit: ${scrollLimit}")
            echo("majorNth: ${majorNth}")
            echo("detailedMajor: ${detailedMajorList}")
            return
        }
    }
}


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
    val mongoRepository: MongoRepository<LectureReviewWithMetaData> = MongoRepository.of<LectureReviewWithMetaData>(mongoUrl, "reviews")

    // create remote web driver
    val driver: WebDriver = RemoteWebDriver(URL(remoteDriverUrl), ChromeOptions())

    val timeout: Long = 7
    val sleepTime: Int = args.sleepTime
    val loginOut = LoginOut(driver, timeout.toLong(), sleepTime, everytimeId, everytimePassword)

    val lectureReviewScraper: LectureReviewScraper = LectureReviewScraper(
        driver,
        sleepTime,
        timeout,
        args.scrollLimit,
        mongoRepository,
        loginOut
    )

    lectureReviewScraper.login()
    for (i in args.detailedMajorNthList.indices) {
        lectureReviewScraper.scrape(args.majorNth, args.detailedMajorNthList[i])
    }
    lectureReviewScraper.logout()

    driver.quit()
}
