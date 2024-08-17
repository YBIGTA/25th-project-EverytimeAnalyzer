package org.example

fun sleep(sec: Int) = Thread.sleep((sec * 1000).toLong())

fun mongoUrlBuilder(host: String, port: Int, username: String, password: String): String =
    "mongodb://$username:$password@$host:$port/?authSource=admin"