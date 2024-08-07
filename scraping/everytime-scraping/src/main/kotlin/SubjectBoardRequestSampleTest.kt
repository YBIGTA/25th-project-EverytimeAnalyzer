package org.example

import org.example.request.LoginOut
import org.example.request.SubjectBoardRequest
import org.openqa.selenium.chrome.ChromeDriver

fun mySleep(sleepTime: Int) {
    Thread.sleep(sleepTime.toLong() * 1000)
}

fun main() {
    val chromeDriver: ChromeDriver = ChromeDriver()

    val timeout: Int = 7
    val sleepTime: Int = 3
    val loginOut = LoginOut(chromeDriver, timeout.toLong(), sleepTime)
    val subjectBoardRequest = SubjectBoardRequest(chromeDriver, timeout.toLong(), sleepTime)


    // parse
    loginOut.loginPage()
    mySleep(sleepTime)
    subjectBoardRequest.requestSubjectListPage(2, 1)
    loginOut.logoutPage()

}
