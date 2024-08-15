package org.example.parser

import org.bson.types.ObjectId
import org.example.entity.LectureInfo
import org.example.request.LectureBoardCssSelector
import org.jsoup.nodes.Document
import org.jsoup.select.Elements

object LectureTableParser {
    fun nthTd(nth: Int) = "td:nth-child(${nth})"
    fun resolveRawProfessorList(raw: String): List<String> {
        return raw.split(",")
    }

    fun resolvePeriod(raw: String): Map<String, List<Int>>{
        val extractPeriod: Regex = Regex("""(?<day>[월화수목금토일])(?<period>[0-9,]+)""")

        val result  = extractPeriod.findAll(raw)
            .map { matchResult ->
                val matchedDay: String = matchResult.groups["day"]!!.value
                val matchedPeriod: String = matchResult.groups["period"]!!.value

                val periods:List<Int> =  matchedPeriod
                    .split(",")
                    .filter {it != ""}
                    .map { it.toInt() }

                matchedDay to periods
            }
            .groupBy(keySelector = {it.first}, valueTransform = {it.second})
            .map { it.key to it.value.flatten() }
            .toMap()

        return result
    }

    fun parse(doc: Document): List<LectureInfo> {
        // get table
        val lectureList: Elements = doc.select(LectureBoardCssSelector.lectureListTr)

        val lectureInfoList: List<LectureInfo> = lectureList.map {
            val type: String = it.selectFirst(nthTd(2))!!.text()
            val code: String = it.selectFirst(nthTd(3))!!.text()
            val name: String = it.selectFirst(nthTd(5))!!.text()
            val rawProfessors: String = it.selectFirst(nthTd(6))!!.text()
            val time: String = it.selectFirst(nthTd(7))!!.text()
            val place: String = it.selectFirst(nthTd(8))!!.text()

            LectureInfo(
                ObjectId(),
                code,
                type.split("/"),
                name,
                resolveRawProfessorList(rawProfessors),
                resolvePeriod(time),
                place
            )
        }

        return lectureInfoList
    }
}