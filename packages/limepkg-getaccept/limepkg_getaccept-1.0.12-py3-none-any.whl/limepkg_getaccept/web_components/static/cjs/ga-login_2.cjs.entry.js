'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');
const index$1 = require('./index-2fa8f133.js');

const gaLoginCss = ".auth-error{display:block;color:#f88987;margin-top:1rem}.auth-button{margin-top:1rem}limel-button{--lime-primary-color:#f49132}";

const GaLogin = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.setSession = index.createEvent(this, "setSession", 7);
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
                return (index.h("limel-input-field", { id: loginField.id, class: loginField.style, label: loginField.label, type: loginField.type, value: this[loginField.value], required: loginField.required, trailingIcon: loginField.icon, onChange: event => this.onChange(event, loginField.value) }));
            }),
            (() => {
                /* if (this.errorOnLogin) {
                    return (
                        <span class="auth-error">
                            Could not login. Please check your credentials
                        </span>
                    );
                } */
                return (index.h("div", null, index.h("limel-button", { class: "auth-button", label: "Login", primary: true, loading: this.loading, disabled: this.isDisabled(), onClick: this.onLogin }), this.errorOnLogin ? (index.h("span", { class: "auth-error" }, "Could not login. Please check your credentials")) : (null)));
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
            .get(index$1.PlatformServiceName.Http)
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
};
GaLogin.style = gaLoginCss;

const gaSignupCss = ".auth-signup-field-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}.auth-imput{margin-bottom:0.2rem;margin-right:0.5rem;width:48%}.auth-button{margin-top:1rem}.auth-imput{margin-bottom:0.2rem}.auth-language-label{display:block;margin:1rem 0rem 0.5rem 1rem}limel-button{--lime-primary-color:#f49132}";

const GaSignup = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.setSession = index.createEvent(this, "setSession", 7);
        this.errorHandler = index.createEvent(this, "errorHandler", 7);
        this.isLoading = false;
        this.disableSignup = false;
        this.signupFirstName = '';
        this.signupLastName = '';
        this.companyName = '';
        this.mobile = '';
        this.countryCode = 'SE';
        this.signupPassword = '';
        this.signupFields = [
            {
                id: 'SignupEmail',
                style: 'auth-imput',
                label: 'Email address',
                type: 'email',
                value: 'signupEmail',
                required: true,
                icon: 'filled_message',
            },
            {
                id: 'Password',
                style: 'auth-imput',
                label: 'Password',
                type: 'password',
                value: 'signupPassword',
                required: true,
                icon: 'lock_2',
            },
            {
                id: 'FirstName',
                style: 'auth-imput',
                label: 'First name',
                type: 'text',
                value: 'signupFirstName',
                required: true,
                icon: 'user',
            },
            {
                id: 'LastName',
                style: 'auth-imput',
                label: 'Last name',
                type: 'text',
                value: 'signupLastName',
                required: true,
                icon: 'user',
            },
            {
                id: 'Company',
                style: 'auth-imput',
                label: 'Company',
                type: 'text',
                value: 'companyName',
                required: true,
                icon: 'organization',
            },
            {
                id: 'Mobile',
                style: 'auth-imput',
                label: 'Mobile',
                type: 'text',
                value: 'mobile',
                required: true,
                icon: 'phone_not_being_used',
            },
        ];
        this.countryCodes = [
            {
                id: 'SE',
                text: 'SWE',
                selected: true,
            },
            {
                id: 'NO',
                text: 'NOR',
            },
            {
                id: 'FI',
                text: 'FIN',
            },
            {
                id: 'DK',
                text: 'DEN',
            },
            {
                id: 'GB',
                text: 'GBR',
            },
            {
                id: 'US',
                text: 'USA',
            },
        ];
        this.onChange = this.onChange.bind(this);
        this.countrySetOnChange = this.countrySetOnChange.bind(this);
        this.onSignup = this.onSignup.bind(this);
    }
    render() {
        this.disableSignup = this.shouldDisableSignup();
        return [
            index.h("div", { class: "auth-signup-field-container" }, this.signupFields.map((signupField) => {
                return (index.h("limel-input-field", { id: signupField.id, class: signupField.style, label: signupField.label, type: signupField.type, value: this[signupField.value], required: signupField.required, trailingIcon: signupField.icon, onChange: event => this.onChange(event, signupField.value) }));
            })),
            index.h("span", { class: "auth-language-label" }, "Country"),
            index.h("limel-chip-set", { type: "choice", onChange: this.countrySetOnChange, required: true, value: this.countryCodes }),
            index.h("limel-button", { class: "auth-button", label: "Signup", primary: true, loading: this.isLoading, disabled: this.disableSignup, onClick: this.onSignup }),
        ];
    }
    shouldDisableSignup() {
        return (this.signupEmail === '' &&
            this.signupLastName === '' &&
            this.signupLastName === '' &&
            this.mobile === '' &&
            this.signupPassword === '');
    }
    onChange(event, valueReference) {
        this[valueReference] = event.detail;
    }
    countrySetOnChange(event) {
        this.countryCode = event.detail.id.toString();
    }
    async onSignup() {
        this.isLoading = true;
        const signupData = {
            company: this.companyName,
            first_name: this.signupFirstName,
            last_name: this.signupLastName,
            country_code: this.countryCode,
            mobile: this.mobile,
            email: this.signupEmail,
            password: this.signupPassword,
        };
        const { data, success } = await index$1.signup(this.platform, signupData);
        if (success) {
            const session = {
                username: this.signupEmail,
                access_token: data.access_token,
                expires_in: data.expires_in,
            };
            this.setSession.emit(session);
        }
        else {
            if (data.error) {
                this.errorHandler.emit(data.error);
            }
            else {
                this.errorHandler.emit('Something went wrong...');
            }
        }
        this.isLoading = false;
    }
};
GaSignup.style = gaSignupCss;

exports.ga_login = GaLogin;
exports.ga_signup = GaSignup;
