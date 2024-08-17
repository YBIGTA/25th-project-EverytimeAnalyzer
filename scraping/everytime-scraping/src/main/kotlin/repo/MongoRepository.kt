package org.example.repo

import com.mongodb.ConnectionString
import com.mongodb.kotlin.client.MongoClient
import com.mongodb.kotlin.client.MongoCollection
import com.mongodb.kotlin.client.MongoDatabase
import org.slf4j.Logger
import org.slf4j.LoggerFactory

class MongoRepository<T : Any>(
    URL: String,
    private val collectionName: String,
    private val clazz: Class<T>
) {
    private val client: MongoClient
    private val databaseName: String = "everytime"
    private val logger: Logger = LoggerFactory.getLogger(MongoRepository::class.java)

    companion object {
        inline fun <reified K : Any> of(URL: String, collectionName: String): MongoRepository<K> {
            return MongoRepository<K>(
                URL,
                collectionName,
                K::class.java
            )
        }
    }

    init {
        logger.info("mongo url: {}", URL)
        client = MongoClient.create(URL)
    }

    fun insert(article: T, insertLog: String) {
        val database: MongoDatabase = client.getDatabase(databaseName)
        val collection: MongoCollection<T> = database.getCollection(collectionName, clazz)
        logger.trace(insertLog)
        collection.insertOne(article)
    }


}