package org.example

data class Args(
    val urlPrefix: String,
    val startPage: Int,
    val pageNum: Int,
    val sleepTime: Int
)

fun isNumeric(toCheck: String): Boolean {
    return toCheck.toIntOrNull() != null
}

fun validateCondition(condition: Boolean) {
    if (!condition) throw Exception("error")
}

/**
 * expected
 * --url_prefix 385546 --start_page 10 --page_num 5 --sleep_time 4
 */
// TODO: add validation logic for --
fun parseArgs(args: Array<String>): Args {
    // validate
    validateCondition(args.size == 8)
    validateCondition(args[0] == "--url_prefix")
    validateCondition(args[2] == "--start_page")
    validateCondition(args[4] == "--page_num")
    validateCondition(args[6] == "--sleep_time")
    validateCondition(isNumeric(args[3]))
    validateCondition(isNumeric(args[5]))
    validateCondition(isNumeric(args[7]))

    // parse
    val args: Args = Args(
        args[1],
        args[3].toInt(),
        args[5].toInt(),
        args[7].toInt(),
    )
    return args
}