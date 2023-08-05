import { IRecipient } from '../../types/Recipient';
import { EventEmitter } from '../../stencil-public-runtime';
export declare class RecipientItemAdded {
    recipient: IRecipient;
    isSigning: boolean;
    changeRecipientRole: EventEmitter<IRecipient>;
    removeRecipient: EventEmitter<IRecipient>;
    private roles;
    constructor();
    componentWillLoad(): void;
    addRecipientRoles(): void;
    render(): any;
    private handleChangeRole;
    private handleRemoveRecipient;
    private selectedRole;
}
