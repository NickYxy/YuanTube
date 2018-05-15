let checkMobile = () => {
    let mobile = $("#id-input-mobile").val()
    if (mobile != "admin") {
        return mobile && mobile.match(/(^1[3|5|7|8|][\d]{9}$)|(^14[7]\d{8}$)/)
    } else {
        return true
    }
}


let checkPassword = () => {
    let password = $("#id-input-password").val()
    let newpassword = $("#id-input-newpassword").val()
    let regStr = /^[a-zA-Z0-9]{6,20}$/
    // 6-20位字符，可使用字母、数字
    if (typeof(newpassword) == "undefined") {
        return password && password.match(regStr)
    }
    return (password && password.match(regStr)) && (newpassword && newpassword.match(regStr))
}


let checkRePassword = () => {
    let password = $("#id-input-password").val()
    let rePassword = $("#id-input-repassword").val()
    let newpassword = $("#id-input-newpassword").val()
    if (typeof(newpassword) == "undefined") {
        return rePassword && rePassword === password
    }
    return rePassword && rePassword === newpassword
}


let checkform = (type) => {
    let checkDict = {
        password: [checkPassword, "请输入正确格式的密码"],
    }
    if (type === "register") {
        checkDict.mobile = [checkMobile, "请输入正确格式的手机号码"]
        checkDict.repassword = [checkRePassword, "两次输入密码不一致"]
    } else if (type === "login") {
        // checkDict.mobile = [checkMobile, "请输入正确格式的手机号码"]
    } else {
        checkDict.repassword = [checkRePassword, "两次输入密码不一致"]
        checkDict.password = [checkPassword, "请输入正确格式的原密码和新密码"]
    }
    let keys = Object.keys(checkDict)
    let msg = ''
    for (let i = 0; i < keys.length; i++) {
        let key = keys[i]
        let foo = checkDict[key][0]
        if (!foo()) {
            msg = checkDict[key][1]
            return [false, msg]
        }
    }
    return [true, msg]
}


let eventFormSumbit = () => {
    $(".form-user").submit(function (e) {
        let type = $(".form-user").data('type')
        let [status, msg] = checkform(type)
        if (!status) {
            swal(msg)
            e.preventDefault()
        }
    });
}


let sendMsgCode = () => {
    let mobile = $("#id-input-mobile").val()
    let captcha = $("#id-input-captcha").val()
    if (!captcha) {
        swal("请先填写图形验证码")
    } else if(checkMobile()){
        let button = $("#id-button-msg-code")
        let type = $(button).data('type')
        let form = {
            mobile: mobile,
            use: type,
            captcha: captcha,
        }
        let response = (res) => {
            if (!res.success) {
                swal(res.message)
            } else {
                swal("已发送")
            }
        }
        apiSendMsgCode(form, response)
    } else {
        swal("请输入正确格式的手机号码")
    }
}


let _main = () => {
    eventFormSumbit()
}


_main()

