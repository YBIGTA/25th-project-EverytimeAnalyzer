package org.example.entity

import org.bson.codecs.pojo.annotations.BsonId
import org.bson.types.ObjectId
import java.time.LocalDateTime


data class EverytimeArticle(
    @BsonId
    val id: ObjectId? = null,
    val articleId: String,
    val title: String,
    val date: LocalDateTime,
    val content: String,
    val comments: List<EverytimeCommentChunk>,
    val scrapCount: Int,
    val likeCount: Int
)