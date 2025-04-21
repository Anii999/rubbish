$(document).on("click", ".兑换按钮", function() {
    var giftId = $(this).data("gift_id");
    var requiredPoints = parseInt($(this).data("points"));
    var currentPoints = parseInt(sessionStorage.getItem('points'));

    if (currentPoints >= requiredPoints) {
        if (confirm("确认兑换此礼品，需要 " + requiredPoints + " 积分？")) {
            // 发送兑换请求
            $.ajax({
                url: "{{ url_for('exchange') }}",
                method: "POST",
                data: { gift_id: giftId },
                success: function(response) {
                    if (response.success) {
                        alert("兑换成功！您已使用 " + requiredPoints + " 积分兑换礼品。");
                        // 更新当前积分
                        sessionStorage.setItem('points', parseInt(sessionStorage.getItem('points')) - requiredPoints);
                        $(".积分余额").text("当前积分: " + sessionStorage.getItem('points'));
                        // 重新加载礼品列表和兑换记录
                        loadGifts();
                        updateExchangeRecords();
                    } else {
                        alert(response.message);
                    }
                },
                error: function() {
                    alert("兑换失败");
                }
            });
        }
    } else {
        alert("积分不足，无法兑换。");
    }
});

$(document).on("click", ".兑换按钮", function() {
    var giftId = $(this).data("gift-id");
    var requiredPoints = parseInt($(this).data("points"));
    var currentPoints = parseInt(sessionStorage.getItem('points'));

    if (currentPoints >= requiredPoints) {
        if (confirm("确认兑换此礼品，需要 " + requiredPoints + " 积分？")) {
            // 发送兑换请求
            $.ajax({
                url: "{{ url_for('exchange') }}",
                method: "POST",
                data: { gift_id: giftId },
                success: function(response) {
                    if (response.success) {
                        alert("兑换成功！您已使用 " + requiredPoints + " 积分兑换礼品。");
                        // 更新当前积分
                        sessionStorage.setItem('points', parseInt(sessionStorage.getItem('points')) - requiredPoints);
                        $(".积分余额").text("当前积分: " + sessionStorage.getItem('points'));
                        // 重新加载礼品列表和兑换记录
                        loadGifts();
                        updateExchangeRecords();
                    } else {
                        alert("兑换失败: " + response.message);
                    }
                },
                error: function() {
                    alert("兑换失败: 服务器错误");
                }
            });
        }
    } else {
        alert("积分不足，无法兑换。");
    }
});
