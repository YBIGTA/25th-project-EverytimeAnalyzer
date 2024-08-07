package org.example.parser

import org.bson.types.ObjectId
import org.example.entity.SubjectReview
import org.jsoup.nodes.Document

object ReviewDivCssSelector {
    val content: String = ".text"
    val stars: String = ".star > .on"
    val semester: String = ".semester"
}

object SubjectReviewPageCssSelector {
    val reviewList: String = "body .article_tab div.articles > div.article"
}

object SubjectReviewPageParser {
    val yearSemesterRegex: Regex = Regex("""(?<year>[0-9]{2})년\s(?<semester>[1-2]{1}학기|여름|겨울)*\s수강자""")
    fun extractYearAndSemester(raw: String): Pair<Int, String> {
        val groups: MatchGroupCollection = yearSemesterRegex.find(raw)?.groups
            ?: throw IllegalStateException("regex match failed input:${raw}")

        return Pair(("20" + groups["year"]!!.value).toInt(), groups["semester"]!!.value)
    }

    fun parse(code: String, doc: Document): List<SubjectReview> {
        return doc.select(SubjectReviewPageCssSelector.reviewList)
            .map {
                val text: String = it.select(ReviewDivCssSelector.content).text()
                val rawSemester: String = it.select(ReviewDivCssSelector.semester).text()
                // val rawStars: String = it.select(ReviewDivCssSelector.stars).attr("style")

                val (year, semester) = extractYearAndSemester(rawSemester)
                SubjectReview(ObjectId(), code, year, semester, text)
            }
    }
}

