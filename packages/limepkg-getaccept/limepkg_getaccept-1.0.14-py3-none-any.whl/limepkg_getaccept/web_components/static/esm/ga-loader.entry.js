import { r as registerInstance, h } from './index-570406ba.js';

const gaLoaderCss = "limel-spinner{margin:1rem 0;color:#f49132}";

const GALoader = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
    }
    render() {
        return (h("limel-flex-container", { justify: "center" }, h("limel-spinner", null)));
    }
};
GALoader.style = gaLoaderCss;

export { GALoader as ga_loader };
