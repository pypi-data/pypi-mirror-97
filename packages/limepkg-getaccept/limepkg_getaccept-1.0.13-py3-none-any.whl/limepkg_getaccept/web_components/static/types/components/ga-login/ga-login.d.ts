import { LimeWebComponentPlatform } from '@limetech/lime-web-components-interfaces';
import { ISession } from '../../types/Session';
import { EventEmitter } from '../../stencil-public-runtime';
export declare class GaLogin {
    platform: LimeWebComponentPlatform;
    setSession: EventEmitter<ISession>;
    private loading;
    private errorOnLogin;
    private email;
    private password;
    private loginFields;
    constructor();
    render(): any[];
    private isDisabled;
    private onChange;
    private onLogin;
}
