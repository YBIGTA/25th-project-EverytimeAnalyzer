package org.example

import org.example.entity.LectureReview
import org.example.parser.LectureListParser
import org.example.parser.LectureReviewPageParser
import org.example.repo.MongoRepository
import org.example.request.LectureBoardRequest
import org.example.request.LectureReviewRequest
import org.example.request.LoginOut
import org.jsoup.nodes.Document
import org.openqa.selenium.WebDriver
import org.slf4j.Logger
import org.slf4j.LoggerFactory

class LectureReviewScraper(
    private val driver: WebDriver,
    private val sleepTime: Int,
    timeout: Long,
    private val mongoRepository: MongoRepository<LectureReview>,
    private val loginOut: LoginOut
) {
    private val logger: Logger = LoggerFactory.getLogger(LectureReviewScraper::class.java)
    private val lectureBoardRequest = LectureBoardRequest(driver, timeout, sleepTime)
    private val lectureReviewRequest = LectureReviewRequest(driver)

    fun login() {
        loginOut.loginPage()
        sleep(sleepTime)
    }

    fun logout() {
        sleep(sleepTime)
        loginOut.logoutPage()
        println("logout")
    }


    fun scrape(majorNth: Int, detailedMajorNth: Int) {
        val lectureListPage: Document = lectureBoardRequest.lectureListPageRequest(majorNth, detailedMajorNth)

        logger.info("requesting lecture ")

        val reviewPageUrls: List<String> = LectureListParser.parseUrl(lectureListPage)
        val lectureCodes: List<String> = LectureListParser.parseLectureCode(lectureListPage)
        assert(reviewPageUrls == lectureCodes)

        for (i in reviewPageUrls.indices) {
            sleep(sleepTime)
            val parsedReviewPage = lectureReviewRequest.request(reviewPageUrls[i])

            val reviews: List<LectureReview> = LectureReviewPageParser.parse(lectureCodes[i], parsedReviewPage)
            logger.info("[${i}/${reviewPageUrls.size}] requested ${reviewPageUrls[i]}")

            reviews.forEach { mongoRepository.insert(it, "inserting review id=${it.id}, subject_code=${it.lectureCode}") }
            logger.info("inserted reviews to db subject-code:${lectureCodes[i]} insert_count:${reviews.size} ")
        }
    }
}