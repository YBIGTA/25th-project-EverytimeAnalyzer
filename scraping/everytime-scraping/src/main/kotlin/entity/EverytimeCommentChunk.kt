package org.example.entity

data class EverytimeCommentChunk(
    val comment: EverytimeComment,
    val replies: List<EverytimeComment>
)