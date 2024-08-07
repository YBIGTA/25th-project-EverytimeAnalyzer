import org.example.ReviewArgs
import org.example.reviewArgParser
import org.junit.jupiter.api.Test

class ArgParseKtTest {
    @Test
    fun sample_test() {
        val arr: Array<String> = arrayOf("--major_nth", "2", "--detailed_major_nth", "3", "--sleep_time", "5")
        val reviewArgParser: ReviewArgs = reviewArgParser(arr)
        println(reviewArgParser)
    }
}