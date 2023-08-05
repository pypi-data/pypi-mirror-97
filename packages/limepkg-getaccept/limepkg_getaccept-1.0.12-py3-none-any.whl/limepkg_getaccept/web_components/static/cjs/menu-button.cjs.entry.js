'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');

const menuButtonCss = ".ga-menu-item{display:-ms-flexbox;display:flex;-ms-flex-direction:row;flex-direction:row;cursor:pointer;padding:0.5rem}.ga-menu-item:hover{background-color:#f49132;color:#fff}.ga-menu-item .menu-icon{margin-right:0.2rem;font-size:0.6rem}";

const MenuButton = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.closeMenu = index.createEvent(this, "closeMenu", 7);
        this.handleMenuClick = this.handleMenuClick.bind(this);
    }
    render() {
        const { icon, label, view } = this.menuItem;
        return (index.h("li", { class: "ga-menu-item", onClick: () => this.handleMenuClick(view) }, index.h("limel-icon", { class: "menu-icon", name: icon, size: "small" }), index.h("span", null, label)));
    }
    handleMenuClick(view) {
        this.changeView.emit(view);
        this.closeMenu.emit(false);
    }
};
MenuButton.style = menuButtonCss;

exports.menu_button = MenuButton;
