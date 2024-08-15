package org.example.entity

import org.bson.codecs.pojo.annotations.BsonId
import org.bson.types.ObjectId

data class LectureInfo(
    @BsonId
    val id: ObjectId? = null,
    val code: String,
    val type: List<String>,
    val name: String,
    val professorList: List<String>,
    val time: Map<String, List<Int>>,
    val place: String,
)
