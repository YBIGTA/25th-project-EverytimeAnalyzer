import org.example.ReviewArgs
import org.example.reviewArgParser
import org.junit.jupiter.api.Test

class ArgParseKtTest {
    @Test
    fun sample_test() {
        val arr: Array<String> = arrayOf("-st", "5", "-m", "2", "-dm", "1", "3", "5")
        val reviewArgParser: ReviewArgs = reviewArgParser(arr)
        println(reviewArgParser)
    }
}