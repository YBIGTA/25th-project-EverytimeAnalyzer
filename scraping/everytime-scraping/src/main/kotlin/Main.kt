package org.example

import org.example.repo.MongoRepository
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.remote.RemoteWebDriver
import java.net.URL

fun main(args: Array<String>) {
    // parse args
    val args: Args = parseArgs(args)

    val mongoUrl: String = "mongodb://mongo:27017"
    val remoteDriverUrl: String = "http://selenium:4444"
    // prepare connection
    // val mongoUrl: String = "mongodb://localhost:27017"
    val mongoRepository: MongoRepository = MongoRepository(mongoUrl)

    // create remote web driver
    // val remoteDriverUrl: String = "http://127.0.0.1:4444"
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
