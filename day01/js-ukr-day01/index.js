function part1() {
    const fs = require('node:fs');
    var numincreased = 0;

    fs.readFile('day01.txt', 'utf8', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
        var lines = data.split('\n');
        for (var line = 1; line < lines.length; line++) {
            if (parseInt(lines[line - 1]) < parseInt(lines[line])) {
                numincreased++;
            };
        }
        console.log(numincreased);
    });

}

function part2() {
    const fs = require('node:fs');
    var numincreased = 0;

    fs.readFile('day01.txt', 'utf8', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
        var lines = data.split('\n');
        for (var line = 3; line < lines.length; line++) {
            if ((parseInt(lines[line - 3]) + parseInt(lines[line - 2]) + parseInt(lines[line - 1])) < 
            (parseInt(lines[line - 2]) + parseInt(lines[line - 1]) + parseInt(lines[line - 0]))) {
                numincreased++;
            };
        }
        console.log(numincreased);
    });

}

if (process.argv.length < 3 || process.argv[2] === "1") {
    console.log("Part 1");
    part1();
}

if (process.argv.length < 3 || process.argv[2] === "2") {
    console.log("Part 2");
    part2();
}
