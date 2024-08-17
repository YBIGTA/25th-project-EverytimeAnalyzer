import com.github.ajalt.clikt.core.CliktCommand
import com.github.ajalt.clikt.testing.CliktCommandTestResult
import com.github.ajalt.clikt.testing.test
import org.example.ReviewScrap
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Test

class ArgParseKtTest {
    @Test
    fun clikt_test() {
        val reviewScrap: CliktCommand = ReviewScrap()
        val result: CliktCommandTestResult = reviewScrap
            .test(
                "-st 7 -sl 4 -m 3 -dm 11 9 30 -debug true",
                envvars = mapOf(
                    "MONGO_URL" to "mongodb://localhost:27017",
                    "REMOTE_DRIVER_URL" to "http://localhost:4444",
                    "EVERY_TIME_ID" to "id",
                    "EVERY_TIME_PASSWORD" to "pw",
                    "MONGO_HOST" to "mongodb://localhost:27017",
                    "MONGO_USERNAME" to "root",
                    "MONGO_PASSWORD" to "ybigta135",
                    "MONGO_PORT" to "27017"
                )
            )
        val expected = """
            mongoHost: mongodb://localhost:27017
            mongoUsername: root
            mongoPassword: ybigta135
            mongoPort: 27017
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