package org.example

import org.bson.types.ObjectId
import org.example.entity.LectureReviewWithMetaData
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
    driver: WebDriver,
    private val sleepTime: Int,
    timeout: Long,
    private val mongoRepository: MongoRepository<LectureReviewWithMetaData>,
    private val loginOut: LoginOut
) {
    private val logger: Logger = LoggerFactory.getLogger(LectureReviewScraper::class.java)
    private val lectureBoardRequest = LectureBoardRequest(driver, timeout, sleepTime)
    private val lectureReviewRequest = LectureReviewRequest(driver, timeout, sleepTime)

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
            logger.info("[${i + 1}/${reviewPageUrls.size}] requested ${reviewPageUrls[i]}")

            val reviewWithMetaDataList = LectureReviewPageParser
                .parse(lectureCodes[i], parsedReviewPage)
                .map { LectureReviewWithMetaData(ObjectId(), lectureCodes[i], majorNth, detailedMajorNth, it) }

            reviewWithMetaDataList.forEach { mongoRepository.insert(it, "inserting review id=${it.id}, subject_code=${it.lectureCode}") }

            logger.info("inserted reviews to db subject-code:${lectureCodes[i]} insert_count:${reviewWithMetaDataList.size} ")
        }
    }
}