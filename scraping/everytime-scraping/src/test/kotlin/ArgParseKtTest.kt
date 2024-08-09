import org.example.ReviewArgs
import org.example.reviewArgParser
import org.junit.jupiter.api.Test

class ArgParseKtTest {
    @Test
    fun sample_test() {
        val arr: Array<String> = arrayOf("-m", "2", "-dm", "3", "-st", "5")
        val reviewArgParser: ReviewArgs = reviewArgParser(arr)
        println(reviewArgParser)
    }
}