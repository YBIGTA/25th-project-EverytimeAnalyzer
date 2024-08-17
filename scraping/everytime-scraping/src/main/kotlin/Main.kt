package org.example

import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.core.subcommands
import com.github.ajalt.clikt.parameters.options.default
import com.github.ajalt.clikt.parameters.options.option
import com.github.ajalt.clikt.parameters.options.required
import com.github.ajalt.clikt.parameters.options.varargValues
import com.github.ajalt.clikt.parameters.types.boolean
import com.github.ajalt.clikt.parameters.types.int
import org.example.entity.LectureInfo
import org.example.entity.LectureReviewWithMetaData
import org.example.parser.LectureTableParser
import org.example.repo.MongoRepository
import org.example.request.LectureBoardRequest
import org.example.request.LoginOut
import org.jsoup.nodes.Document
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.remote.RemoteWebDriver
import java.net.URL

abstract class DefaultArgsParser(name: String) : CliktCommand(name) {
    protected val mongoHost by option(envvar = "MONGO_HOST").required()
    protected val mongoUsername by option(envvar = "MONGO_USERNAME").required()
    protected val mongoPassword by option(envvar = "MONGO_PASSWORD").required()
    protected val mongoPort by option(envvar = "MONGO_PORT").int().required()

    protected val remoteDriverUrl by option(envvar = "REMOTE_DRIVER_URL").required()
    protected val everytimeId by option(envvar = "EVERY_TIME_ID").required()
    protected val everytimePW by option(envvar = "EVERY_TIME_PASSWORD").required()

    protected val sleepTime: Int by option("-st").int().default(5)
    protected val scrollLimit: Int by option("-sl").int().default(3)
    protected val majorNth: Int by option("-m").int().required()
    protected val detailedMajorNthList: List<Int> by option("-dm").int().varargValues().required()
    protected val argParseDebug: Boolean by option("-debug").boolean().default(false)

    protected fun printArgs() {
        echo("mongoHost: ${mongoHost}")
        echo("mongoUsername: ${mongoUsername}")
        echo("mongoPassword: ${mongoPassword}")
        echo("mongoPort: ${mongoPort}")

        echo("remoteDriverUrl: ${remoteDriverUrl}")
        echo("everytimeId: ${everytimeId}")
        echo("everytimePW: ${everytimePW}")
        echo("sleepTime: ${sleepTime}")
        echo("scrollLimit: ${scrollLimit}")
        echo("majorNth: ${majorNth}")
        echo("detailedMajor: ${detailedMajorNthList}")
    }

    abstract fun scrape()

    override fun run() {
        if (argParseDebug) {
            printArgs()
        } else {
            scrape()
        }
    }
}

class LectureInfoScrape : DefaultArgsParser("lecture") {
    override fun scrape() {
        val timeout: Long = 10L
        // create remote web driver
        val driver: WebDriver = RemoteWebDriver(URL(remoteDriverUrl), ChromeOptions())
        val loginOut = LoginOut(driver, timeout, sleepTime, everytimeId, everytimePW)
        val mongoUrl = mongoUrlBuilder(mongoHost, mongoPort, mongoUsername, mongoPassword)
        val mongoRepository: MongoRepository<LectureInfo> = MongoRepository.of<LectureInfo>(mongoUrl, "lecture")
        val lectureBoardRequest: LectureBoardRequest = LectureBoardRequest(driver, timeout, sleepTime)


        loginOut.loginPage()
        sleep(sleepTime)

        for (detailedMajorNth in detailedMajorNthList) {
            val doc: Document = lectureBoardRequest.request(majorNth, detailedMajorNth)
            val lectureInfoList: List<LectureInfo> = LectureTableParser.parse(doc)
            lectureInfoList
                .forEach {
                    mongoRepository.insert(it, "inserting lecture [id:${it.code}]")
                }
            sleep(sleepTime)
        }
        loginOut.logoutPage()
        driver.quit()
    }
}

class ReviewScrap : DefaultArgsParser("review") {
    override fun scrape() {
        val timeout: Long = 10L
        // create remote web driver
        val driver: WebDriver = RemoteWebDriver(URL(remoteDriverUrl), ChromeOptions())
        val loginOut = LoginOut(driver, timeout, sleepTime, everytimeId, everytimePW)
        val mongoUrl = mongoUrlBuilder(mongoHost, mongoPort, mongoUsername, mongoPassword)
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

class EntryParser : CliktCommand() {
    override fun run() = Unit
}


fun main(args: Array<String>) = EntryParser()
    .subcommands(ReviewScrap(), LectureInfoScrape())
    .main(args)

