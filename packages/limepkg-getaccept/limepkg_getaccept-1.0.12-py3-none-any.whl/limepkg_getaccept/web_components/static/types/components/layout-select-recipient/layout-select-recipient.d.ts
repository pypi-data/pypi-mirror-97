import { IRecipient } from '../../types/Recipient';
import { EventEmitter } from '../../stencil-public-runtime';
import { LimeWebComponentPlatform } from '@limetech/lime-web-components-interfaces';
import { IDocument } from '../../types/Document';
export declare class LayoutSelectRecipient {
    platform: LimeWebComponentPlatform;
    document: IDocument;
    updateDocumentRecipient: EventEmitter<IRecipient[]>;
    private errorHandler;
    searchTerm: string;
    private selectedRecipientList;
    private includeCoworkers;
    private recipientList;
    componentWillLoad(): void;
    constructor();
    render(): any[];
    private selectRecipientHandler;
    removeRecipientHandler(recipient: CustomEvent<IRecipient>): void;
    changeRecipientRoleHandler(recipient: CustomEvent<IRecipient>): void;
    private isAdded;
    private toggleIncludeCoworkers;
    private onSearch;
    private fetchRecipients;
    private fetchPersons;
    private fetchCoworkers;
}
