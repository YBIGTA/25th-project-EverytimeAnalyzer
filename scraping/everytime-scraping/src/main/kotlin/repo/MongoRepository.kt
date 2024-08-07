package org.example.repo

import com.mongodb.ConnectionString
import com.mongodb.kotlin.client.MongoClient
import com.mongodb.kotlin.client.MongoCollection
import com.mongodb.kotlin.client.MongoDatabase
import org.example.entity.EverytimeArticle
import org.slf4j.Logger
import org.slf4j.LoggerFactory

class MongoRepository(
    URL: String,
) {
    private val client: MongoClient
    private val databaseName: String = "everytime"
    private val logger: Logger = LoggerFactory.getLogger(MongoRepository::class.java)

    init {
        val connectionString: ConnectionString = ConnectionString(URL)
        client = MongoClient.create(connectionString)
    }

    fun insertArticle(article: EverytimeArticle) {
        val database: MongoDatabase = client.getDatabase(databaseName)
        val collection: MongoCollection<EverytimeArticle> = database.getCollection<EverytimeArticle>("article")
        logger.info("inserting article id:{}", article.articleId)
        collection.insertOne(article)
    }
}