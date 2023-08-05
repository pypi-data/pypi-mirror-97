import { EventEmitter } from '../../stencil-public-runtime';
export declare class LimeDocumentList {
    documents: any[];
    isLoading: boolean;
    setLimeDocument: EventEmitter;
    constructor();
    render(): any;
    private selectDocument;
}
