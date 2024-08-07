package org.example

import org.example.entity.SubjectReview
import org.example.parser.SubjectListParser
import org.example.parser.SubjectReviewPageParser
import org.example.repo.MongoRepository
import org.example.request.LoginOut
import org.example.request.SubjectBoardRequest
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
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
    val mongoRepository: MongoRepository<SubjectReview> = MongoRepository.of<SubjectReview>(mongoUrl, "reviews")

    // create remote web driver
    val driver: WebDriver = RemoteWebDriver(URL(remoteDriverUrl), ChromeOptions())

    val timeout: Int = 7
    val sleepTime: Int = 3
    val loginOut = LoginOut(driver, timeout.toLong(), sleepTime, everytimeId, everytimePassword)
    val subjectBoardRequest = SubjectBoardRequest(driver, timeout.toLong(), sleepTime)

    // login
    loginOut.loginPage()
    sleep(sleepTime)

    // 에브리타임 강의 목록 스크래핑
    val subjectListPage: Document = subjectBoardRequest.requestSubjectListPage(args.majorNth, args.detailedMajorNth)

    // 개별 강의후기 페이지 url과 과목코드 추출
    val reviewPageUrls: List<String> = SubjectListParser.parseUrl(subjectListPage)
    val subjectCodes: List<String> = SubjectListParser.parseSubjectCode(subjectListPage)
    assert(reviewPageUrls == subjectCodes)

    // 개별 강의후기 페이지 스크래핑
    for (i in reviewPageUrls.indices) {
        driver.get("https://everytime.kr${reviewPageUrls[i]}?tab=article")
        sleep(sleepTime)
        val doc: Document = Jsoup.parse(driver.pageSource)
        val parse = SubjectReviewPageParser.parse(subjectCodes[i], doc)
        parse.forEach { mongoRepository.insert(it, "inserting review id=${it.id}, subject_code=${it.code}") }
    }


    // logout
    loginOut.logoutPage()
    // need to close session (REQUIRED!!)
    driver.quit()
}
