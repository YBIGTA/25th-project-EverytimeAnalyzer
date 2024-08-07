package org.example

import org.example.parser.SubjectListParser
import org.example.parser.SubjectReviewPageParser
import org.example.request.LoginOut
import org.example.request.SubjectBoardRequest
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.openqa.selenium.chrome.ChromeDriver

fun mySleep(sleepTime: Int) {
    Thread.sleep(sleepTime.toLong() * 1000)
}

fun main() {
    val chromeDriver: ChromeDriver = ChromeDriver()

    val timeout: Int = 7
    val sleepTime: Int = 3
    val loginOut = LoginOut(chromeDriver, timeout.toLong(), sleepTime)
    val subjectBoardRequest = SubjectBoardRequest(chromeDriver, timeout.toLong(), sleepTime)


    // parse
    loginOut.loginPage()
    mySleep(sleepTime)
    val page: Document = subjectBoardRequest.requestSubjectListPage(2, 1)
    val parseUrl: List<String> = SubjectListParser.parseUrl(page)
    // parseUrl.forEach { println(it) }
    parseUrl
        .map { "https://everytime.kr${it}?tab=article" }
        .last()
        .also {
            chromeDriver.get(it)
            Thread.sleep(2000)
            val doc: Document = Jsoup.parse(chromeDriver.pageSource)
            val parse = SubjectReviewPageParser.parse(doc)
            println(parse)
        }
    // .map { SubjectReviewPageParser.parse(it) }
    // .first()
    // .forEach { println(it) }

    loginOut.logoutPage()

}
