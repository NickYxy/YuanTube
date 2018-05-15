/**
 * Created by djz on 2018/4/25.
 */
let uploadInfoImg = (e, url) => {
    let self = e
    $(e).ajaxfileupload({
        action: url,
        onComplete: function (res) {
            let parent = $(self).parent()
            let input = $(parent).find('.hidden')
            console.log(res)
            if (res.success) {
                let pic = res.data
                let paths = pic.split('/')
                let filename = paths[paths.length - 1]
                $(input).val(filename)
                let img =  $(parent).find('img')
                $(img).attr("src", pic + "?random=" + Math.random());
                $(img).addClass("profile-img")
            } else {
                swal('请上传正确格式的照片并检查图片大小')
            }
        }
    });
}


let eventUploadImg = (url) => {
    $('.info-pics').on('click', function () {
        let self = this
        let input = $(self).find("input[type='file']")
        uploadInfoImg(input, url)
    })
}


let checkConfirm = () => {
    let check = $("input:checkbox:checked")
    return check.length
}


let openImg = (e) => {
    url = $(e).attr("src")
    if (url) {
        window.open(url)
    }
}


let vaildFormSubmit = () => {
    $("form").submit(function (e) {
        if (!checkConfirm()) {
            swal("请勾选最后的保证选项")
            e.preventDefault()
        }
    });
}


let imgView = () => {
    // 新窗口打开图片
    $('img').on('click', function () {
        let self = this
        openImg(self)
    })
}


let checkPassClient = () => {
    let check = $("input[name='pass']:checked").val()
    if (check === "nopass") {
        let reason = $("#id-input-reason").val()
        return [reason, "请填写驳回理由"]
    } else {
        let v = $('#id-base_info_pic').val()
        return [v, "请上传投资者基本信息表"]
    }
}


let vaildFormClient = () => {
    $("form").submit(function (e) {
        let [val, msg] = checkPassClient()
        if (!val) {
            swal(msg)
            e.preventDefault()
        }
    });
}


let checkCompanyPics = () => {
    let d = {
        base_info_pic: "投资基本信息表",
        business_license_pic: "营业执照",
        organizing_institution_pic: "组织机构代码证",
        legal_representative_pic: " 法定代表人证件",
        authorized_representative_pic: "授权代表人证件",
        power_of_attorney_pic: "授权委托书",
    }
    let inputs = $('.info-pics').find('.hidden')
    for (let i = 0; i < inputs.length; i++) {
        let e = inputs[i]
        let v = $(e).val()
        if (!v) {
            let key = $(e).attr('name')
            let msg = d[key]
            return [v, '请上传' + msg]
        }
    }
    return [true, '']
}


let checkPassCompany = () => {
    let check = $("input[name='pass']:checked").val()
    if (check === "nopass") {
        let reason = $("#id-input-reason").val()
        return [reason, "请填写驳回理由"]
    } else {
        return checkCompanyPics()
    }
}

let vaildFormCompany = () => {
    $("form").submit(function (e) {
        let [val, msg] = checkPassCompany()
        if (!val) {
            swal(msg)
            e.preventDefault()
        }
    });
}