package org.example.request

import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.support.ui.ExpectedConditions
import org.openqa.selenium.support.ui.WebDriverWait
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import java.time.Duration

class ArticleRequest(
    private val driver: WebDriver,
    private val timeout: Long
) {
    private val logger: Logger = LoggerFactory.getLogger(ArticleListRequest::class.java)
    fun request(url: String): Document {
        logger.info("requesting article: {}", url)

        driver.get(url)

        WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("#container > div.wrap.articles > article")))

        val pageSource: String = driver.pageSource
        return Jsoup.parse(pageSource)
    }
}