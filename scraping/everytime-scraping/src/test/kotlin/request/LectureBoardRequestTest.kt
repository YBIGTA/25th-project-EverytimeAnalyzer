package request

import org.example.request.LectureBoardRequest
import org.example.request.LoginOut
import org.jsoup.nodes.Document
import org.junit.jupiter.api.Test
import org.openqa.selenium.chrome.ChromeDriver

class LectureBoardRequestTest {

    // // 단순히 작동하는 지 눈으로 확인
    // @Test
    // fun scrollDownTest() {
    //     val driver: ChromeDriver = ChromeDriver()
    //     val lectureBoardRequest = LectureBoardRequest(driver, 5, 3)
    //     //....
    //     val id = "ticktacktok135"
    //     val pw = "park6240"
    //     val loginOut = LoginOut(driver, 3, 3, id, pw)
    //     try {
    //         loginOut.loginPage()
    //     } catch (_: Exception) {
    //
    //     }
    //     Thread.sleep(3000)
    //     val doc: Document = lectureBoardRequest.lectureListPageRequest(8, 1)
    //     Thread.sleep(3000)
    //     loginOut.logoutPage()
    // }
}