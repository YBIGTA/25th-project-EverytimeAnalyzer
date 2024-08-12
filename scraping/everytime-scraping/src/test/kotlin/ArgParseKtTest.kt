import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.testing.CliktCommandTestResult
import com.github.ajalt.clikt.testing.test
import org.example.ReviewArgs
import org.example.ReviewScrap
import org.example.reviewArgParser
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Test

class ArgParseKtTest {
    @Test
    fun sample_test() {
        val arr: Array<String> = arrayOf("-st", "5", "-sl", "3", "-m", "2", "-dm", "1", "3", "5")
        val reviewArgParser: ReviewArgs = reviewArgParser(arr)
        println(reviewArgParser)
    }

    @Test
    fun clikt_test() {
        val reviewScrap: CliktCommand = ReviewScrap()
        val result: CliktCommandTestResult = reviewScrap
            .test(
                "-st 7 -sl 4 -m 3 -dm 11 9 30",
                envvars = mapOf(
                    "MONGO_URL" to "mongodb://localhost:27017",
                    "REMOTE_DRIVER_URL" to "http://localhost:4444",
                    "EVERY_TIME_ID" to "id",
                    "EVERY_TIME_PASSWORD" to "pw"
                )
            )
        val expected = """
            mongoURL: mongodb://localhost:27017
            remoteDriverUrl: http://localhost:4444
            everytimeId: id
            everytimePW: pw
            sleepTime: 7
            scrollLimit: 4
            majorNth: 3
            detailedMajor: [11, 9, 30]
            
        """.trimIndent()

        Assertions.assertEquals(result.output, expected)
    }
}