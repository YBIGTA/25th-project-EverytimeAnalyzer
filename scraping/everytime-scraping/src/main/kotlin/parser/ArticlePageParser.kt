package org.example.parser

import org.bson.types.ObjectId
import org.example.entity.EverytimeArticle
import org.example.entity.EverytimeComment
import org.example.entity.EverytimeCommentChunk
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import org.jsoup.select.Elements
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeFormatterBuilder
import java.time.temporal.ChronoField

object ArticlePageParser {
    private val commentSelector: String = "#container > div.wrap.articles > article > div.comments > article"
    private val titleSelector: String = "#container > div.wrap.articles > article.item > a.article h2.large"

    // 본문 css selector
    private val contentSelector: String = "#container > div.wrap.articles > article.item > a.article p.large"
    private val likeCountSelector: String = "#container > div.wrap.articles > article.item > a.article > ul.status.left > li.vote"
    private val scrapCountSelector: String = "#container > div.wrap.articles > article.item > a.article > ul.status.left > li.scrap"
    private val articleIdSelector: String = "head > meta:nth-child(8)"
    private val writtenDateSelector: String = "#container > div.wrap.articles > article time.large"
    private val dateFormatter: DateTimeFormatter = DateTimeFormatterBuilder()
        .appendPattern("MM/dd HH:mm")
        .parseDefaulting(ChronoField.YEAR, 2024L)
        .toFormatter()

    fun toEverytimeComment(commentElement: Element): EverytimeComment {
        val content: String = commentElement.selectFirst("p.large")!!.text()
        val likes: Int = commentElement.selectFirst("li.vote")!!.text().toInt()
        return EverytimeComment(
            content,
            likes
        )
    }

    /**
     * @param doc 에타 개별 게시글 페이지 html
     */
    fun parseComment(doc: Document): List<EverytimeCommentChunk> {
        val commentsDiv: Elements = doc.select(commentSelector)
            ?: throw NoSuchElementException()

        val commentLists: MutableList<Pair<EverytimeComment, MutableList<EverytimeComment>>> = mutableListOf()

        for (comment in commentsDiv) {
            val className: String = comment.selectFirst("article")!!.className()
            if (className == "parent") {
                commentLists.add(Pair(toEverytimeComment(comment), mutableListOf()))
            } else if (className == "child") {
                commentLists.last().second.add(toEverytimeComment(comment))
            }
        }

        return commentLists.map {
            EverytimeCommentChunk(it.first, it.second)
        }
    }

    fun parseArticle(doc: Document): EverytimeArticle {

        val title: String = doc.selectFirst(titleSelector)!!.text()
        val content: String = doc.selectFirst(contentSelector)!!.text()
        val articleId: String = doc.selectFirst(articleIdSelector)!!.attr("content")
        val comments: List<EverytimeCommentChunk> = parseComment(doc)
        val scrapCount: Int = doc.selectFirst(scrapCountSelector)!!.text().toInt()
        val likeCount: Int = doc.selectFirst(likeCountSelector)!!.text().toInt()
        val date: LocalDateTime = LocalDateTime.parse(
            doc.selectFirst(writtenDateSelector)!!.text(),
            dateFormatter
        )

        return EverytimeArticle(
            ObjectId(),
            articleId,
            title,
            date,
            content,
            comments,
            scrapCount,
            likeCount
        )
    }
}