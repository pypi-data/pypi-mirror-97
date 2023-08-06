import { EventEmitter } from '../../stencil-public-runtime';
import { IListItem } from '../../types/ListItem';
export declare class TemplateList {
    templates: IListItem[];
    selectedTemplate: IListItem;
    isLoading: boolean;
    setTemplate: EventEmitter;
    constructor();
    render(): any;
    private selectTemplate;
}
