var num = 1;

window.addEventListener('load', function() {
    next();
});

function next() {
    if (num == 13) {
        var mbti = "";
        $("#EI").val() < 2 ? (mbti += "I") : (mbti += "E");
        $("#SN").val() < 2 ? (mbti += "N") : (mbti += "S");
        $("#TF").val() < 2 ? (mbti += "F") : (mbti += "T");
        $("#JP").val() < 2 ? (mbti += "P") : (mbti += "J");

        console.log(mbti);
        // window.location.href = '../html/index.html';
    } else {
        let presentNum = 0;
        if (num < 10) { presentNum = "0" + num; } else { presentNum = num; }
        $("#changeNum").html(presentNum);
        $("#title").html(q[num]["title"]);
        $("#type").val(q[num]["type"]);
        $("#A").html(q[num]["A"]);
        $("#B").html(q[num]["B"]);
        $("#img").attr('src', q[num]["img"]);
        num++;
    }
}

$("#A").click(function() {
    var type = $("#type").val();
    var preValue = $("#" + type).val();
    $("#" + type).val(parseInt(preValue) + 1);
    next();
});
$("#B").click(function() {
    next();
});