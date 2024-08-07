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

class ArticleListRequest(
    private val driver: WebDriver,
    private val urlPrefix: String,
    private val timeout: Long
) {
    private val hrefSelector: String = "#container > div.wrap.articles > article > a"
    private val logger: Logger = LoggerFactory.getLogger(ArticleListRequest::class.java)

    fun getArticleList(page: Int): List<String> {
        logger.info("requesting page:{}", page)

        driver.get("https://everytime.kr/${urlPrefix}/p/${page}")

        WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(ExpectedConditions.presenceOfElementLocated(By.cssSelector(hrefSelector)))

        val pageSource: String = driver.pageSource
        val dom: Document = Jsoup.parse(pageSource)
        val map: List<String> = dom.select(hrefSelector)
            .map { it.attr("href") }
        return map
    }
}