        // 菜单切换功能
        $("#登录按钮").click(function() {
            $("#登录表单").show();
            $("#注册表单").hide();
            $("#修改表单").hide();
        });

        $("#注册按钮").click(function() {
            $("#登录表单").hide();
            $("#注册表单").show();
            $("#修改表单").hide();
        });

        $("#修改按钮").click(function() {
            $("#登录表单").hide();
            $("#注册表单").hide();
            $("#修改表单").show();
        });

        // 登录功能
        $("#登录提交").click(function() {
            var userId = $("#loginUserId").val();
            var password = $("#loginPassword").val();

            if (!userId) {
                alert("请输入用户ID！");
                return;
            }

            if (!password) {
                alert("请输入密码！");
                return;
            }

            // 模拟登录操作
            alert("登录成功！");
        });

        // 注册功能
        $("#注册提交").click(function() {
            var userId = $("#registerUserId").val();
            var userName = $("#registerUserName").val();
            var password = $("#registerPassword").val();
            var confirmPassword = $("#confirmRegisterPassword").val();

            if (!userId) {
                alert("请输入用户ID！");
                return;
            }

            if (!userName) {
                alert("请输入用户名！");
                return;
            }

            if (!password) {
                alert("请输入密码！");
                return;
            }

            if (password !== confirmPassword) {
                alert("两次输入的密码不一致！");
                return;
            }

            // 模拟注册操作
            alert("注册成功！");
        });

        // 修改功能
        $("#修改提交").click(function() {
            var userId = $("#userId").val();
            var currentUserName = $("#currentUserName").val();
            var newUserName = $("#newUserName").val();
            var originalPassword = $("#originalPassword").val();
            var newPassword = $("#newPassword").val();
            var confirmNewPassword = $("#confirmNewPassword").val();

            if (!newUserName) {
                alert("请输入新用户名！");
                return;
            }

            if (!originalPassword) {
                alert("请输入原始密码！");
                return;
            }

            if (!newPassword) {
                alert("请输入新密码！");
                return;
            }

            if (newPassword !== confirmNewPassword) {
                alert("两次输入的新密码不一致！");
                return;
            }

            // 模拟修改操作
            alert("用户信息已成功修改！");
        });

        // 重置功能
        $("#修改重置").click(function() {
            $("#修改表单内容")[0].reset();
        });

        