package org.example

data class Args(
    val urlPrefix: String,
    val startPage: Int,
    val pageNum: Int,
    val sleepTime: Int
)

data class ReviewArgs(
    val sleepTime: Int,
    val scrollLimit: Int,
    val majorNth: Int,
    val detailedMajorNthList: List<Int>,
)

fun isNumeric(toCheck: String): Boolean {
    return toCheck.toIntOrNull() != null
}

fun validateCondition(condition: Boolean) {
    if (!condition) throw Exception("argument parse error")
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

/**
 * expect args like -st 5 -sl 3 -m 2 -dm 1 3 5 7
 * dm(세부 학과: ex 경제학과, 문화와 예술 등등), m(학과: 교양과목, 이과대학, 상경대학) is expected single digit
 */
fun reviewArgParser(args: Array<String>): ReviewArgs {
    validateCondition(6 <= args.size)
    validateCondition(args[0] == "-st")
    validateCondition(args[2] == "-sl")
    validateCondition(args[4] == "-m")
    validateCondition(args[6] == "-dm")

    args.filterIndexed { idx, _ -> idx !in arrayOf(0, 2, 4, 6) }
        .forEach { validateCondition(isNumeric(it)) }

    // parse
    return ReviewArgs(
        args[1].toInt(),
        args[3].toInt(),
        args[5].toInt(),
        args.slice(7..<args.size).map { it.toInt() }
    )
}