package org.example.request

import org.example.sleep
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.openqa.selenium.WebDriver
import org.slf4j.Logger
import org.slf4j.LoggerFactory

class LectureReviewRequest(
    private val driver: WebDriver,
) {
    private val logger: Logger = LoggerFactory.getLogger(LectureReviewRequest::class.java)

    fun request(urlPrefix: String): Document {
        driver.get("https://everytime.kr${urlPrefix}?tab=article")
        sleep(1)
        return Jsoup.parse(driver.pageSource)
    }

}