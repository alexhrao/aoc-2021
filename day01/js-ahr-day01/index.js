const fs = require('fs');

function part1() {
    const nums = fs.readFileSync("../../inputs/day01.txt")
        .toString('utf-8')
        .split("\n")
        .map(n => parseInt(n));
    let out = 0;
    for (let i = 1; i < nums.length; ++i) {
        if (nums[i] > nums[i - 1]) {
            out += 1;
        }
    }
    console.log(out);
}

function part2() {
    const nums = fs.readFileSync("../../inputs/day01.txt")
        .toString('utf-8')
        .split("\n")
        .map(n => parseInt(n));
    let out = 0;
    for (let i = 3; i < nums.length; i++) {
        const left = nums[i - 3] + nums[i - 2] + nums[i - 1];
        const right = nums[i - 2] + nums[i - 1] + nums[i];
        if (right > left) {
            out += 1;
        }
    }
    console.log(out);
}

if (process.argv.length < 3 || process.argv[2] === "1") {
    console.log("Part 1");
    part1();
}

if (process.argv.length < 3 || process.argv[2] === "2") {
    console.log("Part 2");
    part2();
}
