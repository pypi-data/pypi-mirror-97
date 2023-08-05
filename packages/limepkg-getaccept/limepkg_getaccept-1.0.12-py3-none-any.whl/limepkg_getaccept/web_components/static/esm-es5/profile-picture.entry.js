import { r as registerInstance, h } from './index-570406ba.js';
var profilePictureCss = ".thumbnail{display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center;-ms-flex-align:center;align-items:center;width:6rem;height:6rem;border-radius:50%;-webkit-box-shadow:0 3px 6px rgba(0, 0, 0, 0.05), 0 3px 6px rgba(0, 0, 0, 0.05);box-shadow:0 3px 6px rgba(0, 0, 0, 0.05), 0 3px 6px rgba(0, 0, 0, 0.05);margin-bottom:1rem}.thumbnail-placeholder{background-color:#f5f5f5}.thumbnail-placeholder limel-icon{height:3rem;width:3rem}";
var LayoutSettings = /** @class */ (function () {
    function LayoutSettings(hostRef) {
        registerInstance(this, hostRef);
    }
    LayoutSettings.prototype.render = function () {
        if (this.thumbUrl) {
            return (h("img", { class: "thumbnail", src: this.getThumbUrl(this.thumbUrl) }));
        }
        return (h("div", { class: "thumbnail thumbnail-placeholder" }, h("limel-icon", { name: "user" })));
    };
    LayoutSettings.prototype.getThumbUrl = function (originalUrl) {
        if (originalUrl === void 0) { originalUrl = ''; }
        var path = originalUrl.split('/').slice(-1)[0];
        var urlPath = originalUrl.split('/')[3];
        return "getaccept/thumb_proxy/" + urlPath + "/" + path;
    };
    return LayoutSettings;
}());
LayoutSettings.style = profilePictureCss;
export { LayoutSettings as profile_picture };
