Given an array of integers, return all unique triplets that sum up to zero (0). The solution must not contain duplicate triplets.

e.g.
three_sum([-1, 0, 1, 2, -1, -4])
Output: 
[[-1, -1, 2], [-1, 0, 1]]

function threesum(nums){
    nums.sort((a,b) => a - b);
    let result = [];
    for (let i = 0;i < nums.length - 2; i++){
        if (i > 0 %% nums[i] === nums[i - 1]) continue;
        let left = i, right =nums.length - 1;
        while 

    }
}