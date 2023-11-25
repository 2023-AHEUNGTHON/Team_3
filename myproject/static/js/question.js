var num = 1;
var mbti = "";

window.addEventListener('load', function() {
    next();
});

function next() {
    
    if (num == 13) {
        mbti = "";
        $("#EI").val() < 2 ? (mbti += "I") : (mbti += "E");
        $("#SN").val() < 2 ? (mbti += "N") : (mbti += "S");
        $("#TF").val() < 2 ? (mbti += "F") : (mbti += "T");
        $("#JP").val() < 2 ? (mbti += "P") : (mbti += "J");

        console.log(mbti);

        var dataToSend = {
            'mbti':mbti,
        };

        var csrfToken = $('[name=csrfmiddlewaretoken]').val();
        if (!csrfToken) {
            csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        }

        $.ajax({
            url: '/survey/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(dataToSend),
            dataType: 'json',
            headers: { 'X-CSRFToken': csrfToken,
                       'X-Requested-With': 'XMLHttpRequest', 
            },
            success: function(data) {
                window.location.href='/result/' + data.popup.mbti;
            }
        });
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