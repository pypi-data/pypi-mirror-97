import { IDocument } from '../../types/Document';
import { EventEmitter } from '../../stencil-public-runtime';
export declare class DocumentListItem {
    document: IDocument;
    openDocument: EventEmitter<IDocument>;
    constructor();
    render(): any;
    private handleOpenDocument;
    private getDocumentIcon;
}
