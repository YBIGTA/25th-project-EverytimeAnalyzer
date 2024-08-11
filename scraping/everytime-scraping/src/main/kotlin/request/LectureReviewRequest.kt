package org.example.request

import org.example.sleep
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.openqa.selenium.By
import org.openqa.selenium.TimeoutException
import org.openqa.selenium.WebDriver
import org.openqa.selenium.WebElement
import org.openqa.selenium.interactions.Actions
import org.openqa.selenium.support.ui.ExpectedConditions
import org.openqa.selenium.support.ui.WebDriverWait
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import java.time.Duration


object LectureReviewSelector{
    val review = "body > div:nth-child(1) > div > div.pane > div > div.articles .text"
}
class LectureReviewRequest(
    private val driver: WebDriver,
    private val timeout: Long,
    private val sleepTime: Int
) {
    private val logger: Logger = LoggerFactory.getLogger(LectureReviewRequest::class.java)
    private val actions: Actions = Actions(driver)

    fun scrollDown(): Int {
        val reviews: MutableList<WebElement> = WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(
                ExpectedConditions.visibilityOfAllElementsLocatedBy(
                    By.cssSelector(LectureReviewSelector.review)
                )
            )
        actions.moveToElement(reviews.first()).scrollToElement(reviews.last()).perform()
        return reviews.size
    }

    fun request(urlPrefix: String): Document {
        driver.get("https://everytime.kr${urlPrefix}?tab=article")
        sleep(1)
        var prevReviewSize: Int = 0
        try {
            while (true) {
                sleep(sleepTime)
                val currentTrSize: Int = scrollDown()
                if (prevReviewSize == currentTrSize)
                    break
                prevReviewSize = currentTrSize
            }
        } catch (e: TimeoutException) {
            if (prevReviewSize != 0)
                logger.warn("error occur when scraping page: ${urlPrefix} error: ${e}")
        }
        logger.info("detected {} reviews", prevReviewSize)
        return Jsoup.parse(driver.pageSource)
    }

}