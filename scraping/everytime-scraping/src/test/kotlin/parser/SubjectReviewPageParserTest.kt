package parser

import org.example.parser.SubjectReviewPageParser
import org.junit.jupiter.api.Test

class SubjectReviewPageParserTest {
    @Test
    fun sampleTest() {
        val sample1 = "24년 겨울 수강자"
        val sample2 = "24년 1학기 수강자"
        val sample3 = "24년 1학기 수강자"

        println(SubjectReviewPageParser.extractYearAndSemester(sample1))
        println(SubjectReviewPageParser.extractYearAndSemester(sample2))
        println(SubjectReviewPageParser.extractYearAndSemester(sample3))
    }
}