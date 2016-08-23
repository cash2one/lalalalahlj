/**
 * Created by wanglina on 2016/7/7.
 */
function js_method(key) {
    // var a = ""
    //if (key == null || key==undefined ) {
    //    a = encodeURI($("#keyword").val());
    //    if (a == "") {
    //        return false;
    //    }
    //}
    //else {
    //    a = key;
    //}
    //if (a == "") {
    //    return false;
    //} else {
    //    var url = "http://www.hljss.com" + encodeURI("/s/" + key + "/");
        var url = encodeURI("/ss/" + key + "/");
        window.open(url, '_blank');
    //}

}
function s_method() {
       var  a = encodeURI($("#keyword").val());
        if (a == "") {
            return false;
        } else {
        //var url = "http://www.hljss.com" + encodeURI("/s/" + a + "/");
        var url = encodeURI("/ss/" + a + "/");
        window.open(url, '_blank');

        }

}