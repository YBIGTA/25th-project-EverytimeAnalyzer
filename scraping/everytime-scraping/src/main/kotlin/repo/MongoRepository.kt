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
        val connectionString: ConnectionString = ConnectionString(URL)
        /**
         * docker-compose로 스크래핑 코드와 mongodb를 같이 띄웠을 때
         * 스크래핑 코드가 먼저 작동해서 db connection이 맺어지지 않은 대참사가 발생한다.
         * docker단에서 해결해야하는 문제이지만 일단 그냥 sleep으로 임시방편
         */
        Thread.sleep(4000)
        client = MongoClient.create(connectionString)
    }

    fun insert(article: T, insertLog: String) {
        val database: MongoDatabase = client.getDatabase(databaseName)
        val collection: MongoCollection<T> = database.getCollection(collectionName, clazz)
        logger.info(insertLog)
        collection.insertOne(article)
    }


}