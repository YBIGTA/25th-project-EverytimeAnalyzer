package org.example

data class Args(
    val urlPrefix: String,
    val startPage: Int,
    val pageNum: Int,
    val sleepTime: Int
)

data class ReviewArgs(
    val majorNth: Int,
    val detailedMajorNth: Int,
    val sleepTime: Int,
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
fun articleArgParser(args: Array<String>): Args {
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

fun reviewArgParser(args: Array<String>): ReviewArgs {
    // validate
    validateCondition(args.size == 6)
    validateCondition(args[0] == "-m")
    validateCondition(args[2] == "-dm")
    validateCondition(args[4] == "-st")
    validateCondition(isNumeric(args[1]))
    validateCondition(isNumeric(args[3]))
    validateCondition(isNumeric(args[5]))

    // parse
    val args: ReviewArgs = ReviewArgs(
        args[1].toInt(),
        args[3].toInt(),
        args[5].toInt()
    )
    return args

}