package org.example

import org.example.parser.ArticlePageParser
import org.example.repo.MongoRepository
import org.example.request.ArticleListRequest
import org.example.request.ArticleRequest
import org.example.request.LoginOut
import org.jsoup.nodes.Document
import org.openqa.selenium.WebDriver
import org.slf4j.Logger
import org.slf4j.LoggerFactory

class EverytimeParser(
    driver: WebDriver,
    private val timeout: Int,
    private val urlPrefix: String,
    private val sleepTime: Int,
    private val mongoRepository: MongoRepository
) {
    private val loginOut: LoginOut = LoginOut(driver, timeout.toLong(), 5)
    private val articleListRequest: ArticleListRequest = ArticleListRequest(driver, urlPrefix, timeout.toLong())
    private val articleRequest: ArticleRequest = ArticleRequest(driver, timeout.toLong())
    private val logger: Logger = LoggerFactory.getLogger(EverytimeParser::class.java)

    fun sleep() = Thread.sleep(sleepTime.toLong() * 1000)

    fun login() {
        loginOut.loginPage()
        sleep()
    }


    fun logout() {
        sleep()
        loginOut.logoutPage()
        println("logout")
    }

    fun parse(startPage: Int, pageNum: Int) {
        // get article url list
        val pageUrlList: List<String> = IntRange(startPage, startPage + pageNum)
            .map { page ->
                sleep()
                articleListRequest.getArticleList(page)
            }
            .flatten()
            .map { "https://everytime.kr" + it }

        // request each article
        // store to mongodb
        for (articleUrl in pageUrlList) {
            sleep()
            val request: Document = articleRequest.request(articleUrl)

            try {
                val parsedArticle = ArticlePageParser.parseArticle(request)
                mongoRepository.insertArticle(parsedArticle)
            } catch (e: NullPointerException) {
                logger.warn("parsing error when parsing:{}", articleUrl)
            }

        }
    }
}