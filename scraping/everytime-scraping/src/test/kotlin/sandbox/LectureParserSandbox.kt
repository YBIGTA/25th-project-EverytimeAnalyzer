package sandbox

import org.example.entity.LectureInfo
import org.example.parser.LectureTableParser
import org.example.repo.MongoRepository
import org.example.request.LectureBoardRequest
import org.example.request.LoginOut
import org.example.sleep
import org.jsoup.nodes.Document
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.remote.RemoteWebDriver
import java.net.URL

fun main() {
    val remoteDriverUrl = "http://localhost:4444"
    val everytimeId = "ticktacktok135"
    val everytimePW = "park6240"
    val sleepTime: Int = 5
    val timeout: Long = 10L
    val mongoUrl = "mongodb://localhost:27017"
    // create remote web driver
    val driver: WebDriver = RemoteWebDriver(URL(remoteDriverUrl), ChromeOptions())
    val loginOut = LoginOut(driver, timeout, sleepTime, everytimeId, everytimePW)
    val lectureBoardRequest: LectureBoardRequest = LectureBoardRequest(driver, timeout, sleepTime)
    val mongoRepository: MongoRepository<LectureInfo> = MongoRepository.of<LectureInfo>(mongoUrl, "reviews")

    loginOut.loginPage()
    sleep(sleepTime)
    var doc: Document = lectureBoardRequest.request(2, 3)
    val lectureInfoList: List<LectureInfo> = LectureTableParser.parse(doc)

    lectureInfoList.forEach {
        println(it)
        mongoRepository.insert(it, "foo")
    }

    sleep(sleepTime)
    loginOut.logoutPage()
    driver.quit()
}


