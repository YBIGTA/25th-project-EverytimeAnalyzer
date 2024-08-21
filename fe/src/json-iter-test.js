function test() {
    const sample = {"교수님이 착한":109.22407279968262,"강의내용이 알찬":110.0137372970581}
    var x;
    for (x in sample) {
        console.log(x)
        console.log(sample[x])
    }
}

test()