const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const bcrypt = require('bcrypt');
const mysql = require('mysql2/promise');

const app = express();
const port = 3000;

// 数据库连接
const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'your_mysql_password',
    database: 'rubbish',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// 中间件
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
    secret: 'your_secret_key',
    resave: false,
    saveUninitialized: true
}));

// 静态文件服务
app.use(express.static('public'));

// 登录路由
app.post('/login', async (req, res) => {
    try {
        const { userId, userName, password } = req.body;
        const [users] = await pool.query('SELECT * FROM users WHERE user_id = ? AND username = ?', [userId, userName]);

        if (users.length === 0) {
            return res.json({ success: false, message: '用户不存在' });
        }

        const user = users[0];
        const passwordMatch = await bcrypt.compare(password, user.password);

        if (!passwordMatch) {
            return res.json({ success: false, message: '密码错误' });
        }

        // 更新最后登录时间
        await pool.query('UPDATE users SET last_login = NOW() WHERE id = ?', [user.id]);

        // 设置会话
        req.session.userId = user.id;
        req.session.username = user.username;

        res.json({ success: true, user: { id: user.id, username: user.username } });
    } catch (error) {
        console.error(error);
        res.json({ success: false, message: '服务器错误' });
    }
});

// 注册路由
app.post('/register', async (req, res) => {
    try {
        const { userId, userName, password } = req.body;

        // 检查用户ID和用户名是否已存在
        const [[userCheck]] = await pool.query('SELECT * FROM users WHERE user_id = ? OR username = ?', [userId, userName]);

        if (userCheck) {
            return res.json({ success: false, message: userCheck.user_id === userId ? '用户ID已存在' : '用户名已存在' });
        }

        // 加密密码
        const hashedPassword = await bcrypt.hash(password, 10);

        // 插入新用户
        const [result] = await pool.query('INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)', [userId, userName, hashedPassword]);

        // 创建积分记录
        await pool.query('INSERT INTO scores (user_id, current_score) VALUES (?, 0)', [result.insertId]);

        res.json({ success: true, message: '注册成功' });
    } catch (error) {
        console.error(error);
        res.json({ success: false, message: '服务器错误' });
    }
});

// 修改用户信息路由
app.post('/update-user', async (req, res) => {
    try {
        const { userId, currentUserName, newUserName, originalPassword, newPassword } = req.body;

        // 获取当前用户信息
        const [users] = await pool.query('SELECT * FROM users WHERE user_id = ? AND username = ?', [userId, currentUserName]);

        if (users.length === 0) {
            return res.json({ success: false, message: '用户信息不匹配' });
        }

        const user = users[0];
        const passwordMatch = await bcrypt.compare(originalPassword, user.password);

        if (!passwordMatch) {
            return res.json({ success: false, message: '原始密码错误' });
        }

        // 更新用户名和密码
        let updateQuery = 'UPDATE users SET username = ?';
        const updateParams = [newUserName];

        if (newPassword) {
            const hashedNewPassword = await bcrypt.hash(newPassword, 10);
            updateQuery += ', password = ?';
            updateParams.push(hashedNewPassword);
        }

        updateQuery += ' WHERE id = ?';
        updateParams.push(user.id);

        await pool.query(updateQuery, updateParams);

        res.json({ success: true, message: '修改成功' });
    } catch (error) {
        console.error(error);
        res.json({ success: false, message: '服务器错误' });
    }
});

// 启动服务器
app.listen(port, () => {
    console.log(`服务器运行在 http://localhost:${port}`);
});