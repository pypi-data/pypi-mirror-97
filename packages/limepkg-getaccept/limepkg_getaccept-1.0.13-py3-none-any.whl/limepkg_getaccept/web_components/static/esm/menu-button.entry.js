import { r as registerInstance, c as createEvent, h } from './index-570406ba.js';

const menuButtonCss = ".ga-menu-item{display:-ms-flexbox;display:flex;-ms-flex-direction:row;flex-direction:row;cursor:pointer;padding:0.5rem}.ga-menu-item:hover{background-color:#f49132;color:#fff}.ga-menu-item .menu-icon{margin-right:0.2rem;font-size:0.6rem}";

const MenuButton = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.closeMenu = createEvent(this, "closeMenu", 7);
        this.handleMenuClick = this.handleMenuClick.bind(this);
    }
    render() {
        const { icon, label, view } = this.menuItem;
        return (h("li", { class: "ga-menu-item", onClick: () => this.handleMenuClick(view) }, h("limel-icon", { class: "menu-icon", name: icon, size: "small" }), h("span", null, label)));
    }
    handleMenuClick(view) {
        this.changeView.emit(view);
        this.closeMenu.emit(false);
    }
};
MenuButton.style = menuButtonCss;

export { MenuButton as menu_button };
