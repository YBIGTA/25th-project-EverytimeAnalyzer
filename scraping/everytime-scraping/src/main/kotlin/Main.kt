package org.example

import org.example.entity.EverytimeArticle
import org.example.repo.MongoRepository
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.remote.RemoteWebDriver
import java.net.URL

fun main(args: Array<String>) {
    // parse args
    val args: Args = articleArgParser(args)

    val mongoUrl: String = "mongodb://mongo_db:27017"
    val remoteDriverUrl: String = "http://selenium:4444"
    // prepare connection
    // val mongoUrl: String = "mongodb://localhost:27017"
    val mongoRepository: MongoRepository<EverytimeArticle> = MongoRepository.of<EverytimeArticle>(mongoUrl, "article")

    // create remote web driver
    val driver: WebDriver = RemoteWebDriver(URL(remoteDriverUrl), ChromeOptions())

    // create driver
    val parser: EverytimeParser = EverytimeParser(
        driver,
        10,
        args.urlPrefix,
        args.sleepTime,
        mongoRepository
    )

    // parse
    parser.login()
    parser.parse(args.startPage, args.pageNum)
    parser.logout()

    // need to close session (REQUIRED!!)
    driver.quit()
}
