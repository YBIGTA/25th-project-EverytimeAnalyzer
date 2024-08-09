package org.example.entity

import org.bson.codecs.pojo.annotations.BsonId
import org.bson.types.ObjectId

data class LectureReview(
    val year: Int,
    val semester: String,
    val content: String,
    // val rate: Int,
    // val likes: Int
)

data class LectureReviewWithMetaData(
    @BsonId
    val id: ObjectId? = null,
    val lectureCode: String,
    val majorNth: Int,
    val detailedNth: Int,
    val lectureReview: LectureReview
)



