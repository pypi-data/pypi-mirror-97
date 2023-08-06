import { r as registerInstance, c as createEvent, h } from './index-570406ba.js';
var menuButtonCss = ".ga-menu-item{display:-ms-flexbox;display:flex;-ms-flex-direction:row;flex-direction:row;cursor:pointer;padding:0.5rem}.ga-menu-item:hover{background-color:#f49132;color:#fff}.ga-menu-item .menu-icon{margin-right:0.2rem;font-size:0.6rem}";
var MenuButton = /** @class */ (function () {
    function MenuButton(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.closeMenu = createEvent(this, "closeMenu", 7);
        this.handleMenuClick = this.handleMenuClick.bind(this);
    }
    MenuButton.prototype.render = function () {
        var _this = this;
        var _a = this.menuItem, icon = _a.icon, label = _a.label, view = _a.view;
        return (h("li", { class: "ga-menu-item", onClick: function () { return _this.handleMenuClick(view); } }, h("limel-icon", { class: "menu-icon", name: icon, size: "small" }), h("span", null, label)));
    };
    MenuButton.prototype.handleMenuClick = function (view) {
        this.changeView.emit(view);
        this.closeMenu.emit(false);
    };
    return MenuButton;
}());
MenuButton.style = menuButtonCss;
export { MenuButton as menu_button };
