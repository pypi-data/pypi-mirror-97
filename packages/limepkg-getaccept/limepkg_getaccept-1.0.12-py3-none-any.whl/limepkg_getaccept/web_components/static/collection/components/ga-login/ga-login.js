import { Component, h, Prop, Event, State } from '@stencil/core';
import { PlatformServiceName, } from '@limetech/lime-web-components-interfaces';
export class GaLogin {
    constructor() {
        this.loading = false;
        this.errorOnLogin = false;
        this.email = '';
        this.password = '';
        this.loginFields = [
            {
                id: 'LoginEmail',
                style: 'auth-imput',
                label: 'Email address',
                type: 'email',
                value: 'email',
                required: false,
                icon: 'filled_message',
            },
            {
                id: 'LoginPassword',
                style: 'auth-imput',
                label: 'Password',
                type: 'password',
                value: 'password',
                required: false,
                icon: 'lock_2',
            },
        ];
        this.onChange = this.onChange.bind(this);
        this.onLogin = this.onLogin.bind(this);
        this.isDisabled = this.isDisabled.bind(this);
    }
    render() {
        return [
            this.loginFields.map((loginField) => {
                return (h("limel-input-field", { id: loginField.id, class: loginField.style, label: loginField.label, type: loginField.type, value: this[loginField.value], required: loginField.required, trailingIcon: loginField.icon, onChange: event => this.onChange(event, loginField.value) }));
            }),
            (() => {
                /* if (this.errorOnLogin) {
                    return (
                        <span class="auth-error">
                            Could not login. Please check your credentials
                        </span>
                    );
                } */
                return (h("div", null,
                    h("limel-button", { class: "auth-button", label: "Login", primary: true, loading: this.loading, disabled: this.isDisabled(), onClick: this.onLogin }),
                    this.errorOnLogin ? (h("span", { class: "auth-error" }, "Could not login. Please check your credentials")) : (null)));
            })(),
        ];
    }
    isDisabled() {
        return !(this.email && this.password);
    }
    onChange(event, valueReference) {
        this[valueReference] = event.detail;
    }
    async onLogin() {
        this.errorOnLogin = false;
        this.loading = true;
        const data = { email: this.email, password: this.password };
        const response = await this.platform
            .get(PlatformServiceName.Http)
            .post('getaccept/login/', data);
        this.loading = false;
        if (response.success) {
            const session = {
                username: this.email,
                access_token: response.data.access_token,
                expires_in: response.data.expires_in,
            };
            this.setSession.emit(session);
        }
        else {
            this.errorOnLogin = true;
        }
    }
    static get is() { return "ga-login"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["ga-login.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["ga-login.css"]
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
        "loading": {},
        "errorOnLogin": {},
        "email": {},
        "password": {}
    }; }
    static get events() { return [{
            "method": "setSession",
            "name": "setSession",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "ISession",
                "resolved": "ISession",
                "references": {
                    "ISession": {
                        "location": "import",
                        "path": "../../types/Session"
                    }
                }
            }
        }]; }
}
