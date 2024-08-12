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
    private val mongoUrl by option(envvar = "MONGO_URL").required()
    private val remoteDriverUrl by option(envvar = "REMOTE_DRIVER_URL").required()
    private val everytimeId by option(envvar = "EVERY_TIME_ID").required()
    private val everytimePW by option(envvar = "EVERY_TIME_PASSWORD").required()

    private val sleepTime: Int by option("-st").int().default(5)
    private val scrollLimit: Int by option("-sl").int().default(3)
    private val majorNth: Int by option("-m").int().required()
    private val detailedMajorNthList: List<Int> by option("-dm").int().varargValues().required()
    private val argParseDebug: Boolean by option("-debug").boolean().default(false)

    private fun printArgs() {
        echo("mongoURL: ${mongoUrl}")
        echo("remoteDriverUrl: ${remoteDriverUrl}")
        echo("everytimeId: ${everytimeId}")
        echo("everytimePW: ${everytimePW}")
        echo("sleepTime: ${sleepTime}")
        echo("scrollLimit: ${scrollLimit}")
        echo("majorNth: ${majorNth}")
        echo("detailedMajor: ${detailedMajorNthList}")
    }

    override fun run() {
        if (argParseDebug) {
            printArgs()
        } else {
            scrape()
        }
    }

    fun scrape() {
        val timeout: Long = 10L
        // create remote web driver
        val driver: WebDriver = RemoteWebDriver(URL(remoteDriverUrl), ChromeOptions())
        val loginOut = LoginOut(driver, timeout, sleepTime, everytimeId, everytimePW)
        val mongoRepository: MongoRepository<LectureReviewWithMetaData> = MongoRepository.of<LectureReviewWithMetaData>(mongoUrl, "reviews")

        val lectureReviewScraper: LectureReviewScraper = LectureReviewScraper(
            driver,
            sleepTime,
            timeout,
            scrollLimit,
            mongoRepository,
            loginOut
        )

        lectureReviewScraper.login()
        for (detailedMajorNth in detailedMajorNthList) {
            lectureReviewScraper.scrape(majorNth, detailedMajorNth)
        }
        lectureReviewScraper.logout()
        driver.quit()
    }
}


fun main(args: Array<String>) = ReviewScrap().main(args)
