package parser

import org.assertj.core.api.Assertions
import org.assertj.core.api.Assertions.assertThat
import org.assertj.core.api.Assertions.entry
import org.example.parser.LectureTableParser
import org.junit.jupiter.api.Test

class LectureTableParserTest {
    @Test
    fun period_split_test() {
        val sample1 = "수7,8(수9)"
        val sample2 = "월7,8,수8"
        val sample3 = "화4/목5,6"
        val sample4 = "토11,12,13"
        val sample5 = "화5,6,목5(목6)"
        assertThat(LectureTableParser.resolvePeriod(sample1))
            .containsOnly(
                entry("수", listOf(7, 8, 9)),
            )
        assertThat(LectureTableParser.resolvePeriod(sample2))
            .containsOnly(
                entry("월", listOf(7, 8)),
                entry("수", listOf(8)),
            )
        assertThat(LectureTableParser.resolvePeriod(sample3))
            .containsOnly(
                entry("화", listOf(4)),
                entry("목", listOf(5, 6)),
            )
        assertThat(LectureTableParser.resolvePeriod(sample4))
            .containsOnly(
                entry("토", listOf(11, 12, 13))
            )
        assertThat(LectureTableParser.resolvePeriod(sample5))
            .containsOnly(
                entry("화", listOf(5, 6)),
                entry("목", listOf(5, 6)),
            )
    }
}