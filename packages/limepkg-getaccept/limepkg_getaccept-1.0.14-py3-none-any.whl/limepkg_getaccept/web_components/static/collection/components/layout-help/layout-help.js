import { Component, h } from '@stencil/core';
export class LayoutHelp {
    render() {
        return [
            h("div", null,
                h("h3", null, "Help"),
                h("div", { class: "help-container" },
                    h("div", { class: "help-support" },
                        h("a", { class: "help-support-link", href: "https://www.getaccept.com/support" }, "Have any questions or just looking for someone to talk to. Our support are always there for you"),
                        h("ul", { class: "support-links-list" },
                            h("li", null,
                                h("limel-icon", { class: "support", name: "phone", size: "small" }),
                                h("a", { href: "tel:+46406688158" }, "+46 40-668-81-58")),
                            h("li", null,
                                h("limel-icon", { class: "support", name: "email", size: "small" }),
                                h("a", { href: "mailto:support@getaccept.com" }, "support@getaccept.com")))))),
        ];
    }
    static get is() { return "layout-help"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["layout-help.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["layout-help.css"]
    }; }
}
