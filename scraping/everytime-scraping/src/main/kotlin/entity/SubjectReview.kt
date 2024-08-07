package org.example.entity

import org.bson.codecs.pojo.annotations.BsonId
import org.bson.types.ObjectId

data class SubjectReview(
    @BsonId
    val id: ObjectId? = null,
    val code: String,
    val year: Int,
    val semester: String,
    val content: String,
    // val rate: Int,
    // val likes: Int
)