let log = console.log.bind(console)


let ajax = function(method, path, data, responseCallback) {
    let r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if (r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            responseData = JSON.parse(r.response)
            log('receive', responseData)
            responseCallback(responseData)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    log('send',data)
    r.send(data)
}


let apiSendMsgCode = function(form, callback) {
    let path = '/api/send/msg'
    ajax('POST', path, form, callback)
}


let apiArrangeManager = function(user_uuid, form, callback) {
    let path = '/api/manager/arrange/' + user_uuid
    ajax('POST', path, form, callback)
}