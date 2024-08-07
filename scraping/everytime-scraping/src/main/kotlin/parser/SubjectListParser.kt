package org.example.parser

import org.jsoup.nodes.Document

object SubjectListCssSelector {
    val url: String = "#subjects > div.list > table > tbody > tr > td > a"
    val subjectCode: String = "#subjects > div.list > table > tbody > tr > td:nth-child(3)"
}

object SubjectListParser {
    /**
     * @return /lecture/view/2786332, /lecture/view/2775860 이런 형식으로 리턴합니다잉
     */
    fun parseUrl(doc: Document): List<String> {
        val reviewUrlList: List<String> = doc.select(SubjectListCssSelector.url)
            .map { it.attr("href") }

        return reviewUrlList
    }

    fun parseSubjectCode(doc: Document): List<String> {
        val subjectCodeList: List<String> = doc.select(SubjectListCssSelector.subjectCode)
            .map { it.text() }

        return subjectCodeList
    }
}