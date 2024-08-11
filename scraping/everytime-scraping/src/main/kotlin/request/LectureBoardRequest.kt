package org.example.request

import org.example.sleep
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.WebElement
import org.openqa.selenium.interactions.Actions
import org.openqa.selenium.support.ui.ExpectedConditions
import org.openqa.selenium.support.ui.WebDriverWait
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import java.time.Duration

object LectureBoardCssSelector {
    val lectureListOpenBtn: String = "#container > ul > li.button.search"
    val lectureListTable: String = "#subjects > div.list > table > tbody"
    val lectureListTr: String = "#subjects > div.list > table > tbody tr"
    val majorSelectBtn: String = "#subjects > div.filter > a:nth-child(4)"
}

object MajorSelectPageCssSelector {
    val sinchonBtn: String = "#subjectCategoryFilter > div > ul > li:nth-child(1)"
    fun majorBtn(nth: Int): String = "#subjectCategoryFilter > div > ul > ul.unfolded > li:nth-of-type(${nth})"
    fun detailMajorBtn(nth: Int): String = "#subjectCategoryFilter > div > ul > ul.unfolded > ul.unfolded > li:nth-of-type(${nth})"
}

class LectureBoardRequest(
    private val driver: WebDriver,
    private val timeout: Long,
    private val sleepTime: Int
) {
    private val lectureBoardPageUrl: String = "https://everytime.kr/timetable"
    private val logger: Logger = LoggerFactory.getLogger(LoginOut::class.java)
    private val actions: Actions = Actions(driver)

    fun clickBtn(selector: String) = WebDriverWait(driver, Duration.ofSeconds(timeout))
        .until(ExpectedConditions.elementToBeClickable(By.cssSelector(selector)))
        .click()

    /**
     *  전공/영역 선택 로직
     *  @param majorNth 교양기초, 대학교양, 자율선택, 문과대학 등등 의 nth-of-type 값
     *  @param detailMajorNth 문학과 예술, 경제학전공등등의 nth-of-type 값
     */
    fun selectMajor(majorNth: Int, detailMajorNth: Int) {
        // "전공-영역" 버튼 클릭
        sleep(sleepTime)
        clickBtn(LectureBoardCssSelector.majorSelectBtn)
        logger.info("opening subjectList major-select-popup-success")
        // 전공선택 팝업에서 "신촌" 버튼 클릭
        sleep(sleepTime)
        clickBtn(MajorSelectPageCssSelector.sinchonBtn)
        logger.info("clicked sinchonBtn")
        // 전공선택 팝업에서 "대학교 교양" 버튼 클릭
        sleep(sleepTime)
        clickBtn(MajorSelectPageCssSelector.majorBtn(majorNth))
        logger.info("clicked majorBtn")
        // 전공선택 팝업에서 "문학과 예술" 버튼 클릭
        sleep(sleepTime)
        clickBtn(MajorSelectPageCssSelector.detailMajorBtn(detailMajorNth))
        logger.info("clicked deatailMajorBtn")
    }

    fun scrollDown(): Int {
        val trList: MutableList<WebElement> = WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(
                ExpectedConditions.visibilityOfAllElementsLocatedBy(
                    By.cssSelector(LectureBoardCssSelector.lectureListTr)
                )
            )
        actions.moveToElement(trList.first()).scrollToElement(trList.last()).perform()
        return trList.size
    }

    fun request(majorNth: Int, detailMajorNth: Int): Document {
        // 시간표 페이지로 이동
        driver.get(lectureBoardPageUrl)

        // "수강신청 목록에서 검색"버튼 클릭
        sleep(sleepTime)
        WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(LectureBoardCssSelector.lectureListOpenBtn)))
            .click()
        logger.info("opening subjectList success")

        selectMajor(majorNth, detailMajorNth)

        // 강의 table 불러올때까지 기달리기
        sleep(sleepTime)
        WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector(LectureBoardCssSelector.lectureListTable)))

        var prevTrSize: Int = 0
        while (true) {
            sleep(sleepTime)
            val currentTrSize: Int = scrollDown()
            if (prevTrSize == currentTrSize)
                break
            prevTrSize = currentTrSize
        }
        logger.info("detected {} lectures", prevTrSize)


        val pageSource: String = driver.pageSource
        return Jsoup.parse(pageSource)
    }
}