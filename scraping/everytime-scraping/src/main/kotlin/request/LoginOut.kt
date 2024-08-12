package org.example.request

import org.example.sleep
import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.support.ui.ExpectedConditions
import org.openqa.selenium.support.ui.WebDriverWait
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import java.time.Duration

object LoginOutSelector {
    val idInput: String = "body > div:nth-child(2) > div > form > div.input > input[type=text]:nth-child(1)"
    val pwInput: String = "body > div:nth-child(2) > div > form > div.input > input[type=password]:nth-child(2)"
    val submmit: String = "body > div:nth-child(2) > div > form > input[type=submit]"
    val logOut: String = "#container > div.leftside > div.card.pconly > form > ul > li:nth-child(2) > a"
}

class LoginOut(
    private val driver: WebDriver,
    private val timeout: Long,
    private val sleepTime: Int,
    private val everytimeId: String,
    private val everytimePassword: String,
) {
    private val EVERY_TIME_LOGIN_URL: String = "https://account.everytime.kr/login"
    private val MAIN_PAGE: String = "https://everytime.kr/"
    private val logger: Logger = LoggerFactory.getLogger(LoginOut::class.java)

    fun loginPage() {
        val loginPageSleepTime: Int = 1
        driver.get(EVERY_TIME_LOGIN_URL)
        sleep(sleepTime)
        // actions.moveByOffset(100, 100).click().perform()
        WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(ExpectedConditions.elementToBeClickable(By.cssSelector(LoginOutSelector.idInput)))
            .also {
                it.click()
                sleep(loginPageSleepTime)
                it.sendKeys(everytimeId)
            }
        WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(ExpectedConditions.elementToBeClickable(By.cssSelector(LoginOutSelector.pwInput)))
            .also {
                it.click()
                sleep(loginPageSleepTime)
                it.sendKeys(everytimePassword)
            }
        sleep(loginPageSleepTime)
        WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(ExpectedConditions.elementToBeClickable(By.cssSelector(LoginOutSelector.submmit)))
            .click()
        logger.info("login success")
    }

    fun logoutPage() {
        driver.get(MAIN_PAGE)

        WebDriverWait(driver, Duration.ofSeconds(timeout))
            .until(ExpectedConditions.elementToBeClickable(By.cssSelector(LoginOutSelector.logOut)))
            .click()

        sleep(sleepTime)

        logger.info("logout success")

        driver.quit()
        logger.info("quit chrome driver")

    }

}