import { IDocument } from '../../types/Document';
import { LimeWebComponentPlatform } from '@limetech/lime-web-components-interfaces';
import { ISession } from '../../types/Session';
export declare class LayoutOverview {
    sentDocuments: IDocument;
    platform: LimeWebComponentPlatform;
    externalId: string;
    session: ISession;
    documents: IDocument[];
    private isLoadingDocuments;
    render(): any[];
}
