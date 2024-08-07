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
    val reviewPageUrls: List<String> = SubjectListParser.parseUrl(page)
    val subjectCodes: List<String> = SubjectListParser.parseSubjectCode(page)
    assert(reviewPageUrls == subjectCodes)

    for (i in reviewPageUrls.indices) {
        chromeDriver.get("https://everytime.kr${reviewPageUrls[i]}?tab=article")
        Thread.sleep(2000)
        val doc: Document = Jsoup.parse(chromeDriver.pageSource)
        val parse = SubjectReviewPageParser.parse(subjectCodes[i], doc)
        println(parse.size)
    }

    loginOut.logoutPage()

}
