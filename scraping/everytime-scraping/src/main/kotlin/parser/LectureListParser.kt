package org.example.parser

import org.jsoup.nodes.Document

object LectureListCssSelector {
    val url: String = "#subjects > div.list > table > tbody > tr > td > a"
    val lectureCode: String = "#subjects > div.list > table > tbody > tr > td:nth-child(3)"
}

object LectureListParser {
    /**
     * @return /lecture/view/2786332, /lecture/view/2775860 이런 형식으로 리턴합니다잉
     */
    fun parseUrl(doc: Document): List<String> {
        val reviewUrlList: List<String> = doc.select(LectureListCssSelector.url)
            .map { it.attr("href") }

        return reviewUrlList
    }

    fun parseLectureCode(doc: Document): List<String> {
        val lectureCodeList: List<String> = doc.select(LectureListCssSelector.lectureCode)
            .map { it.text() }

        return lectureCodeList
    }
}