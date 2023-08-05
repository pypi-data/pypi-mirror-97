import { Component, h, State, Prop } from '@stencil/core';
export class LayoutLogin {
    constructor() {
        this.isSignup = false;
        this.toggleSignupContainer = this.toggleSignupContainer.bind(this);
    }
    render() {
        const loginClass = this.isSignup
            ? 'login-container'
            : 'login-container active';
        const signupClass = this.isSignup
            ? 'signup-container active'
            : 'signup-container';
        return [
            h("div", { class: "auth-container" },
                h("div", { class: loginClass, onClick: () => this.toggleSignupContainer(false) },
                    h("h3", null, "Welcome Back"),
                    h("ga-login", { platform: this.platform })),
                h("div", { class: signupClass, onClick: () => this.toggleSignupContainer(true) },
                    h("h3", null, "Create Account"),
                    (() => {
                        if (this.isSignup) {
                            return h("ga-signup", { platform: this.platform });
                        }
                        else {
                            return (h("limel-input-field", { label: "Email address", type: "email", value: "", trailingIcon: "filled_message" }));
                        }
                    })())),
        ];
    }
    toggleSignupContainer(value) {
        this.isSignup = value;
    }
    static get is() { return "layout-login"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["layout-login.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["layout-login.css"]
    }; }
    static get properties() { return {
        "platform": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "LimeWebComponentPlatform",
                "resolved": "LimeWebComponentPlatform",
                "references": {
                    "LimeWebComponentPlatform": {
                        "location": "import",
                        "path": "@limetech/lime-web-components-interfaces"
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
    static get states() { return {
        "isSignup": {}
    }; }
}
