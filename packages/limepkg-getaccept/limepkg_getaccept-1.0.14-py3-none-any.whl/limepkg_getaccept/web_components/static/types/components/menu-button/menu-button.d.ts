import { IMenuItem } from '../../types/MenuItem';
import { EventEmitter } from '../../stencil-public-runtime';
export declare class MenuButton {
    changeView: EventEmitter;
    closeMenu: EventEmitter;
    menuItem: IMenuItem;
    constructor();
    render(): any;
    private handleMenuClick;
}
