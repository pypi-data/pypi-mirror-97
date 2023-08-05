import { Component, h, Prop, Event } from '@stencil/core';
export class MenuButton {
    constructor() {
        this.handleMenuClick = this.handleMenuClick.bind(this);
    }
    render() {
        const { icon, label, view } = this.menuItem;
        return (h("li", { class: "ga-menu-item", onClick: () => this.handleMenuClick(view) },
            h("limel-icon", { class: "menu-icon", name: icon, size: "small" }),
            h("span", null, label)));
    }
    handleMenuClick(view) {
        this.changeView.emit(view);
        this.closeMenu.emit(false);
    }
    static get is() { return "menu-button"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["menu-button.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["menu-button.css"]
    }; }
    static get properties() { return {
        "menuItem": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IMenuItem",
                "resolved": "IMenuItem",
                "references": {
                    "IMenuItem": {
                        "location": "import",
                        "path": "../../types/MenuItem"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            }
        }
    }; }
    static get events() { return [{
            "method": "changeView",
            "name": "changeView",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "any",
                "resolved": "any",
                "references": {}
            }
        }, {
            "method": "closeMenu",
            "name": "closeMenu",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "any",
                "resolved": "any",
                "references": {}
            }
        }]; }
}
