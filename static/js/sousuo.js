/**
 * Created by wanglina on 2016/7/7.
 */
function js_method(akey) {
    var url = "http://www.hljss.com" + encodeURI("/s/" + akey + "/");
    window.open(url, '_blank');
}
function s_method(key) {
    var a = ""
    if (key == null) {
        a = encodeURI($("#keyword").val());
        if (a == "") {
            return false;
        }
    }
    else {
        a = key;
    }
    if (a == "") {
        return false;
    } else {
        var url = encodeURI("/ss/" + a + "/");
        window.open(url, '_blank')
    }

}