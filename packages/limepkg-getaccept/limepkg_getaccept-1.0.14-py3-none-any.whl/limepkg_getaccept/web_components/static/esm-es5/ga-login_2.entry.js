var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
import { r as registerInstance, c as createEvent, h } from './index-570406ba.js';
import { P as PlatformServiceName, l as signup } from './index-20a727f3.js';
var gaLoginCss = ".auth-error{display:block;color:#f88987;margin-top:1rem}.auth-button{margin-top:1rem}limel-button{--lime-primary-color:#f49132}";
var GaLogin = /** @class */ (function () {
    function class_1(hostRef) {
        registerInstance(this, hostRef);
        this.setSession = createEvent(this, "setSession", 7);
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
    class_1.prototype.render = function () {
        var _this = this;
        return [
            this.loginFields.map(function (loginField) {
                return (h("limel-input-field", { id: loginField.id, class: loginField.style, label: loginField.label, type: loginField.type, value: _this[loginField.value], required: loginField.required, trailingIcon: loginField.icon, onChange: function (event) { return _this.onChange(event, loginField.value); } }));
            }),
            (function () {
                return (h("div", null, h("limel-button", { class: "auth-button", label: "Login", primary: true, loading: _this.loading, disabled: _this.isDisabled(), onClick: _this.onLogin }), _this.errorOnLogin ? (h("span", { class: "auth-error" }, "Could not login. Please check your credentials")) : (null)));
            })(),
        ];
    };
    class_1.prototype.isDisabled = function () {
        return !(this.email && this.password);
    };
    class_1.prototype.onChange = function (event, valueReference) {
        this[valueReference] = event.detail;
    };
    class_1.prototype.onLogin = function () {
        return __awaiter(this, void 0, void 0, function () {
            var data, response, session;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.errorOnLogin = false;
                        this.loading = true;
                        data = { email: this.email, password: this.password };
                        return [4 /*yield*/, this.platform
                                .get(PlatformServiceName.Http)
                                .post('getaccept/login/', data)];
                    case 1:
                        response = _a.sent();
                        this.loading = false;
                        if (response.success) {
                            session = {
                                username: this.email,
                                access_token: response.data.access_token,
                                expires_in: response.data.expires_in,
                            };
                            this.setSession.emit(session);
                        }
                        else {
                            this.errorOnLogin = true;
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    return class_1;
}());
GaLogin.style = gaLoginCss;
var gaSignupCss = ".auth-signup-field-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}.auth-imput{margin-bottom:0.2rem;margin-right:0.5rem;width:48%}.auth-button{margin-top:1rem}.auth-imput{margin-bottom:0.2rem}.auth-language-label{display:block;margin:1rem 0rem 0.5rem 1rem}limel-button{--lime-primary-color:#f49132}";
var GaSignup = /** @class */ (function () {
    function class_2(hostRef) {
        registerInstance(this, hostRef);
        this.setSession = createEvent(this, "setSession", 7);
        this.errorHandler = createEvent(this, "errorHandler", 7);
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
    class_2.prototype.render = function () {
        var _this = this;
        this.disableSignup = this.shouldDisableSignup();
        return [
            h("div", { class: "auth-signup-field-container" }, this.signupFields.map(function (signupField) {
                return (h("limel-input-field", { id: signupField.id, class: signupField.style, label: signupField.label, type: signupField.type, value: _this[signupField.value], required: signupField.required, trailingIcon: signupField.icon, onChange: function (event) { return _this.onChange(event, signupField.value); } }));
            })),
            h("span", { class: "auth-language-label" }, "Country"),
            h("limel-chip-set", { type: "choice", onChange: this.countrySetOnChange, required: true, value: this.countryCodes }),
            h("limel-button", { class: "auth-button", label: "Signup", primary: true, loading: this.isLoading, disabled: this.disableSignup, onClick: this.onSignup }),
        ];
    };
    class_2.prototype.shouldDisableSignup = function () {
        return (this.signupEmail === '' &&
            this.signupLastName === '' &&
            this.signupLastName === '' &&
            this.mobile === '' &&
            this.signupPassword === '');
    };
    class_2.prototype.onChange = function (event, valueReference) {
        this[valueReference] = event.detail;
    };
    class_2.prototype.countrySetOnChange = function (event) {
        this.countryCode = event.detail.id.toString();
    };
    class_2.prototype.onSignup = function () {
        return __awaiter(this, void 0, void 0, function () {
            var signupData, _a, data, success, session;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.isLoading = true;
                        signupData = {
                            company: this.companyName,
                            first_name: this.signupFirstName,
                            last_name: this.signupLastName,
                            country_code: this.countryCode,
                            mobile: this.mobile,
                            email: this.signupEmail,
                            password: this.signupPassword,
                        };
                        return [4 /*yield*/, signup(this.platform, signupData)];
                    case 1:
                        _a = _b.sent(), data = _a.data, success = _a.success;
                        if (success) {
                            session = {
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
                        return [2 /*return*/];
                }
            });
        });
    };
    return class_2;
}());
GaSignup.style = gaSignupCss;
export { GaLogin as ga_login, GaSignup as ga_signup };
