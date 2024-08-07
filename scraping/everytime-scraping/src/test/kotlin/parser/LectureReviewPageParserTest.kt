package parser

import org.example.parser.LectureReviewPageParser
import org.junit.jupiter.api.Test

class LectureReviewPageParserTest {
    @Test
    fun sampleTest() {
        val sample1 = "24년 겨울 수강자"
        val sample2 = "24년 1학기 수강자"
        val sample3 = "24년 1학기 수강자"

        println(LectureReviewPageParser.extractYearAndSemester(sample1))
        println(LectureReviewPageParser.extractYearAndSemester(sample2))
        println(LectureReviewPageParser.extractYearAndSemester(sample3))
    }
}